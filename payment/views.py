from django.shortcuts import render,redirect
from cart.cart import Cart
from .forms import ShippingForm,PaymentForm
from .models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product,Profile
import datetime
# Create your views here.
def payment_success(request):
    return render(request,"payment/payment_success.html",{})

def checkout(request):
    cart=Cart(request)
    cart_products=cart.get_prods
    quantities=cart.get_quants
    totals=cart.cart_total()
    if request.user.is_authenticated:
        #checkout as logged in user
        shipping_user=ShippingAddress.objects.get(user__id=request.user.id) 
        shipping_form=ShippingForm(request.POST or None,instance=shipping_user)

        return render(request,"payment/checkout.html",{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_form':shipping_form})
    else:
        #checkout as guest
        shipping_form=ShippingForm(request.POST or None)
        return render(request,"payment/checkout.html",{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_form':shipping_form})

def billing_info(request):
    if request.POST:    
        #Get the Cart
        cart=Cart(request)
        cart_products=cart.get_prods
        quantities=cart.get_quants
        totals=cart.cart_total()
        
        #create a session with shipping info
        my_shipping=request.POST
        request.session['my_shipping']=my_shipping

        #check to see if user is logged in 
        if request.user.is_authenticated:

             #Get billing form
            billing_form=PaymentForm()
            return render(request,"payment/billing_info.html",{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_info':request.POST,'billing_form':billing_form})    
        else:
            #Not logged in
            #Get billing form
            billing_form=PaymentForm()
            return render(request,"payment/billing_info.html",{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_info':request.POST,'billing_form':billing_form})    
    else:
        messages.success(request,"Access Denied")
        return redirect('home')
    
def process_order(request):
    if request.POST:
        #Get the cart
        cart=Cart(request)
        cart_products=cart.get_prods
        quantities=cart.get_quants
        totals=cart.cart_total()

        #Get billing info from the last page
        payment_form=PaymentForm(request.POST or None)

        #Get shipping Session Data
        my_shipping=request.session.get('my_shipping')

        #Gather Order Info
        full_name=my_shipping['shipping_full_name']
        email=my_shipping['shipping_email']
        #creating shipping address from session info
        shipping_address=f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid=totals
        
    
        if request.user.is_authenticated:
            #logged in
            user=request.user
            #Create an order
            create_order=Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()

            #Add order items
            #get order ID(pk= primary key)
            order_id=create_order.pk

            #get product info
            for product in cart_products():
                #get product ID
                product_id=product.id

                #get product price
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price

                # get product quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item=OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price)
                        create_order_item.save()
            
            #Delete cart(delete session id which keeps record of the cart) 
            for key in list(request.session.keys()):
                if key=="session_key":
                    #delete the key
                    del request.session[key]

            #delete cart from database(old cart field)
            current_user=Profile.objects.filter(user__id=request.user.id)

            #delete shopping cart from database
            current_user.update(old_cart="")

            messages.success(request,"Order Placed")
            return redirect('home')
        else:
            #not logged in
            #Create an order
            create_order=Order(full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            #Add order items
            #get order ID(pk= primary key)
            order_id=create_order.pk

            #get product info
            for product in cart_products():
                #get product ID
                product_id=product.id

                #get product price
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price

                # get product quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        #create order item
                        create_order_item=OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price)
                        create_order_item.save()

            #Delete cart(delete session id which keeps record of the cart) 
            for key in list(request.session.keys()):
                if key=="session_key":
                    #delete the key
                    del request.session[key]


            
            messages.success(request,"Order Placed")
            return redirect('home')   
        
    else:
        messages.success(request,"Access Denied")
        return redirect('home')
     
#shipped_dashboard
def shipped_dash(request):
    #want to check if user is admin and logged in
    if request.user.is_authenticated and request.user.is_superuser:   
        orders=Order.objects.filter(shipped=True)
        if request.POST:
            status=request.POST['shipping_status']
            num=request.POST['num']
            
            #grab order
            order=Order.objects.filter(id=num)

            order.update(shipped=False)
        
            messages.success(request,"Shipping Status Updated")
            return redirect('home')
        
        return render(request,"payment/shipped_dash.html",{"orders":orders})    
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


#Not Shipped Dashboard
def not_shipped_dash(request):
    #want to check if user is admin and logged in 
    if request.user.is_authenticated and request.user.is_superuser:   
        orders=Order.objects.filter(shipped=False)
        if request.POST:
            status=request.POST['shipping_status']
            num=request.POST['num']
            
            order=Order.objects.filter(id=num)
            
            now=datetime.datetime.now()
            order.update(shipped=True,date_shipped=now)
        
            messages.success(request,"Shipping Status Updated")
            return redirect('home')
        return render(request,"payment/not_shipped_dash.html",{"orders":orders})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')
    
#To open order items page
def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get order
        order=Order.objects.get(id=pk)
        #get order items
        items=OrderItem.objects.filter(order=pk)
        if request.POST:
            status=request.POST['shipping_status']
            #check if true or false
            if status=="true":
                #get the order
                order=Order.objects.filter(id=pk)
                
                #update the status
                now=datetime.datetime.now()
                order.update(shipped=True,date_shipped=now)
            else:
                #get the order
                order=Order.objects.filter(id=pk)
                
                #update the status
                order.update(shipped=False)
            messages.success(request,"Shipping Status Updated")
            return redirect('home')    
        
        return render(request,'payment/orders.html',{'order':order,'items':items})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')

