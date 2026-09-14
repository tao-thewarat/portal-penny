from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class PaymentTransaction(View):
    
    def get(self, request):
        return render(
            request,
            "portal/payment_transaction_templates.html",
        )
