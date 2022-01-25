import re
from django.db.models import Count
from django.core.checks import messages
from django.shortcuts import render,redirect
from django.contrib import messages
from accounts.models import CompanyDetails
from adminw.forms import ItemModifyForm
from adminw.models import Items
import re
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/accounts/login')
def display(request):
    user=request.user
    test1  = request.user.username
    print(request.user.username)

    c = CompanyDetails.objects.filter(Code= test1).values('Company_name')
    c = c[0]['Company_name']
    print(c)



    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        price = request.POST['price']
        if int(price) > 0:
            if not re.search(r'\d', name) and len(name)<=30:
                if Items.objects.filter(user=user,Product_Id=id).exists():
                #print(ID_check)
                #ID_check= ID_check[0]['Product_Id']
                #print(ID_check)
                #if ID_check == id:
                #if Items.objects.filter(Product_Id=id).exists():
                    print('yes')
                    messages.info(request,'Product Id already exists... enter unique Product ID')
                    return redirect('display')
                
                else:
                    additems=Items(Product_Id=id,Product_name=name,Price=price,user=user)
                    additems.save()
                    return redirect('display')
            else:
                messages.info(request,'Product name must have only alphabets, maximum of 30...')
                return redirect('display')
        else:
            messages.info(request,'Price cannot be negative')
            return redirect('display')
    
    items=Items.objects.filter(user=user).order_by('Product_Id')
    content ={
        'items':items,
        'shop' :c
    }
    return render(request,'display.html',content)

@login_required(login_url='/accounts/login')
def deleteitem(request,pk):

    code = request.user.username
    cname = CompanyDetails.objects.get(Code=code)
    context = {
         "shop": cname,
     }
    if request.method == 'POST':
        item=Items.objects.get(pk=pk)
        item.delete()
        messages.info(request,'Item got deleted')
        return redirect("display")
    
    return render(request, 'deleteitem.html',context)

@login_required(login_url='/accounts/login')
def modify(request,pk):
    code = request.user.username
    cname = CompanyDetails.objects.get(Code=code)
   
    queryset = Items.objects.get(Product_Id = pk, user=request.user)
    #form_class = ItemModifyForm
    form = ItemModifyForm (instance=queryset)
    if request.method == 'POST':
        form = ItemModifyForm (request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect("display")
        
    items=Items.objects.filter(user=request.user).filter(Product_Id=pk)
    context ={
            'items':items,
            'form': form,
            "shop": cname
             }
    return render(request,'modify.html',context)

@login_required(login_url='/accounts/login')
def deleteall(request):


    code = request.user.username
    cname = CompanyDetails.objects.get(Code=code)
    context = {
         "shop": cname,
     }
    if request.method == 'POST':
        items = Items.objects.filter(user=request.user)
        items.delete()
        messages.info(request,'All Items got deleted')
        return redirect("display")
  
    return render(request,'deleteall.html',context)

  

