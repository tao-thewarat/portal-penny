from django.urls import path

from .views.payment_transaction import PaymentTransaction

urlpatterns = [
    path(
        route="transactions/",
        view=PaymentTransaction.as_view(),
        name="transactions",
    ),
]
