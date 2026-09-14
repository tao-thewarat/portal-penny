import json
from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from portal.models import PaymentTransaction


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class PaymentTransactionView(View):
    def get(self, request):
        transactions = PaymentTransaction.objects.all().order_by(
            "-occurred_at",
            "-create_at",
        )
        return render(
            request=request,
            template_name="portal/payment_transaction.html",
            context={
                "transactions": transactions,
            },
        )

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                data={
                    "success": False,
                    "error": "Invalid JSON body",
                },
                status=400,
            )

        required_fields = [
            "name",
            "user_id",
            "type",
            "amount",
            "category",
            "occurred_at",
            "confidence",
            "source_text",
        ]

        if missing_fields := [
            field for field in required_fields if data.get(field) in (None, "")
        ]:
            return JsonResponse(
                data={
                    "success": False,
                    "error": "Required fields are missing",
                    "fields": missing_fields,
                },
                status=400,
            )

        if (occurred_at := parse_date(data.get("occurred_at"))) is None:
            return JsonResponse(
                data={
                    "success": False,
                    "error": "occurredAt must use YYYY-MM-DD format",
                },
                status=400,
            )

        create_at_value = data.get("create_at")
        create_at = None

        if create_at_value not in (None, ""):
            if not isinstance(create_at_value, str):
                return JsonResponse(
                    data={
                        "success": False,
                        "error": "create_at must be a string",
                    },
                    status=400,
                )

            create_at = parse_datetime(create_at_value)

            if create_at is None:
                return JsonResponse(
                    data={
                        "success": False,
                        "error": "create_at must be a valid ISO datetime",
                    },
                    status=400,
                )

        try:
            amount = Decimal(str(data.get("amount")))
        except (InvalidOperation, TypeError, ValueError):
            return JsonResponse(
                data={"success": False, "error": "amount must be a valid number"},
                status=400,
            )

        try:
            vals = {
                **data,
                "amount": amount,
                "occurred_at": occurred_at,
            }
            if create_at is not None:
                vals["create_at"] = create_at
            transaction = PaymentTransaction(**vals)
            transaction.full_clean()
            transaction.save()
        except ValidationError as error:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Validation failed",
                    "fields": error.message_dict,
                },
                status=400,
            )

        return JsonResponse(
            data={
                "success": True,
                "data": data,
            },
            status=201,
        )
