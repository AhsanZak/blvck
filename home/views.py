from django.shortcuts import render, redirect
from accounts.models import productdetail
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
import datetime
import uuid


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
        return render(request, 'home/user_profile.html', {'username': user.username, 'profilepic': profilepic})


def edit_userProfile(request):
    print("Entered  User Profile Pic Edit")
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_image = request.FILES.get('user_image')
            user = request.user

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
        return render(request, 'home/cart.html', {'cart_data': cart})
    else:
        return render(request, 'home/index.html')


def add_cart(request, id):
    print("----------------------------------Entered add_cart function--------------------------")
    if request.user.is_authenticated:
        user = request.user
        product = productdetail.objects.get(id=id)

        quantity = 0
        if OrderItem.objects.filter(product=product).exists():
            quantity = quantity + 1
        else:
            quantity = 1

        items = OrderItem.objects.create(user=user, product=product, quantity=quantity)
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

        return render(request, 'home/checkout.html', {'items': items, 'order': order})
    else:
        return render(request, 'home/index.html')


#
# def checkout(request):
#     return render(request, 'home/checkout.html')


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
            address = ShippingAddress.objects.create(address=address, state=state, city=city)

            cart = OrderItem.objects.filter(user=user)
            date = datetime.datetime.now()
            transaction_id = uuid.uuid4()
            for item in cart:
                Order.objects.create(user=user, address=address, product=item.product,
                                     total_price=item.product.product_price,
                                     transaction_id=transaction_id, date_ordered=date, complete=True)
                item.product.save()
            cart.delete()
            messages.info(request, "Placed Order")
            return redirect(home)
            # return render(request, 'home/payment.html')
        else:
            print("entered payment else conditioin")
            return render(request, 'home/checkout.html')
    else:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        return render(request, 'home/checkout.html')


def user_order(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user)
        cart = OrderItem.objects.filter(user=user)
        return render(request, 'home/user_order.html', {'item_data': order})
    return render(request, 'home/user_order.html')
