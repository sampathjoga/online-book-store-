from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book, CartItem, Order
from django.contrib.auth.models import User

def index(request):
    books = Book.objects.all()
    return render(request, 'BooksApp/index.html', {'books': books})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        user.save()
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'BooksApp/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'BooksApp/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)
        return redirect('index')
    return render(request, 'BooksApp/register.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, CartItem, Order

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'BooksApp/cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        order.items.set(items)
        order.save()
        # Clear cart after order
        items.delete()
        return render(request, 'BooksApp/checkout.html', {'order': order})
    total = sum(item.total_price() for item in items)
    return render(request, 'BooksApp/checkout.html', {'items': items, 'total': total})