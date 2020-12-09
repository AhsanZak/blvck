from django.shortcuts import render, redirect
from accounts.models import ProductDetail
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
import datetime
import uuid
import blvckparis
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
import requests
import json


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    else:
        product = ProductDetail.objects.all()
        return render(request, 'home/index.html', {'product_data': product})


def user_home(request):
    if request.user.is_authenticated:
        product = ProductDetail.objects.all()
        return render(request, 'home/user_index.html', {'product_data': product})
    else:
        return redirect('user_login')


def otp_login(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    otp = 1
    if request.method == 'POST':
        number = request.POST['mobile']
        request.session['number'] = number
        if User.objects.filter(last_name=number).exists():
            otp = 0
            url = "https://d7networks.com/api/verifier/send"
            number = str(91) + number
            print(number)
            payload = {
                'mobile': number,
                'sender_id': 'SMSINFO',
                'message': 'Your otp code is {code}',
                'expiry': '900'}
            files = [
            ]
            headers = {
                'Authorization': 'Token b76a52adeb253e2dbb98dd2378d542f8d53fbe6b'
            }
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            print(response.text.encode('utf8'))

            data = response.text.encode('utf8')
            datadict = json.loads(data)
            print('datadict:', datadict)

            id = datadict['otp_id']
            print('id:', id)
            request.session['id'] = id

            return render(request, 'home/otplogin.html', {'otp': otp})
        else:
            messages.info(request, "Please enter registered Number")
            return render(request, 'home/otplogin.html', {'otp': otp})
    else:
        return render(request, 'home/otplogin.html', {'otp': otp})


def verify_otp(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    else:
        if request.method == 'POST':
            otp = request.POST['otp']
            print(otp)

            id_otp = request.session['id']
            url = "https://d7networks.com/api/verifier/verify"

            payload = {'otp_id': id_otp,
                       'otp_code': otp}
            files = [

            ]
            headers = {
                'Authorization': 'Token b76a52adeb253e2dbb98dd2378d542f8d53fbe6b'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            print(response.text.encode('utf8'))
            data = response.text.encode('utf8')
            datadict = json.loads(data)
            status = datadict['status']

            if status == 'success':
                number = request.session['number']
                user = User.objects.filter(last_name=number).first()
                if user is not None:
                    if user.is_active == False:
                        messages.info(request, 'User is blocked')
                        return redirect(user_login)
                    else:
                        auth.login(request, user)
                        return redirect(user_home)
                else:
                    return redirect(user_login)

            else:
                messages.error(request, 'User not Exist')
                return redirect(user_login)

        else:
            return HttpResponse("Oops")


def user_login(request):
    if request.user.is_authenticated:
        print("User is authenticated")
        return redirect('user_home')

    if request.method == 'POST':
        print("Login the User ")

        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username).first()

        if user is not None and check_password(password, user.password):
            if user.is_active == False:
                print("user is not none")
                messages.info(request, 'User is Blocked')
                return redirect('user_login')
            else:
                auth.login(request, user)
                return redirect('user_home')
        else:
            value = {"username": username}
            messages.info(request, "Invalid Credentials")
            return redirect('user_login')

    else:
        return render(request, 'home/user_login.html')


def user_signup(request):
    if request.method == 'POST':
        first_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['username']
        last_name = request.POST['mobileNo']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        print("User values enterede")

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return render(request, 'home/user_signup.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return render(request, 'home/user_signup.html')
            elif User.objects.filter(last_name=last_name).exists():
                messages.info(request, "Mobile Number Taken")
                return render(request, 'home/user_signup.html')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()
                print("User created")
                print(username)
                print(password1)
                return redirect('user_login')

    else:
        return render(request, 'home/user_signup.html')


def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        profilepic = UserProfile.objects.filter(user=user)
        # userdetail = User.objects.filter(user=user)
        return render(request, 'home/userProfile.html', {'username': user.username, 'profilepic': profilepic})
    else:
        return redirect(user_home)


def edit_user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_image = request.FILES.get('user_image')
            user = request.user
            user.first_name = request.POST['full_name']
            user.email = request.POST['email']
            user.last_name = request.POST['mobileNo']
            image_data = request.POST['pro_img']

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=user.first_name + '.' + ext)

            if data is not None:
                profilepic = UserProfile.objects.filter(user=user)
                if not profilepic:
                    UserProfile.objects.create(user_image=data, user=user)
                else:
                    user_profile1 = UserProfile.objects.get(user=user)
                    user_profile1.user_image = data
                    user_profile1.save()

            user.save()
            return redirect(user_profile)


    else:
        return redirect(user_profile)


def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(home)


def view_single(request, id):
    print(id)
    product = ProductDetail.objects.filter(id=id).first()
    return render(request, 'home/single.html', {'product': product})


def cart(request):
    print("--------------------------------Entered cart function---------------------------------")
    if request.user.is_authenticated:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        print(cart)
        print(user.id)

        for i in cart:
            i.total_price = i.product.product_price * i.quantity

        get_total = 0
        for x in cart:
            get_total = x.get_total + get_total
        print(cart)

        return render(request, 'home/cart.html', {'cart_data': cart, 'total_amount': get_total})
    else:
        return render(request, 'home/user_login.html')


def cart_update(request, id):
    if request.method == 'POST':
        user = request.user
        action = request.POST['action']
        if action == 'add':
            print(action)
            carts = OrderItem.objects.filter(user=user)
            cart = OrderItem.objects.get(id=id)
            cart.quantity += 1
            cart.save()
            product_total = cart.product.product_price * cart.quantity
            print(id)
            print(request.POST)
            get_total = 0
            for x in carts:
                get_total = x.get_total + get_total
            return JsonResponse({"product_total": product_total, "grand_total": get_total}, safe=False)
        elif action == 'minus':
            print(action)
            carts = OrderItem.objects.filter(user=user)
            cart = OrderItem.objects.get(id=id)
            cart.quantity -= 1
            cart.save()

            product_total = cart.product.product_price * cart.quantity
            print(id)
            print(request.POST)
            get_total = 0
            for x in carts:
                get_total = x.get_total + get_total
            return JsonResponse({"product_total": product_total, "grand_total": get_total}, safe=False)

    else:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        return render(request, 'home/cart.html', {'cart_data': cart})


def add_cart(request, id):
    print("----------------------------------Entered add_cart function--------------------------")

    if request.user.is_authenticated:
        user = request.user
        product = ProductDetail.objects.get(id=id)

        # Quantity
        if OrderItem.objects.filter(product=product, user=user).exists():
            order = OrderItem.objects.get(product=product, user=user)
            order.quantity += 1
            order.save()
            print("a", id)
        else:
            print("v", id)
            quantity = 1
            OrderItem.objects.create(user=user, product=product, quantity=quantity)

        return redirect(cart)
    else:
        return render(request, 'home/user_login.html')


def user_remove_order_item(request, id):
    b = OrderItem.objects.get(id=id)
    b.delete()
    print("Deleted Order")
    return redirect(cart)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        items = OrderItem.objects.filter(user=user)
        order = Order.objects.filter(user=user)
        address = ShippingAddress.objects.filter(user=user)

        total_price = 0
        for i in items:
            total_price += i.get_total

        return render(request, 'home/checkout.html',
                      {'items': items, 'order': order, 'total_price': total_price,
                       'address': address})
    else:
        return render(request, 'home/index.html')


def add_address(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            address = request.POST['address']
            state = request.POST['state']
            city = request.POST['city']

            address = ShippingAddress.objects.create(user=user, address=address, state=state, city=city)
            address.save()
            return redirect(add_address)
        else:
            address = ShippingAddress.objects.filter(user=user)
            print(address)
            return render(request, 'home/add_address.html', {'address': address})

    else:
        return redirect(user_home)


def user_payment(request, id):
    if request.user.is_authenticated:
        print("Authenticated User")
        if request.method == 'POST':
            print("post")
            user = request.user
            mode = request.POST['mode']
            transaction_id = uuid.uuid4()
            if mode == 'Paypal':
                return JsonResponse({'mode': mode, 'tid': transaction_id}, safe=False)
            elif mode == 'Razorpay':
                return JsonResponse({'mode': mode, 'tid': transaction_id}, safe=False)

            else:
                date = datetime.datetime.now()
                address = ShippingAddress.objects.get(id=id)

                cart = OrderItem.objects.filter(user=user)
                get_total = 0
                for x in cart:
                    get_total = x.get_total + get_total
                print(get_total)

                for item in cart:
                    Order.objects.create(user=user, address=address, product=item.product,
                                         total_price=get_total,
                                         transaction_id=transaction_id, date_ordered=date, payment_status='Pending',
                                         payment_mode=mode, quantity=0, order_status='Placed')
                cart.delete()
                return JsonResponse({'mode': mode, 'tid': transaction_id}, safe=False)
        else:
            user = request.user
            address = ShippingAddress.objects.get(id=id)
            orderItem = OrderItem.objects.filter(user=user)

            get_total = 0
            for x in orderItem:
                get_total = x.get_total + get_total
            print(get_total)

            return render(request, 'home/user_payment.html',
                          {'address': address, 'items': orderItem, 'total_price': get_total})
    else:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        return render(request, 'home/checkout.html')


def success_razorpay(request):
    if request.user.is_authenticated:
        print(
            "Success Razorpay Function -------------------------------------------------******************************* ")
        date = datetime.datetime.now()
        user = request.user
        mode = 'Razorpay'
        id = request.POST['id']
        tid = request.POST['tid']
        address = ShippingAddress.objects.get(id=id)
        cart = OrderItem.objects.filter(user=user)
        get_total = 0
        for x in cart:
            get_total = x.get_total + get_total
        print(get_total)
        for item in cart:
            Order.objects.create(user=user, address=address, product=item.product,
                                 total_price=get_total,
                                 transaction_id=tid, date_ordered=date, payment_status='SUCCESS',
                                 payment_mode=mode, quantity=0, order_status='Placed')
        cart.delete()
        return JsonResponse('success', safe=False)


def success_paypal(request):
    if request.user.is_authenticated:
        date = datetime.datetime.now()
        user = request.user
        mode = 'Paypal'
        id = request.POST['id']
        tid = request.POST['tid']
        address = ShippingAddress.objects.get(id=id)
        cart = OrderItem.objects.filter(user=user)
        get_total = 0
        for x in cart:
            get_total = x.get_total + get_total
        print(get_total)
        for item in cart:
            Order.objects.create(user=user, address=address, product=item.product,
                                 total_price=get_total,
                                 transaction_id=tid, date_ordered=date, payment_status='SUCCESS',
                                 payment_mode=mode, quantity=0, order_status='Placed')
        cart.delete()
        return JsonResponse('success', safe=False)


def user_order(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user)
        order_dict = {}
        for x in order:
            if not x.transaction_id in order_dict.keys():
                order_dict[x.transaction_id] = x
                order_dict[x.transaction_id].order_price = order_dict[x.transaction_id].total_price
            else:
                order_dict[x.transaction_id].order_price += order_dict[x.transaction_id].total_price
        print(order_dict)
        return render(request, 'home/user_order.html', {'item_data': order_dict})
    return render(request, 'home/index.html')


# Razorpay

def razorpay(request):
    if request.method == 'POST':
        order_amount = 50000
        order_currency = 'USD'
        client = blvckparis.Client(auth=('rzp_test_U3zNUwvRlxDktr', '3W7BJXaO00FzZM190nJA24bK'))

        payment = client.order.create({'amount': order_amount, 'currency': 'USD', 'payment_capture': '1'})

    else:
        return render(request, 'home/razorpay.html')
    # Razorpay//
