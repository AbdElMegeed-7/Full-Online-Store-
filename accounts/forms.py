from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter PassWord',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm PassWord',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'phone_number', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Your PhoneNumber'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
