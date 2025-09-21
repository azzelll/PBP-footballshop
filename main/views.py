import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from main.forms import ProductForm
from main.models import Product
from django.forms import inlineformset_factory
from .models import Product, ProductSize
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.decorators import login_required

ProductSizeFormSet = inlineformset_factory(
    Product,
    ProductSize,
    fields=("size", "stock"),
    extra=1, 
    can_delete=True
)

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        formset = ProductSizeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            product_sizes = formset.save(commit=False)
            for ps in product_sizes:
                ps.product = product
                ps.save()
            return redirect("main:show_main")
    else:
        form = ProductForm()
        formset = ProductSizeFormSet()

    return render(request, "add_product.html", {"form": form, "formset": formset})

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        'npm' : '2406495615',
        'name': 'Made Shandy Krisnanda',
        'class': 'PBP C',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        formset = ProductSizeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product_entry = form.save(commit=False)
            product_entry.user = request.user
            product_entry.save()
            product_sizes = formset.save(commit=False)
            for ps in product_sizes:
                ps.product = product_entry
                ps.save()
            return redirect("main:show_main")
    else:
        form = ProductForm()
        formset = ProductSizeFormSet()
    
    context = {"form": form, "formset": formset}
    return render(request, "create_product.html", context)


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
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response