from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name=forms.CharField(label="Full Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}),required=True)
    shipping_email=forms.CharField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}),required=True)
    shipping_address1=forms.CharField(label="Address 1", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}),required=True)
    shipping_address2=forms.CharField(label="Address 2", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}),required=False)
    shipping_city=forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),required=True)
    shipping_state=forms.CharField(label="State", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),required=False)
    shipping_zipcode=forms.CharField(label="Zipcode", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}),required=False)
    shipping_country=forms.CharField(label="Country", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),required=True)

    class Meta:
        model=ShippingAddress
        fields=['shipping_full_name','shipping_email','shipping_address1','shipping_address2','shipping_city','shipping_state','shipping_zipcode','shipping_country']

        #exclude field which is foreign key in our model,we don't want to use it in form 
        exclude=['user',]

#We will use regular form to send our data we dont want to save it in database
class PaymentForm(forms.Form):
    card_name=forms.CharField(label="Card Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Name'}),required=True)
    card_number=forms.CharField(label="Card Number", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}),required=True)
    card_exp_date=forms.CharField(label="Expiration Date", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expiration Date'}),required=True)
    card_cvv_number=forms.CharField(label="CVV Code", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Code'}),required=True)
    card_address1=forms.CharField(label="Billing Address 1", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 1'}),required=True)
    card_address2=forms.CharField(label="Billing Address 2", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 2'}),required=False)
    card_city=forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),required=True)
    card_state=forms.CharField(label="State", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),required=True)
    card_zipcode=forms.CharField(label="Zip Code", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}),required=True)
    card_country=forms.CharField(label="Country", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),required=True)
    
