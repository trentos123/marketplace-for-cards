from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    RARITY = [
        ("common", "Common"),
        ("uncommon", "Uncommon"),
        ("rare", "Rare"),
        ("mythic", "Mythic"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="cards/", null=True, blank=True)
    rarity = models.CharField(max_length=20, choices=RARITY, default="common")
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    # FIX: needed for sorting (optional but recommended)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)