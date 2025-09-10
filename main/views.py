from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.forms import ProductForm
from main.models import Product
from django.forms import inlineformset_factory
from .models import Product, ProductSize

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

def show_main(request):
    product_list = Product.objects.all()

    context = {
        'npm' : '2406495615',
        'name': 'Made Shandy Krisnanda',
        'class': 'PBP C',
        'product_list': product_list
    }

    return render(request, "main.html", context)

def create_product(request):
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

    return render(request, "create_product.html", {"form": form, "formset": formset})

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
    