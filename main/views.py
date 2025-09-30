import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from main.forms import ProductForm
from main.models import Product
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_main(request):
    filter_value = request.GET.get("filter", "all")
    category = request.GET.get("category", None)
    if filter_value == "my":
        filter_type = "my"
    else:
        filter_type = "all"
        
    # Start with all products or user's products
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    # Apply category filter if specified
    if category:
        product_list = product_list.filter(category=category)

    # Order by: featured first, then by latest
    product_list = product_list.order_by('-is_featured', '-id')

    context = {
        'npm': '2406495615',
        'name': 'Made Shandy Krisnanda',
        'class': 'PBP C',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_entry = form.save(commit=False)
            product_entry.user = request.user
            product_entry.save()
            messages.success(request, f'Product "{product_entry.name}" has been created successfully!')
            return redirect("main:show_main")
        else:
            messages.error(request, 'Failed to create product. Please check the form.')
    else:
        form = ProductForm()
    
    context = {"form": form}
    return render(request, "create_product.html", context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    # Check if user is the owner
    if product.user != request.user:
        messages.error(request, 'You are not allowed to edit this product.')
        return redirect('main:show_main')
    
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, f'Product "{product.name}" has been updated successfully!')
        return redirect('main:show_main')

    context = {
        'form': form,
        'product': product
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    # Check if user is the owner
    if product.user != request.user:
        messages.error(request, 'You are not allowed to delete this product.')
        return redirect('main:show_main')
    
    product_name = product.name
    product.delete()
    messages.success(request, f'Product "{product_name}" has been deleted successfully!')
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login') 
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, Product_id):
    try:
        product_item = Product.objects.filter(pk=Product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, Product_id):
    try:
        product_item = Product.objects.get(pk=Product_id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            messages.success(request, f'Welcome back, {user.username}!')
            return response
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    messages.success(request, 'You have been logged out successfully.')
    return response