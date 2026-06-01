import stripe
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import Card, CartItem, Order, OrderItem, SellerBalance


stripe.api_key = settings.STRIPE_SECRET_KEY


# ---------------- HOME ----------------
def home(request):
    cards = Card.objects.all()
    return render(request, "marketplace/home.html", {"cards": cards})


def detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, "marketplace/detail.html", {"card": card})


# ---------------- CART ----------------
@login_required
def add_to_cart(request, pk):
    card = get_object_or_404(Card, pk=pk)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        card=card
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart")


@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(i.card.price * i.quantity for i in items)

    return render(request, "marketplace/cart.html", {
        "items": items,
        "total": total
    })


@login_required
def remove_from_cart(request, pk):
    CartItem.objects.filter(id=pk, user=request.user).delete()
    return redirect("cart")


# ---------------- CHECKOUT ----------------
@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)

    if not items.exists():
        return redirect("cart")

    line_items = []

    for item in items:
        line_items.append({
            "price_data": {
                "currency": settings.STRIPE_CURRENCY,
                "product_data": {"name": item.card.title},
                "unit_amount": int(item.card.price * 100),
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=line_items,
        metadata={"user_id": request.user.id},
        success_url=request.build_absolute_uri("/payment-success/"),
        cancel_url=request.build_absolute_uri("/cart/"),
    )

    return redirect(session.url)


@login_required
def payment_success(request):
    return render(request, "marketplace/success.html")


# ---------------- WEBHOOK (FULL SYSTEM) ----------------
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        if Order.objects.filter(stripe_session_id=session["id"]).exists():
            return HttpResponse(status=200)

        user = User.objects.get(id=session["metadata"]["user_id"])
        items = CartItem.objects.filter(user=user)

        total = sum(i.card.price * i.quantity for i in items)

        order = Order.objects.create(
            user=user,
            total=total,
            stripe_session_id=session["id"],
            stripe_payment_intent=session.get("payment_intent")
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                card=item.card,
                quantity=item.quantity,
                price=item.card.price
            )

            item.card.stock = max(0, item.card.stock - item.quantity)
            item.card.save()

            balance, _ = SellerBalance.objects.get_or_create(
                seller=item.card.seller
            )
            balance.balance += item.card.price * item.quantity
            balance.save()

        items.delete()

    return HttpResponse(status=200)


# ---------------- REGISTER ----------------
def register(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(request, "registration/register.html", {"form": form})