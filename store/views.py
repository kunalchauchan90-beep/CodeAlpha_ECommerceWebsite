from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Product, Cart, Order

def home(request):
    products = Product.objects.all()

    return render(
        request,
        'index.html',
        {'products': products}
    )

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(
        request,
        'product_detail.html',
        {'product': product}
    )

def register(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/')

    return render(request, 'register.html')

def login_user(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)
            return redirect('/')

        else:

            return render(
                request,
                'login.html',
                {'error': 'Username ya Password galat hai'}
            )

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def add_to_cart(request, id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    product = Product.objects.get(id=id)

    Cart.objects.create(
        user=request.user,
        product=product
    )

    return redirect('/')

def place_order(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()

    return redirect('/')