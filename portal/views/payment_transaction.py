from decimal import Decimal
from typing import ClassVar

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from portal.forms import PaymentTransactionForm
from portal.models.payment_transaction import EntryType, PaymentTransaction
from portal.permissions import HasBotApiToken
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
            logout(request)
            return redirect("discord_login")

        tx = PaymentTransaction.objects.filter(
            user_id=user.uid,
        ).order_by(
            "-occurred_at",
            "-created_at",
        )
        zero = Decimal(0)
        summary = tx.aggregate(
            income=Sum("amount", filter=Q(type=EntryType.INCOME), default=zero),
            expense=Sum("amount", filter=Q(type=EntryType.EXPENSE), default=zero),
            income_count=Count("id", filter=Q(type=EntryType.INCOME)),
            expense_count=Count("id", filter=Q(type=EntryType.EXPENSE)),
        )
        summary["balance"] = summary["income"] - summary["expense"]
        summary["balance_abs"] = abs(summary["balance"])
        summary["count"] = summary["income_count"] + summary["expense_count"]

        expense_by_category = list(
            tx.filter(type=EntryType.EXPENSE)
            .values("category")
            .annotate(total=Sum("amount"), count=Count("id"))
            .order_by("-total")
        )
        for row in expense_by_category:
            row["percent"] = (
                float(row["total"] / summary["expense"] * 100)
                if summary["expense"]
                else 0.0
            )

        return render(
            request=request,
            template_name="portal/payment_transaction.html",
            context={
                "transactions": tx,
                "summary": summary,
                "expense_by_category": expense_by_category,
            },
        )


class PaymentTransactionApiView(APIView):
    """
    Where the Penny bot writes transactions. It has no browser session, so this
    view skips login_required and authenticates with a shared token instead.
    """

    authentication_classes: ClassVar[list] = []
    permission_classes: ClassVar[list[type[HasBotApiToken]]] = [
        HasBotApiToken,
    ]

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
