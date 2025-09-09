from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    method = forms.ChoiceField(choices=Payment.PAYMENT_METHODS, widget=forms.RadioSelect)

    class Meta:
        model = Payment
        fields = ['method']
