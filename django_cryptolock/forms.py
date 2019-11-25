from django import forms


class SimpleSignUpForm(forms.Form):
    username = forms.CharField()
    challenge = forms.CharField()
    address = forms.CharField()
    signature = forms.CharField()
