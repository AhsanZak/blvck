from django.shortcuts import render, redirect
from accounts.models import productdetail
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
import datetime
import uuid
import blvckparis


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        product = productdetail.objects.all()
        return render(request, 'home/user_index.html', {'product_data': product})
    product = productdetail.objects.all()
    return render(request, 'home/index.html', {'product_data': product})


def user_home(request):
    if request.user.is_authenticated:
        product = productdetail.objects.all()
        return render(request, 'home/user_index.html', {'product_data': product})
    else:
        return redirect('user_login')


def user_login(request):
    if request.user.is_authenticated:
        print("User is authenticated")
        return redirect('user_home')

    if request.method == 'POST':
        print("Login the User ")

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        print(user)

        if user is not None:
            print("user is not none")
            auth.login(request, user)
            return redirect('user_home')
        else:
            print("user is none")
            messages.info(request, "Invalid credentials")
            return redirect('/user_login')
    else:
        return render(request, 'home/user_login.html')


def user_signup(request):
    print("Entered user signup")
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


def edit_userProfile(request):
    print("Entered  User Profile Pic Edit")
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_image = request.FILES.get('user_image')
            user = request.user
            user.first_name = request.POST['full_name']
            user.email = request.POST['email']
            user.last_name = request.POST['mobileNo']

            print("------------------------------------------------")
            print(user_image)

            if user_image is not None:
                profilepic = UserProfile.objects.filter(user=user)
                if not profilepic:
                    UserProfile.objects.create(user_image=user_image, user=user)
                else:
                    user_profile1 = UserProfile.objects.get(user=user)
                    user_profile1.user_image = user_image
                    user_profile1.save()

            user.save()
            return redirect(user_profile)


    else:
        return redirect(user_profile)


def user_logout(request):
    auth.logout(request)
    return render(request, 'home/index.html')


def view_single(request, id):
    print(id)
    product = productdetail.objects.filter(id=id).first()
    return render(request, 'home/single.html', {'product': product})


def cart(request):
    print("--------------------------------Entered cart function---------------------------------")
    if request.user.is_authenticated:
        user = request.user
        cart = OrderItem.objects.filter(user=user)

        for i in cart:
            i.total_price = i.product.product_price * i.quantity

        return render(request, 'home/cart.html', {'cart_data': cart})
    else:
        return render(request, 'home/index.html')


def add_cart(request, id):
    print("----------------------------------Entered add_cart function--------------------------")
    if request.user.is_authenticated:
        user = request.user
        product = productdetail.objects.get(id=id)

        # Quantity
        if OrderItem.objects.filter(product=product).exists():
            order = OrderItem.objects.get(product=product)
            order.quantity += 1
            order.save()
        else:
            quantity = 1
            OrderItem.objects.create(user=user, product=product, quantity=quantity)

        return redirect(cart)
    else:
        return render(request, 'home/index.html')


def user_removeOrderItem(request, id):
    b = OrderItem.objects.get(id=id)
    b.delete()
    print("Deleted Order")
    return redirect(cart)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        items = OrderItem.objects.filter(user=user)
        order = Order.objects.filter(user=user)
        address = ShippingAddress.objects.filter(user=user)
        print(address)

        total_price = 0
        for i in items:
            total_price += i.get_total

        return render(request, 'home/checkout.html',
                      {'items': items, 'order': order, 'total_price': total_price,
                       'address': address})
    else:
        return render(request, 'home/index.html')


def user_payment(request):
    print("Entered user paymnet function ----------------------------")
    if request.user.is_authenticated:
        print("Authenticated User")
        if request.method == 'POST':
            print("post")
            user = request.user
            address = request.POST['address1']
            state = request.POST['state']
            city = request.POST['city']

            if ShippingAddress.objects.filter(address=address, state=state, city=city).exists():
                cart = OrderItem.objects.filter(user=user)
                date = datetime.datetime.now()
                transaction_id = uuid.uuid4()
                payment_mode = 'COD'
            else:
                ShippingAddress.objects.create(user=user, address=address, state=state, city=city)
                cart = OrderItem.objects.filter(user=user)
                date = datetime.datetime.now()
                transaction_id = uuid.uuid4()
                payment_mode = 'COD'
            address_instance = ShippingAddress.objects.get(address=address)
            for item in cart:
                Order.objects.create(user=user, address=address_instance, product=item.product,
                                     total_price=item.product.product_price,
                                     transaction_id=transaction_id, date_ordered=date, complete=True,
                                     payment_mode=payment_mode)
                item.product.save()
            cart.delete()

            messages.info(request, "Placed Order")
            return redirect(home)
            # return render(request, 'home/payment.html')
        else:
            print("entered payment else conditioin")
            orderItem = OrderItem.Objects.get
            return render(request, 'home/checkout.html')
    else:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        return render(request, 'home/checkout.html')


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
