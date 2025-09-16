from django.shortcuts import render,redirect
from .models import Product,Category,Profile

#To use login and logout functionality
from django.contrib.auth import login,logout,authenticate

#Used to show messages on screen
from django.contrib import messages

#To register new user through forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

#To use form created in forms.py file
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm

#to use form from payment app
from payment.forms import ShippingForm
from payment.models import ShippingAddress

#To use multiple filter conditions
from django.db.models import Q

#to use json
import json

#import Cart class from cart.py file in cart folder
from cart.cart import Cart

def home(request):
    cat_menu=Category.objects.all()
    products=Product.objects.all()
    return render(request,'index.html',{'products':products,'cat_menu':cat_menu})



def about(request):
    cat_menu=Category.objects.all()
    return render(request,'about.html',{'cat_menu':cat_menu})




def update_user(request):
    #check if user is already created only then we need to update its profile
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        #if current user is posted or if not posted current user is sent as instance
        user_form=UpdateUserForm(request.POST or None,instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request,"User has been updated")
            return redirect('home')
        return render(request,'update_user.html',{'user_form':user_form})
    else:
        messages.success(request,"You must be logged in to access this page")
        return redirect('home')



def update_info(request):
    if request.user.is_authenticated:
        #get current user 
        current_user=Profile.objects.get(user__id=request.user.id)
        
        #get current user's shipping info
        shipping_user=ShippingAddress.objects.get(user__id=request.user.id)
        #if current user is posted or if not posted current user is sent as instance
        #get origional user form
        form=UserInfoForm(request.POST or None,instance=current_user)
        
        #get user's shipping form
        shipping_form=ShippingForm(request.POST or None,instance=shipping_user)
        if form.is_valid():
            #save origional form
            form.save()

            #save shipping form
            shipping_form.save()

            messages.success(request,"Your information has been updated")
            return redirect('home')
        return render(request,'update_info.html',{'form':form,'shipping_form':shipping_form})
    else:
        messages.success(request,"You must be logged in to access this page")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user=request.user

        #did fill out the form
        if request.method == 'POST':
            form=ChangePasswordForm(current_user,request.POST)

            #is the form valid
            if form.is_valid():
                form.save()
                messages.success(request,"Your Password has been Updated...")
                login(request,current_user)
                return redirect('update_user')
            else:
                #show the django errors for the invalid form
                for error in list(form.errors.values()):
                    messages.error(request,error)
                return redirect('update_password')
        else:
            form=ChangePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request,"You Must be Logged in to Change Password")
        return redirect('home')


def login_user(request):
    cat_menu=Category.objects.all()
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        #authenticate username and password of user
        user=authenticate(request,username=username,password=password)
        #checking whether username is invalid or not
        if user is not None:
            login(request,user)
            
            #getting user profile 
            
            current_user=Profile.objects.get(user__id=request.user.id)
            
            #get saved cart from db model
            saved_cart=current_user.old_cart

            #convert db string back to python dictionary using JSON if cart is not empty
            if saved_cart:
                #convert to dictionary using JSON 
                converted_cart=json.loads(saved_cart)

                #add loaded cart dictionary to session
                cart=Cart(request)

                #loop through the cart and add items from database(.items function will get each item from dict. one by one)
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)

            messages.success(request,("You have been Logged In"))

            return redirect("home")
        else:
            messages.success(request,("Invaid username and password"))
            return redirect("login")
    else:
        return render(request,'login.html',{'cat_menu':cat_menu})



def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out!"))
    return redirect('home')




def register_user(request):
    cat_menu=Category.objects.all()
    form=SignUpForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        #To check the validity of form
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']

            #login user
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("Username Created-Please fill out your User information below..."))           
            return redirect('update_info')
        else:
            messages.success(request,("Registration failed.Please Try Again"))           
            return redirect('register')
    else:
        return render(request,'register.html',{'form':form,'cat_menu':cat_menu})
    



def product(request,pk):
    cat_menu=Category.objects.all()
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product,'cat_menu':cat_menu})



def category(request,cname):
    cat_menu=Category.objects.all()
    #replace hyphens with spaces
    cname=cname.replace('-',' ')

    #grab category from url
    try:
        #look up the category
        category=Category.objects.get(name=cname)
        
        products=Product.objects.filter(category=category)
        
        context={
            'products':products,
            'category':category,
            'cat_menu':cat_menu
        }
        
        return render(request,'category.html',context)
    except:
        messages.success(request,"That category doesnot exist")
        return redirect('home')



def category_summary(request):
    categories=Category.objects.all()
    return render(request,'category_summary.html',{'categories':categories})


def search(request):
    #Determine if they filled out the form
    if request.method=="POST":
        searched=request.POST['searched']
        
        #query the products DB Model
        #icontains will filter name without case sensitivity
        #Q is used for multiple filter conditions and | is used for or condition
        searched=Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        #test for no matching records
        if not searched:
            messages.error(request,"That Product Does Not Exist")
            return render(request,'search.html',{})
        else:
            return render(request,'search.html',{'searched':searched})
    else:
        return render(request,'search.html',{})

