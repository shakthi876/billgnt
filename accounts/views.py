import uuid
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import re
from unicodedata import name
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.contrib.auth.hashers import make_password
from accounts.helper import send_forget_password_mail
from accounts.models import CompanyDetails, Profile
from cryptography.fernet import Fernet
from datetime import date

# Create your views here.

from cryptography.fernet import Fernet

from cashier.models import Bill


""" def my_encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)


def my_decrypt(key, data):
    f = Fernet(key)
    return f.decrypt(data)


my_key = Fernet.generate_key()
other_key = Fernet.generate_key()
my_string = b"my deep dark secret"
print(my_string)
my_encrypt_string = my_encrypt(my_key, my_string)
print(my_encrypt_string)
my_decrypt_string = my_decrypt(my_key, my_encrypt_string)
print(my_decrypt_string)
other_decrypt_string = my_decrypt(other_key, my_encrypt_string)



 """




def login(request):
    #messages.error(request,'Invalid Credential ')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('twolink')
        else:
            messages.error(request,'Invalid Credential ')
            return redirect('login')

    return render(request,'login.html')

"""
            if username == 'admin':
                auth.login(request,user)
                messages.info(request,'Welcome Admin !!! ')
                return redirect('display')
            elif username == 'cashier':
                messages.info(request,'welcome to Bill Counter !!! ')
                return redirect('search')
            else:
                messages.info(request,'Credential Invalid :)')
                return redirect('login')
        else:
            messages.info(request,'Credential Invalid :)')
            return redirect('login')
    """


def register(request):

    
    if request.method == 'POST':
        Ccode= request.POST['CCode']
        Cname = request.POST['Companyname']
        email = request.POST.get('email')
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        password3 = request.POST['password3']
        password4 = request.POST['password4']

        if CompanyDetails.objects.filter(Code=Ccode).exists():
            messages.error(request,' Company Code Already exists')
            return redirect('register')
        else:
            if CompanyDetails.objects.filter(Company_name__iexact=Cname).exists():
                messages.error(request,'Company name already exists')
                return redirect('register')
            else:
                if CompanyDetails.objects.filter(Owner_Email_Address__iexact=email).exists():
                    messages.error(request,'Email Already exists')
                    return redirect('register')
                else:
                    if password1 != password2:
                        messages.error(request,'Password not matched')
                        return redirect('register')
                    else:
                        if password3 != password4:
                            messages.error(request,'Admin Password not matched')
                            return redirect('register')
                        else:
                            
                            mkpass=make_password(password3)
                            cdetails = CompanyDetails.objects.create(Code=Ccode,Company_name=Cname,Owner_Email_Address=email,AdminPass=mkpass)
                            cdetails.save()
                            username = Ccode
                           # mkpassu = make_password(password3)
                            user= User.objects.create_user(username=username,password= password1,email=email)
                            user.save()
                            profile_obj = Profile.objects.create(user = user)
                            profile_obj.save()
                            bill = Bill.objects.create(user=user,BillNumber=1)
                            bill.save()
                            messages.success(request,'Registered Successfully Done !!!')
                            return redirect('login')

    return render(request,'register.html')







from datetime import datetime
@login_required(login_url='/accounts/login')
def twolink(request):    
    code = request.user.username
    cname = CompanyDetails.objects.get(Code=code)
    today = date.today()


    d1 = today.strftime("%B %d, %Y")
    now = datetime.now()
    dt_string = now.strftime(" %H:%M")
    context ={
                "name": cname,
                "d1" : d1,
                "time":dt_string
            }
    return render(request,'twolink.html',context)

@login_required(login_url='/accounts/login')
def adminlogin(request):
    if request.method == 'POST':
        name=request.user.username
        admincheck= CompanyDetails.objects.filter(Code=name).values('AdminPass')
        admincheck= admincheck[0]['AdminPass']
        
        admincode = request.POST['pass']

        matchcheck=check_password(admincode,admincheck)

     
        print(admincode)
        if matchcheck:
            print('yes')
            return redirect('display')
        else:
            print('no')
            messages.error(request,'Error !! check the password')
            return redirect('adminlogin')

    name=request.user.username
    print(name)
    code = request.user.username
    cname = CompanyDetails.objects.get(Code=code)
    context = {
         "shop": cname,
     }
    return render(request,'adminlogin.html',context)




def changepassword(request , token):
    context = {}
    profile_obj = Profile.objects.filter(forget_password_token = token).first()
    print('check',profile_obj.user.id)
    context = {'user_id' : profile_obj.user.id}

    if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.error(request, 'No user id found.')
                return redirect(f'/accounts/changepassword/{token}/')
                
            
            if  new_password != confirm_password:
                messages.error(request, 'Password Not Matched')
                return redirect(f'/accounts/changepassword/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Password updated successfully!')
            return redirect('/accounts/login/')
            
            
            
    return render(request , 'changepassword.html' , context)




def forgetp(request):
    if request.method == 'POST':
        username = request.POST['username']

        if User.objects.filter(username=username).exists():
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('forgetp')

        else:
            messages.error(request,'Company code not exists')
            return redirect('forgetp')

    return render (request,'forgetp.html')

"""

def adminchange(request):
    print(request.user.username)
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1==pass2:
            pass
            
        else:
            messages.info(request,'Error !!')
            return redirect('adminchange')


    return render(request,'adminchange.html')


 """


        

    
    

def logout(request):
    auth.logout(request)
    messages.success(request,'Log out successfully !!!')
    return redirect('login')



def forgetpass(request):
    return render(request,'forgetpass.html') 


def how(request):
    code = request.user.username
    cname = CompanyDetails.objects.get(Code=code)
    context = {
         "shop": cname,
     }
    return render(request,'how.html',context)