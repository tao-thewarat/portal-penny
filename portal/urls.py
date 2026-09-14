from django.urls import path

from .views.payment_transaction import PaymentTransactionView

urlpatterns = [
    path(
        route="transactions/",
        view=PaymentTransactionView.as_view(),
        name="transactions",
    ),
    path(
        route="api/transactions",
        view=PaymentTransactionView.as_view(),
        name="create_payment_transaction",
    ),
]
