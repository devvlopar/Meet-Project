import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from buyer.models import Buyer, Cart
from django.http import HttpResponse

from seller.models import Product

import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.



def index(request):
    try:
        user_object = Buyer.objects.get(email = request.session['email'])
        all_products = Product.objects.all()
        return render(request, 'index.html', {'user':user_object, 'all_products': all_products})
    except:
        return render(request, 'login.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        f_email = request.POST['email']
        f_pass = request.POST['password'] 
        try:
            user_object = Buyer.objects.get(email = f_email)
            if f_pass == user_object.passwd:
                request.session['email'] = f_email
                all_products = Product.objects.all()
                return render(request, 'index.html',{'user':user_object, 'all_products': all_products})
            else:
                return render(request, 'login.html', {'msg':'Wrong Password!!'})

        except:
            return render(request, 'register.html', {'msg':'Email Not Registered\nSign Up Now!!'})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        try:
            Buyer.objects.get(email = request.POST['email'])
            return render(request, 'register.html', {'msg':'Email Already exists!!'})
        except:
            global c_otp
            c_otp = random.randrange(1000, 9999)
            global user_info
            user_info = {
                'fname' : request.POST['fname'],
                'lname' : request.POST['lname'],
                'email' : request.POST['email'],
                'password' : request.POST['password']
            }
            subject = 'Ecommerce registration'
            message = f'Hi your OTP is {c_otp}.'
            email1 = request.POST['email']
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email1] )
            return render(request, 'otp.html')

def otp(request):
    if request.method == 'POST':
        user_otp = request.POST['u_otp']
        user_otp = int(user_otp)
        print(user_otp, c_otp)
        if c_otp == user_otp:
            Buyer.objects.create(
                passwd = user_info['password'],
                fname = user_info['fname'],
                lname = user_info['lname'],
                email = user_info['email']
            )
            msg = 'Successfully account created!!'
            return render(request, 'register.html', {'msg': msg})
        else:
            return render(request, 'otp.html', {'msg':'OTP is wrong'})
    else:
        return render(request, 'register.html')

def shop(request):
    return render(request, 'shop.html')

def logout(request):
    try:
        del request.session['email']
        return render(request,'login.html')
    except:
        return render(request,'login.html')

def profile(request):
    if request.method == 'POST':
        new = {
            'fname' : request.POST['fname'],
            'lname' : request.POST['lname'],
            'passwd' : request.POST['password']
        }
        session_user = Buyer.objects.get(email = request.session['email'])
        session_user.fname = new['fname']
        session_user.lname = new['lname']
        session_user.passwd = new['passwd']
        if 'pic' in request.FILES:
            session_user.pic = request.FILES['pic']
        session_user.save()



        user_data = Buyer.objects.get(email = request.session['email'])
        return render(request, 'profile.html', {'user':user_data})

    else:
        try:
            user_data = Buyer.objects.get(email = request.session['email'])
            return render(request, 'profile.html', {'user':user_data})
        except:
            return render(request, 'login.html')


def cart(request):
    buyer_object = Buyer.objects.get(email = request.session['email'])
    cart_data = Cart.objects.filter(buyer = buyer_object)
    total = 0
    for i in cart_data:
        total += i.product.price
    global final_total
    final_total = total + 100


    currency = 'INR'
    amount = final_total*100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['cart_data'] = cart_data
    context['total'] = total
    context['final_total'] = final_total



    return render(request, 'cart.html', context = context)

def add_to_cart(request, pk):
    product_object = Product.objects.get(id= pk)
    buyer_object = Buyer.objects.get(email = request.session['email']) 
    Cart.objects.create(
        product = product_object,
        buyer = buyer_object
    )
    all_products = Product.objects.all()

    return render(request, 'index.html' , {'user':buyer_object,'all_products': all_products})


def remove_item(request, pk):
    # DRY : Don't Repeat Yourself
    # API : Application Programming Interface
    d_product = Cart.objects.get(id = pk)
    d_product.delete()
    return redirect('cart')


#Payment Process Starts From Here

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 

 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(
            #     params_dict)
            # if result is not None:
            amount = final_total * 100  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)

                # render success page on successful caputre of payment
                return render(request, 'paymentsuccess.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'paymentfail.html')
            
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponse('fail')
    else:
       # if other than POST request is made.
        return HttpResponse('method failiure')
