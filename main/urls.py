from django.urls import path
from main.views import (
    # Web views
    show_main, create_product, show_product, show_xml, show_json, 
    show_json_by_id, show_xml_by_id, register, login_user, logout_user, 
    edit_product, delete_product, create_product_ajax, delete_product_ajax, 
    update_product_ajax, get_products_json, login_ajax, register_ajax,
    # Flutter views  
    create_product_flutter, get_products_flutter
)

app_name = 'main'

urlpatterns = [
    # Web routes
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('product/<uuid:id>/', show_product, name='show_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:Product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:Product_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<uuid:id>/edit/', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete/', delete_product, name='delete_product'),
    
    # AJAX API routes (for web)
    path('api/products/', get_products_json, name='get_products_json'),
    path('api/create-ajax/', create_product_ajax, name='create_product_ajax'),
    path('api/update-ajax/<uuid:id>/', update_product_ajax, name='update_product_ajax'),
    path('api/delete-ajax/<uuid:id>/', delete_product_ajax, name='delete_product_ajax'),
    path('api/login/', login_ajax, name='login_ajax'),
    path('api/register/', register_ajax, name='register_ajax'),
    
    # Flutter API routes  
    path('flutter/products/', get_products_flutter, name='get_products_flutter'),
    path('flutter/create/', create_product_flutter, name='create_product_flutter'),
]