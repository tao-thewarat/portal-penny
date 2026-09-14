from django.urls import path

from .views.payment_transaction import (
    PaymentTransactionFormView,
    PaymentTransactionView,
)

urlpatterns = [
    path(
        route="transactions/",
        view=PaymentTransactionView.as_view(),
        name="transactions",
    ),
    path(
        route="transactions/<int:pk>/",
        view=PaymentTransactionFormView.as_view(),
        name="transaction_form",
    ),
    path(
        route="api/transactions",
        view=PaymentTransactionView.as_view(),
        name="create_payment_transaction",
    ),
]
