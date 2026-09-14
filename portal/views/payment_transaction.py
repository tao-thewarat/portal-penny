from typing import ClassVar

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from portal.models import PaymentTransaction
from portal.serializers.payment_transaction import PaymentTransactionSerializer


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class PaymentTransactionView(APIView):
    permission_classes: ClassVar[list[type[AllowAny]]] = [
        AllowAny,
    ]

    def get(self, request):
        transactions = PaymentTransaction.objects.all().order_by(
            "-occurred_at",
            "-created_at",
        )
        return render(
            request=request,
            template_name="portal/payment_transaction.html",
            context={
                "transactions": transactions,
            },
        )

    def post(self, request, *args, **kwargs):
        serializer = PaymentTransactionSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                data={
                    "success": False,
                    "error": "Validation failed",
                    "fields": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction = serializer.save()

        return Response(
            data={
                "success": True,
                "data": PaymentTransactionSerializer(
                    transaction,
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )
