from django import forms
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your email'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Enter your message', 'rows': 5
    }))
    captcha = CaptchaField()


class PaymentForm(forms.Form):
    name = forms.CharField(label="Your name")
    email = forms.EmailField(label="Your Email")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")
    captcha = CaptchaField()
    

