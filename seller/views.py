from django.shortcuts import render
from django.http import HttpResponse
from seller.models import Product, Seller
from django.core.mail import send_mail
from django.conf import settings
import random


# Create your views here.
def seller_index(request):
    try:
        seller_object = Seller.objects.get(email=request.session['email'])
        return render(request, 'seller_index.html', {'seller_data':seller_object})
    except:
        return render(request, 'seller_login.html')

def seller_logout(request):
    try:
        del request.session['email']
        return render(request, 'seller_login.html')

    except:
        return render(request, 'seller_login.html')

def add_products(request):
    if request.method == 'POST':
        seller_object = Seller.objects.get(email = request.session['email'])
        Product.objects.create(
            name = request.POST['name'],
            description = request.POST['description'],
            price = request.POST['price'],
            seller = seller_object,
            quantity = request.POST['quantity'],
            pic = request.FILES['pic']
        )
        return HttpResponse('Successfully Uploaded!!')
    else:
        return render(request, 'add_products.html')

    
def seller_register(request):
    if request.method == 'GET':
        return render(request, 'seller_register.html')
    else:
        try:
            Seller.objects.get(email = request.POST['email'])
            return render(request, 'register.html', {'msg':'Email Already exists!!'})
        except:
            global c_otp
            c_otp = random.randrange(1000, 9999)
            global seller_info
            seller_info = {
                'fname' : request.POST['fname'],
                'lname' : request.POST['lname'],
                'email' : request.POST['email'],
                'password' : request.POST['password']
            }
            subject = 'Ecommerce Seller registration'
            message = f'Hi your OTP is {c_otp}.'
            email1 = request.POST['email']
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email1] )
            return render(request, 'seller_otp.html')

    
def seller_otp(request):
    if request.method == 'POST':
        user_otp = request.POST['u_otp']
        user_otp = int(user_otp)
        print(user_otp, c_otp)
        if c_otp == user_otp:
            Seller.objects.create(
                passwd = seller_info['password'],
                fname = seller_info['fname'],
                lname = seller_info['lname'],
                email = seller_info['email']
            )
            msg = 'Successfully account created!!'
            return render(request, 'seller_login.html', {'msg': msg})
        else:
            return render(request, 'seller_otp.html', {'msg':'OTP is wrong'})
    else:
        return render(request, 'seller_register.html')


def seller_login(request):
    if request.method == 'GET':
        return render(request, 'seller_login.html')
    else:
        f_email = request.POST['email']
        f_pass = request.POST['password'] 
        try:
            user_object = Seller.objects.get(email = f_email)
            if f_pass == user_object.password:
                request.session['email'] = f_email
                return render(request, 'seller_index.html',{'user':user_object})
            else:
                return render(request, 'seller_login.html', {'msg':'Wrong Password!!'})

        except:
            return render(request, 'seller_register.html', {'msg':'Email Not Registered\nSign Up Now!!'})

        
def my_products(request):
    seller_object = Seller.objects.get(email = request.session['email'])
    seller_products =  Product.objects.filter(seller = seller_object)
    return render(request, 'my_products.html', {'my_products': seller_products})