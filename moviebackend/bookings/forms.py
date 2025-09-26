from django import forms

from bookings.views import payment

class PaymentForm(forms.ModelForm):
    customer_name = forms.CharField(
        max_length=100,
        required=True,
        label="Họ và tên",
        widget=forms.TextInput(attrs={'placeholder': 'Nhập họ và tên'})
    )
    customer_email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Nhập email'})
    )
    customer_phone = forms.CharField(
        max_length=15,
        required=True,
        label="Số điện thoại",
        widget=forms.TextInput(attrs={'placeholder': 'Nhập số điện thoại'})
    )
    method = forms.ChoiceField(
        choices=payment.PAYMENT_METHODS,
        widget=forms.RadioSelect,
        label="Phương thức thanh toán"
    )

    class Meta:
        model = payment
        fields = ['customer_name', 'customer_email', 'customer_phone', 'method']
