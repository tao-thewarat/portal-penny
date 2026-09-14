from typing import ClassVar

from django import forms

from portal.models.payment_transaction import PaymentTransaction


class PaymentTransactionForm(forms.ModelForm):
    class Meta:
        model = PaymentTransaction
        fields = (
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
        )
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                },
            ),
            "user_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                },
            ),
            "type": forms.Select(
                attrs={
                    "class": "form-select",
                },
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                },
            ),
            "currency": forms.TextInput(
                attrs={
                    "class": "form-control",
                },
            ),
            "category": forms.TextInput(
                attrs={
                    "class": "form-control",
                },
            ),
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                },
            ),
            "occurred_at": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
            "confidence": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "1",
                    "min": 0,
                    "max": 1,
                },
            ),
            "source_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                },
            ),
        }
