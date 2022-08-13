from django.contrib.auth import get_user_model
from django.shortcuts import render,get_object_or_404
from .models import Category,Product
from django_user_interaction_log.registrars import create_log_record
from cart.forms import CartAddProductForm
# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    return render(request,'shop/product/list.html',{'category': category,'categories':categories,'products':products})

def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_product_form=CartAddProductForm()
    target_object = None
    if get_user_model().objects.filter().exists():
        target_object = get_user_model().objects.first()
    create_log_record(request=request, log_detail='User view product',
                      log_target=target_object)
    return render(request,'shop/product/detail.html',{'product': product, 'cart_product_form':cart_product_form})

def index(req):
    return render(req, 'shop/base.html')