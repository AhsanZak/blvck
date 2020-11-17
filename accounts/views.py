from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import userdetail
from .models import productdetail, category
from home.models import *

import base64
from django.core.files.base import ContentFile


# Create your views here.

def admin_panel(request):
    if request.session.has_key('password'):
        no_users = User.objects.count()
        return render(request, 'index.html', {'no_users': no_users})
    else:
        print("adminloginil keri")
        return redirect('/admin-login')


def admin_login(request):
    print("inside hererererer")
    if request.session.has_key('password'):
        print("first if ")
        return redirect('/adminpanel')

    if request.method == 'POST':
        us = request.POST.get('username')
        ps = request.POST.get('password')

        if us == 'admin' and ps == '12345':
            request.session['password'] = ps
            return render(request, 'index.html')
        else:
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')


def dashboard(request):
    return redirect('/admin-login')


def admin_logout(request):
    if request.session.has_key('password'):
        request.session.flush()
    print("confirm logout")
    return redirect('admin_login')


def manage_user(request):
    if request.session.has_key('password'):
        details = User.objects.all().order_by('id')
        return render(request, 'users.html', {'user': details})
    else:
        return redirect('/admin-login')


def manage_product(request):
    if request.session.has_key('password'):
        print("-----------------------------Entered PRUDCT MANAGEMENT function --------------------------------")
        details = productdetail.objects.all().order_by('id')
        return render(request, 'products.html', {'details': details})
    else:
        return redirect('/admin-login')


def delete_user(request, user_id):
    if request.session.has_key('password'):
        print("-----------------------------Entered User Delete function --------------------------------")
        User.objects.get(id=user_id).delete()
        print("User-deleted-----------------------------------")
        return redirect('/manage-user')
    else:
        return redirect('/admin-login')


def delete_product(request, product_id):
    if request.session.has_key('password'):
        print("-----------------------------Entered Delete function")
        productdetail.objects.get(id=product_id).delete()
        print("Product deleted-----------------------------------")
        # details = productdetail.objects.all().order_by('id')
        # return render(request, 'products.html', {'details': details})
        return redirect('/manage-product')
    else:
        return redirect('/admin-login')


def update_user(request, user_id):
    if request.session.has_key('password'):
        print("Entered Update User ")
        user = User.objects.filter(id=user_id).first
        return render(request, 'update.html', {'user': user})
    else:
        return redirect('/admin-login')


def edit_user(request, user_id):
    if request.session.has_key('password'):
        print("Entered Edit User function")
        if request.method == 'POST':
            user = User.objects.get(id=user_id)
            user.first_name = request.POST['full_name']
            user.email = request.POST['email']
            user.username = request.POST['username']
            user.last_name = request.POST['mobileNo']

            user.save()

            print("User Updated")
            return redirect('/manage-user')
        else:
            return HttpResponse("Say Hello to the Error")
    else:
        return redirect('/admin-login')


def update_product(request, product_id):
    if request.session.has_key('password'):
        print("Entered Update Product function ")
        product = productdetail.objects.filter(id=product_id).first()
        return render(request, 'update-product.html', {'product': product})
    else:
        return redirect('/admin-login')


def edit_product(request, product_id):
    if request.session.has_key('password'):
        print("Entered Edit Product function")
        if request.method == 'POST':
            product = productdetail.objects.get(id=product_id)
            product.product_name = request.POST['product_name']
            product.product_category = request.POST['product_category']
            product.product_price = request.POST['product_price']
            product.product_description = request.POST['product_description']
            # product.product_image = request.FILES.get('product_image')
            if 'product_image' not in request.POST:
                print("Not in post")
                product_image = request.FILES.get('product_image')
            else:
                print(" in post")
                product_image = product.product_image
            product.product_image = product_image
            product.save()

            print("Product Updated")
            return redirect('/manage-product')
        else:
            return HttpResponse("Say Hello to the Error")
    else:
        return redirect('/admin-login')


def create_user(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            first_name = request.POST['full_name']
            email = request.POST['email']
            username = request.POST['username']
            last_name = request.POST['mobileNo']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username Taken")
                    return render(request, 'signup.html')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, "Email Taken")
                    return render(request, 'signup.html')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email,
                                                    first_name=first_name, last_name=last_name)
                    user.save()
                    print("User created")
                    return redirect('/manage-user')
            else:
                messages.info(request, "Passwords Not Matching")
                return render(request, 'signup.html', )

        else:
            return render(request, 'signup.html')
    else:
        return redirect('/admin-login')


def create_product(request):
    if request.session.has_key('password'):
        print("entered product create function")
        if request.method == 'POST':
            product_name = request.POST['product_name']
            product_category = category.objects.get(category_name=request.POST['product_category'])
            product_description = request.POST['product_description']
            product_price = request.POST['product_price']
            product_image = request.FILES.get('product_image')
            image_data = request.POST['pro_img']

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            product = productdetail.objects.create(product_name=product_name, product_category=product_category,
                                                   product_description=product_description, product_price=product_price,
                                                   product_image=data)
            product.save()
            print("product created")
            return redirect('/manage-product')
        else:
            return render(request, 'create_product.html')
    else:
        return redirect('/admin-login')


def manage_category(request):
    value = category.objects.all().order_by('id')
    return render(request, 'category_management.html', {'value': value})


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        value = category.objects.create(category_name=category_name)
        value.save()
        return redirect(manage_category)
    else:
        return render(request, 'add_category.html')


def delete_category(request, id):
    b = category.objects.get(id=id)
    b.delete()
    messages.info(request, 'Deleted Successfully')
    return redirect(manage_category)


def manage_order(request):
    if request.session.has_key('password'):
        table = Order.objects.all()
        return render(request, 'manage_order.html', {'table_data': table})
    else:
        return redirect(admin_login)
