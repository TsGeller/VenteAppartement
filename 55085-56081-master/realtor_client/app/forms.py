from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(max_length=200)


class OfferForm(forms.Form):
    price = forms.IntegerField()

    

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=200)

    