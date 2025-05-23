from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from .models import *
from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required


class HomePageView(View):
    def get(self,request):
        return render(request,"index.html")


class AboutPageView(View):
    def get(self,request):
        return render(request,"about-us.html")


def add_to_cart_view(request):
    products = Product.objects.all()

    if request.method == 'POST':
        # Получаем или создаем корзину
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            cart, created = Cart.objects.get_or_create(user=None)

        for product in products:
            qty_str = request.POST.get(f'quantity_{product.id}', '0')
            try:
                quantity = int(qty_str)
            except ValueError:
                quantity = 0

            if quantity > 0:
                item, created = CartItem.objects.get_or_create(cart=cart, product=product,
                                                               defaults={'quantity': quantity})
                if not created:
                    item.quantity += quantity
                    item.save()

        return redirect('cart_page')

    # Обработка GET — просто показываем калькулятор
    return render(request, 'calculator.html', {'products': products})


def cart_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    cart_items = cart.items.all() if cart else []

    context = {
        'cart_items': cart_items,
        'total_price': cart.total_price() if cart else 0
    }
    return render(request, 'cart.html', context)


class NewPageView(View):
    def get(self, request):
        return render(request, "news.html")


class ProductsPageView(View):
    def get(self, request):
        return render(request, "products.html")


class ProfilePageView(View):
    def get(self, request):
        return render(request, "profile.html")


def clear_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                cart.items.all().delete()
            except Cart.DoesNotExist:
                pass
        else:
            request.session['cart'] = {}
            request.session.modified = True
        return redirect('cart_page')
    else:
        return redirect('cart_page')


def send_order(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        if not phone:
            return render(request, 'cart.html', {'error': 'Пожалуйста, введите номер телефона'})

        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                items = cart.items.all()
            except Cart.DoesNotExist:
                items = []
        else:
            items = []  # Можно сделать логику для сессии, если нужно

        if not items:
            return render(request, 'cart.html', {'error': 'Корзина пуста'})

        # Формируем сообщение для отправки
        message_lines = [f"Номер телефона: {phone}", "Новый заказ:"]
        total = 0
        for item in items:
            line = f"{item.product.product_name} x{item.quantity} = {item.total_price()} so'm"
            message_lines.append(line)
            total += item.total_price()
        message_lines.append(f"Итого: {total} so'm")
        message = "\n".join(message_lines)

        # TODO: Отправка в Telegram (добавь свой токен и chat_id)
        import requests
        token = '7498237907:AAFQgiExVJqi77SaAMUxlmrtCqD5FQwGViQ'
        chat_id = '6975838199'
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message
        }
        requests.post(url, data=payload)

        # Очищаем корзину после заказа
        if request.user.is_authenticated:
            cart.items.all().delete()
        else:
            request.session['cart'] = {}
            request.session.modified = True

        return render(request, 'index.html', {'total': total})

    else:
        return redirect('cart_page')


def login_page_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # куда хочешь после входа
        else:
            error = "Неверное имя пользователя или пароль"
            return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')