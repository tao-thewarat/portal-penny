from typing import ClassVar

from django.db import models
from django.utils import timezone


class EntryType(models.TextChoices):
    EXPENSE = "expense", "Expense"
    INCOME = "income", "Income"


# Create your models here.
class PaymentTransaction(models.Model):
    name = models.CharField(
        max_length=255,
    )
    user_id = models.CharField(
        max_length=50,
        db_index=True,
    )
    type = models.CharField(
        max_length=10,
        choices=EntryType.choices,
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    currency = models.CharField(
        max_length=3,
        default="THB",
    )
    category = models.CharField(
        max_length=50,
    )
    note = models.TextField(
        blank=True,
        null=True,
    )
    occurred_at = models.DateField(
        db_index=True,
    )
    confidence = models.FloatField()
    source_text = models.TextField()
    create_at = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        db_table = "payment_transaction"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["user_id", "occurred_at"]),
            models.Index(
                fields=["user_id", "category", "occurred_at"],
            ),
        ]
