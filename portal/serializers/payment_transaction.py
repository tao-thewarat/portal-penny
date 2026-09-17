from typing import ClassVar

from django.db import transaction
from rest_framework import serializers

from portal.models.payment_transaction import PaymentTransaction
from portal.models.payment_transaction_image import PaymentTransactionImage


class PaymentTransactionSerializer(serializers.ModelSerializer):
    image_keys = serializers.ListField(
        child=serializers.CharField(
            max_length=500,
        ),
        required=False,
        allow_empty=True,
        write_only=True,
    )

    class Meta:
        model = PaymentTransaction

        fields = (
            "id",
            "name",
            "user_id",
            "type",
            "amount",
            "currency",
            "category",
            "note",
            "occurred_at",
            "confidence",
            "source_text",
            "created_at",
            "image_keys",
        )

        read_only_fields = ("id",)

        extra_kwargs: ClassVar[dict[str, dict[str, object]]] = {
            "currency": {
                "required": False,
            },
            "note": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "created_at": {
                "required": False,
            },
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")

        return value

    def validate_confidence(self, value):
        if not 0 <= value <= 1:
            raise serializers.ValidationError("Confidence must be between 0 and 1.")

        return value

    @transaction.atomic
    def create(self, vals):
        image_keys = vals.pop("image_keys", [])
        tx = super().create(vals)
        PaymentTransactionImage.objects.bulk_create(
            objs=[
                PaymentTransactionImage(
                    transaction=tx,
                    image_key=image_key,
                )
                for image_key in image_keys
            ],
        )
        return tx
