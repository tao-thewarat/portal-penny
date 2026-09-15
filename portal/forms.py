from typing import ClassVar, cast

from django import forms

from portal.models.payment_transaction import EntryType, PaymentTransaction


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
        labels: ClassVar[dict[str, str]] = {
            "name": "ชื่อรายการ",
            "user_id": "Discord user ID",
            "type": "ประเภท",
            "amount": "จำนวนเงิน",
            "currency": "สกุลเงิน",
            "category": "หมวดหมู่",
            "note": "โน้ต",
            "occurred_at": "วันที่ทำรายการ",
            "confidence": "ความมั่นใจของ AI",
            "source_text": "ข้อความต้นฉบับ",
        }
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "เช่น Starbucks Coffee",
                    "autocomplete": "off",
                },
            ),
            "user_id": forms.TextInput(),
            "type": forms.RadioSelect(),
            "amount": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                    "inputmode": "decimal",
                    "placeholder": "0.00",
                },
            ),
            "currency": forms.TextInput(
                attrs={
                    "maxlength": 3,
                    "autocomplete": "off",
                    "aria-label": "สกุลเงิน",
                },
            ),
            "category": forms.TextInput(
                attrs={
                    "list": "category-options",
                    "autocomplete": "off",
                    "placeholder": "เลือกหรือพิมพ์หมวดหมู่",
                },
            ),
            "note": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "เลขที่ใบเสร็จ หรือรายละเอียดเพิ่มเติม",
                },
            ),
            "occurred_at": forms.DateInput(
                attrs={
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "confidence": forms.NumberInput(
                attrs={
                    "type": "range",
                    "step": "0.01",
                    "min": "0",
                    "max": "1",
                },
            ),
            "source_text": forms.Textarea(
                attrs={
                    "rows": 4,
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        type_field = cast(
            forms.ChoiceField,
            self.fields["type"],
        )
        type_field.choices = EntryType.choices

        self.fields["user_id"].disabled = True
