from django.forms import Form
from django import forms

class AddEmpForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput)
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput)
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput)
    username = forms.CharField(label="Username", max_length=10, widget=forms.TextInput)
    password1 = forms.CharField(label="Password", max_length=12,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Retype Password", max_length=12,
                                widget=forms.PasswordInput)
    phoneNo = forms.CharField(label="Phone Number", max_length=12,
                                widget=forms.TextInput)