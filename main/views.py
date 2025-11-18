import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse
from main.forms import ProductForm
from main.models import Product
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
    response = HttpResponseRedirect(reverse('main:login') + '?logout=success')
    response.delete_cookie('last_login')
    return response

@csrf_exempt
@require_POST
def create_product_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
    
    try:
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        description = request.POST.get('description')
        thumbnail = request.POST.get('thumbnail', '')
        category = request.POST.get('category', 'shoes')
        stock = int(request.POST.get('stock', 0))
        sizes = request.POST.get('sizes', '')
        discount = int(request.POST.get('discount', 0))
        price = int(request.POST.get('price', 0))
        rating = float(request.POST.get('rating', 0))
        is_featured = request.POST.get('is_featured', 'false').lower() == 'true'
        
        product = Product.objects.create(
            user=request.user,
            name=name,
            brand=brand,
            description=description,
            thumbnail=thumbnail,
            category=category,
            stock=stock,
            sizes=sizes,
            discount=discount,
            price=price,
            rating=rating,
            is_featured=is_featured,
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Product "{product.name}" created successfully!',
            'product_id': str(product.id)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
    
    try:
        product = Product.objects.get(pk=id)
        
        if product.user != request.user:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        
        product_name = product.name
        product.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Product "{product_name}" deleted successfully!'
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)

def get_products_json(request):
    products = Product.objects.all().order_by('-is_featured', '-created_at')
    
    data = []
    for product in products:
        data.append({
            'id': str(product.id),
            'name': product.name,
            'brand': product.brand,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'category_display': product.get_category_display(),
            'price': product.price,
            'discount': product.discount,
            'final_price': product.final_price,
            'formatted_price': product.formatted_price(),
            'stock': product.stock,
            'is_in_stock': product.is_in_stock(),
            'sizes': product.sizes,
            'sizes_list': product.get_sizes_list(),
            'rating': product.rating,
            'is_featured': product.is_featured,
            'user_id': product.user.id if product.user else None,
            'user_username': product.user.username if product.user else 'Anonymous',
            'is_owner': product.user == request.user if request.user.is_authenticated else False
        })
    
    return JsonResponse(data, safe=False)

@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': f'Welcome back, {user.username}!',
                'username': user.username
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid username or password.'
            }, status=401)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Account created successfully!',
                'username': user.username
            })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(e) for e in error_list]
            
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
@require_POST
def update_product_ajax(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
    
    try:
        product = Product.objects.get(pk=id)
        
        if product.user != request.user:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        
        # Update product fields
        product.name = request.POST.get('name', product.name)
        product.brand = request.POST.get('brand', product.brand)
        product.description = request.POST.get('description', product.description)
        product.thumbnail = request.POST.get('thumbnail', product.thumbnail)
        product.category = request.POST.get('category', product.category)
        product.stock = int(request.POST.get('stock', product.stock))
        product.sizes = request.POST.get('sizes', product.sizes)
        product.discount = int(request.POST.get('discount', product.discount))
        product.price = int(request.POST.get('price', product.price))
        product.rating = float(request.POST.get('rating', product.rating))
        product.is_featured = request.POST.get('is_featured', 'false').lower() == 'true'
        
        product.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Product "{product.name}" updated successfully!',
            'product_id': str(product.id)
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
@csrf_exempt
@require_POST
def create_product_flutter(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Unauthorized'
        }, status=401)
    
    try:
        data = json.loads(request.body)
        
        name = data.get('name')
        brand = data.get('brand')
        description = data.get('description')
        thumbnail = data.get('thumbnail', '')
        category = data.get('category', 'shoes')
        stock = int(data.get('stock', 0))
        sizes = data.get('sizes', '')
        discount = float(data.get('discount', 0))
        price = int(data.get('price', 0))
        rating = float(data.get('rating', 0))
        is_featured_str = data.get('is_featured', 'false')
        is_featured = is_featured_str.lower() == 'true'
        
        product = Product.objects.create(
            user=request.user,
            name=name,
            brand=brand,
            description=description,
            thumbnail=thumbnail,
            category=category,
            stock=stock,
            sizes=sizes,
            discount=discount,
            price=price,
            rating=rating,
            is_featured=is_featured,
        )
        
        return JsonResponse({
            'status': 'success',
            'message': f'Product "{product.name}" created successfully!',
            'product_id': str(product.id)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)