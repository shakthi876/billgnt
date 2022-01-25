import datetime
from django.contrib.auth.decorators import login_required
from datetime import date
from multiprocessing import connection
import re
from tkinter.tix import MAX
from urllib import request
from django.contrib import messages
from django.db.models.aggregates import Sum
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from accounts.models import CompanyDetails
from adminw.models import Items
from cashier.models import Bill, Sales, SalesDetails
from reportlab.lib.styles import getSampleStyleSheet
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum,Max
from django.db import connection, transaction
from django.http import HttpResponseRedirect
# Create your views here.


global bill 
@login_required(login_url='/accounts/login')
def search(request):
   
    #print(bill)
    user=request.user
    test1  = request.user.username
    print ('user',user)
    c = CompanyDetails.objects.filter(Code= test1).first()
    #c = c.first()
    print('shop',c)
    #b=SalesDetails.objects.filter(user=user).aggregate(max('BillNo'))
    #b=SalesDetails.objects.filter(user=user).order_by('-BillNo')[0]
    #print('real bill',b)
    # Finding maximum of that user
    """ args=SalesDetails.objects.filter(user=user)
    t=args.aggregate(Max('BillNo'))
    t1=t['BillNo__max']
    bill = t1 #Maximum Value
    print('The acutal max is',t['BillNo__max'])
    ########################################################################
    if t['BillNo__max'] is None:
        bill = 1
        print('super')
        print(bill) """
    """
    else:
        bill = t1+1
        print('Bill',bill)"""
    
    #t =t.objects.first()
    #bill =t
    #print('actual Bill',t)
    





    if request.method == 'POST':
        
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        id = request.POST['id']
        quantity = request.POST['quant']
    

        if Items.objects.filter(user=user,Product_Id=id).exists():
            quantity = float(quantity)
            #pid = Items.objects.filter(user=user,Product_Id=id).values('Product_Id')
            pname = Items.objects.filter(user=user,Product_Id=id).values('Product_name')
            price = Items.objects.filter(user=user,Product_Id=id).values('Price')
            print(price)
            total = price[0]['Price'] *quantity
            items = Items.objects.filter(user=user,Product_Id=id)
            #pname = items.Product_name
            #price = items.Price
            #total =  len(list(chain(quantity * price)))
            #print(price)
            #print(quantity)
            #print(total)
            
            sales = Sales(user=user ,Product_name= pname, Price=price, Quantity=quantity, Total=total)
            sales.save()
            did=sales.id
            user=request.user
            # bill=
            # print('bill number:',bill)


            args=Bill.objects.filter(user=user)
            t=args.aggregate(Max('BillNumber'))
            t1=t['BillNumber__max']
            bill = t1
            print('checking.................',bill)
            print(type(bill))

            # checkb=Bill.objects.filter(user=user).last()
            # print('checking.................',checkb)
            # print(type(checkb))
            
            details = SalesDetails(user=user,Did=did,BillNo=bill,Sold_Date=d1,Item_name=pname,Quantity=quantity)
            details.save()
            return redirect('search')
        else:
            messages.info(request, 'Item Id Not exist')
            return redirect('search')

   

    sales =Sales.objects.filter(user=user)
    checking = Sales.objects.filter(user=user).aggregate(Sum('Total'))
    #test = checking[0]['Total__sum']
    print (checking)
    items=Items.objects.filter(user=request.user).order_by('Product_Id')
    args=Bill.objects.filter(user=user)
    t=args.aggregate(Max('BillNumber'))
    t1=t['BillNumber__max']
    bill = t1
    context = {
        'sales':sales,
        'checking':checking,
        'shop' :c,
        'items':items,
        'bill': bill
    }

   



    return render(request,'search.html',context)

""" def removeall(request):
    if request.method == 'POST':
        items = Sales.objects.filter(user=request.user)
        sales = SalesDetails.objects.filter(user=request.user)
        items.delete()
        sales.delete()
        messages.info(request,'All Items got deleted')
        return redirect("search")
    else:
        return render(request,'removeall.html') """

@login_required(login_url='/accounts/login')
def remove(request,pk):
    test1  = request.user.username
    
    c = CompanyDetails.objects.filter(Code= test1).first()
    #c = c.first()
    print('shop',c)
    if request.method == 'POST':
        item=Sales.objects.get(pk=pk)
        sales= SalesDetails.objects.get(Did=pk)
        item.delete()
        sales.delete()
        messages.info(request,'Item got deleted')
        return redirect("search")
    
    context = {
        'shop': c
    }

    return render(request, 'remove.html',context)

""" def check(request):
    items=Items.objects.filter(user=request.user).order_by('Product_Id')
    content ={
        'items':items,
        
    }
    return render(request,'check.html',content) """

@login_required(login_url='/accounts/login')
def export(request):
    print('user_id=',request.user.id)
    user= request.user.id

    
    if Sales.objects.filter(user=user).exists():
        #Increment to next bill count
        args=Bill.objects.filter(user=user)
        t=args.aggregate(Max('BillNumber'))
        t1=t['BillNumber__max']
        bill = t1 + 1
        useri=request.user
        b=Bill.objects.create(user=useri,BillNumber=bill)
        b.save()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        print("d1 =", d1)   
        response = HttpResponse(content_type = 'application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Bill' + \
            str(datetime.datetime.now())+'.pdf'
        
        response['Content-Transfer-Encoding']= 'binary'

##############################################################


        select_value = request.POST.get('name_of_select') 
        print(select_value)
##############################################################


        sales = Sales.objects.filter(user=request.user)
        sum = sales.aggregate(Sum('Total'))
        print(sum)
        html_string = render_to_string('pdf-output.html',{'expenses': sales,'total': sum['Total__sum'],'date':d1})

        html =HTML(string=html_string)

        result = html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            
            output.seek(0)
            response.write(output.read())
            
            next(request)
        return response
    else:
        messages.info(request,'click next order')
        return redirect('search')

@login_required(login_url='/accounts/login')
def next(request):
    print("deleting")
    items= Sales.objects.all()
    items.delete()
    print("deleting4444")
    



        