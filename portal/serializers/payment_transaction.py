from typing import ClassVar

from rest_framework import serializers

from portal.models import PaymentTransaction


class PaymentTransactionSerializer(serializers.ModelSerializer):
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
