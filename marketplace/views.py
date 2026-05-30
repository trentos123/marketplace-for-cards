from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Card, CartItem, Order


# HOME
def home(request):
    cards = Card.objects.all().order_by("-id")
    return render(request, "marketplace/home.html", {"cards": cards})


# DETAIL
def detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, "marketplace/detail.html", {"card": card})


# CREATE SELL LISTING
@login_required
def create(request):
    if request.method == "POST":
        Card.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            price=request.POST["price"],
            image=request.FILES.get("image"),
            seller=request.user
        )
        return redirect("home")

    return render(request, "marketplace/create.html")


# SELLER PAGE
def seller_profile(request, username):
    cards = Card.objects.filter(seller__username=username)
    return render(request, "marketplace/seller_profile.html", {"cards": cards})


# CART
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


# CHECKOUT
@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(i.card.price * i.quantity for i in items)

    if request.method == "POST":
        Order.objects.create(user=request.user, total=total)
        items.delete()
        return redirect("dashboard")

    return render(request, "marketplace/checkout.html", {"total": total})


# DASHBOARD
@login_required
def dashboard(request):
    cards = Card.objects.filter(seller=request.user)
    orders = Order.objects.filter(user=request.user)

    return render(request, "marketplace/dashboard.html", {
        "cards": cards,
        "orders": orders
    })


# REGISTER
def register(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("/")

    return render(request, "registration/register.html", {"form": form})