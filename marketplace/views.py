from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Card, CartItem


# =========================
# HOME
# =========================
def home(request):
    query = request.GET.get("q")
    sort = request.GET.get("sort")

    cards = Card.objects.all()

    if query:
        cards = cards.filter(title__icontains=query)

    if sort == "price_low":
        cards = cards.order_by("price")
    elif sort == "price_high":
        cards = cards.order_by("-price")
    else:
        cards = cards.order_by("-created_at")  # FIXED (now exists)

    return render(request, "marketplace/home.html", {"cards": cards})


# =========================
# DETAIL
# =========================
def detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, "marketplace/detail.html", {"card": card})


# =========================
# CREATE
# =========================
@login_required
def create(request):
    if request.method == "POST":
        Card.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            image=request.FILES.get("image"),
            seller=request.user
        )
        return redirect("home")

    return render(request, "marketplace/create.html")


# =========================
# SELLER PROFILE
# =========================
def seller_profile(request, username):
    seller = get_object_or_404(User, username=username)
    cards = Card.objects.filter(seller=seller)

    return render(request, "marketplace/seller_profile.html", {
        "seller": seller,
        "cards": cards
    })


# =========================
# CART
# =========================
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


# =========================
# REGISTER
# =========================
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})