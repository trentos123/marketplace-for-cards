from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from decimal import Decimal

from .models import Card, CartItem, Order


def home(request):
    cards = Card.objects.all().order_by("-created_at")
    return render(request, "marketplace/home.html", {"cards": cards})


def detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, "marketplace/detail.html", {"card": card})


@login_required
def create(request):
    if request.method == "POST":
        Card.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description", ""),
            price=Decimal(request.POST.get("price") or 0),
            rarity=request.POST.get("rarity", "common"),
            image=request.FILES.get("image"),
            seller=request.user,
        )
        return redirect("home")

    return render(request, "marketplace/create.html")


def seller_profile(request, username):
    cards = Card.objects.filter(seller__username=username)
    return render(request, "marketplace/seller_profile.html", {"cards": cards})


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
    total = sum(item.card.price * item.quantity for item in items)

    return render(request, "marketplace/cart.html", {
        "items": items,
        "total": total
    })


@login_required
def remove_from_cart(request, pk):
    CartItem.objects.filter(id=pk, user=request.user).delete()
    return redirect("cart")


@login_required
def dashboard(request):
    cards = Card.objects.filter(seller=request.user)
    orders = Order.objects.filter(user=request.user)

    return render(request, "marketplace/dashboard.html", {
        "cards": cards,
        "orders": orders
    })


def register(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(request, "registration/register.html", {"form": form})