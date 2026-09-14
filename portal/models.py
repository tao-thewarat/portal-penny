from django.db import models

# Create your models here.
class PaymentTransaction(models.Model):
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    description = models.CharField(
        max_length=255,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
