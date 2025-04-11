from django.db import models
from django.contrib.auth.models import User

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_amount = models.FloatField(verbose_name="Initial Investment")
    date_added = models.DateTimeField(auto_now_add=True)
    profit_percentage = models.FloatField(verbose_name="Profit Percentage", null=True, blank=True)
    notes = models.TextField(blank=True)

class Partner(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name="partners")
    name = models.CharField(max_length=100)
    amount = models.FloatField(verbose_name="Partner Investment")
    profit_share = models.FloatField(verbose_name="Profit Share (%)")

class ProductPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    cost_per_unit = models.FloatField()
    amount = models.IntegerField(help_text="Number of units purchased")
    weight = models.CharField(max_length=50, help_text="e.g., 5 pounds, 500g")
    total_cost = models.FloatField(editable=False)  # Auto-calculated
    date_added = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_cost = self.cost_per_unit * self.amount
        super().save(*args, **kwargs)
