from locale import currency
from django.shortcuts import render,redirect
from requests import request
from ecommerceapp.models import Contact,Product,OrderUpdate,Orders
from django.contrib import messages
from math import ceil
from django.conf import settings
import json
from django.views.decorators.csrf import  csrf_exempt

import razorpay



# Create your views here.
def index(request):

    allProds = []
    catprods = Product.objects.values('category','id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}

    return render(request,"index.html",params)

    
def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"we will get back to you soon..")
        return render(request,"contact.html")


    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def invoice(request):
    return render(request,"invoice.html")



def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')
      
      
      

    if request.method=="POST":
    
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt', '')
        email = request.POST.get('email','')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        
        Order = Orders(items_json=items_json,name=name,amount=amount,email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        payment_id = request.POST.get('razorpay_payment_id')
       
        
        print(amount)
        print(payment_id)
        Order.save()
        # update.save()
        # print(update)
        thank = True
        
        print(Order.amount)
        
        try:
            amount_integer = int(float(amount))
            print("Total amount as integer:", amount_integer*100)
            
        except ValueError:
            print("Invalid total amount string")
   
        
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        print(f"your id is:{Order.order_id}")
        
        id = Order.order_id
        oid = str('id')+"karthik"
        
        print(id)
        print(oid)
        
        
# # PAYMENT INTEGRATION
        keyid = 'rzp_test_8sh7NnXxIa7Lt0'
        keySecret = 'aX5PG6nix5jd8x9CiBv0yVyV'
 
        client = razorpay.Client(auth=(keyid, keySecret))
   

        context = {
            "amount": amount_integer * 100,
          
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        #server
        #
        order = client.order.create(data=context)
        print(order)
        print(order['id'])
        print(order['amount'])
        print(payment_id)
        
      
        return render(request, 'paytm.html',context)
        

    return render(request, 'checkout.html')

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')
    currentuser=request.user.username
   
    items=Orders.objects.filter(email=currentuser)
    
    rid=""
    for i in items:
        print(i.oid)
   
        myid=i.oid
        rid=myid.replace("ShopyCart","")
        print(rid)
    status=OrderUpdate.objects.filter( order_id=rid)
    for j in status:
        print(j.update_desc)

   
    context ={"items":items,"status":status}
   
    return render(request,"profile.html",context)

