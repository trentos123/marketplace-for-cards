import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

from .models import Card, CartItem, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    cards = Card.objects.all()

    q = request.GET.get("q")
    rarity = request.GET.get("rarity")
    max_price = request.GET.get("max_price")

    if q:
        cards = cards.filter(title__icontains=q)

    if rarity:
        cards = cards.filter(rarity=rarity)

    if max_price:
        cards = cards.filter(price__lte=max_price)

    return render(request, "marketplace/home.html", {"cards": cards})


def card_detail(request, pk):
    card = Card.objects.get(id=pk)
    return render(request, "marketplace/card_detail.html", {"card": card})


@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(i.card.price * i.quantity for i in items)

    return render(request, "marketplace/cart.html", {
        "items": items,
        "total": total
    })


@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)

    line_items = []
    total = 0

    for i in items:
        total += i.card.price * i.quantity

        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": i.card.title},
                "unit_amount": int(i.card.price * 100),
            },
            "quantity": i.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://127.0.0.1:8000/orders/",
        cancel_url="http://127.0.0.1:8000/cart/",
    )

    Order.objects.create(user=request.user, total=total)

    return redirect(session.url)


@login_required
def ajax_add_to_cart(request, pk):
    card = Card.objects.get(id=pk)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        card=card
    )

    if not created:
        item.quantity += 1
        item.save()

    return JsonResponse({"success": True})


def seller_profile(request, username):
    seller = User.objects.get(username=username)
    cards = Card.objects.filter(seller=seller)

    return render(request, "marketplace/seller_profile.html", {
        "seller": seller,
        "cards": cards
    })


@login_required
def dashboard(request):
    cards = Card.objects.filter(seller=request.user)
    return render(request, "marketplace/dashboard.html", {"cards": cards})


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    CartItem.objects.filter(user=request.user).delete()

    return render(request, "marketplace/orders.html", {"orders": orders})