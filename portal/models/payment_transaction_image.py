from django.conf import settings
from django.db import models

from .payment_transaction import PaymentTransaction


class PaymentTransactionImage(models.Model):
    transaction = models.ForeignKey(
        to=PaymentTransaction,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image_key = models.CharField(
        max_length=500,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "payment_transaction_image"

    @property
    def image_url(self) -> str | None:
        if not settings.R2_PUBLIC_BASE_URL or not self.image_key:
            return None
        return f"{settings.R2_PUBLIC_BASE_URL}/{self.image_key.lstrip('/')}"
