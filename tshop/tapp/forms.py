from django import forms


PAYMENT_METHOD =(
    ('S', 'Stripe'),
    ('B','Bkash')
)

class CheckoutForm(forms.Form):
    present_address = forms.CharField()
    home_address = forms.CharField()
    mobile_number = forms.IntegerField()
    payment_option =forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_METHOD)