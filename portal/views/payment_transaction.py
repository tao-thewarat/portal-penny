from typing import ClassVar

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from portal.forms import PaymentTransactionForm
from portal.models.payment_transaction import PaymentTransaction
from portal.serializers.payment_transaction import PaymentTransactionSerializer


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class PaymentTransactionView(APIView):
    permission_classes: ClassVar[list[type[AllowAny]]] = [
        AllowAny,
    ]

    def get(self, request):
        if not (
            user := SocialAccount.objects.filter(
                user=request.user,
                provider="discord",
            ).first()
        ):
            return redirect("accounts/discord/login/")

        tx = PaymentTransaction.objects.filter(
            user_id=user.uid,
        ).order_by(
            "-occurred_at",
            "-created_at",
        )
        return render(
            request=request,
            template_name="portal/payment_transaction.html",
            context={
                "transactions": tx,
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


class PaymentTransactionFormView(View):
    template_name = "portal/payment_transaction_form.html"

    def get(self, request, pk):
        tx = get_object_or_404(
            PaymentTransaction,
            pk=pk,
        )
        form = PaymentTransactionForm(
            instance=tx,
        )

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "form": form,
                "tx": tx,
            },
        )

    def post(self, request, pk):
        tx = get_object_or_404(
            PaymentTransaction,
            pk=pk,
        )
        form = PaymentTransactionForm(data=request.POST, instance=tx)

        if form.is_valid():
            form.save()
            return redirect("transactions")

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "form": form,
                "tx": tx,
            },
        )
