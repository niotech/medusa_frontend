from django import forms
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, max_length=500)  # Limit to 500 characters


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            raise ValidationError("Username cannot be an email address.")
        return username

# class SignInForm(forms.Form):
#     email = forms.EmailField(max_length=30, required=True, label='Email')
#     password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Password')
class SignInForm(forms.Form):
    email = forms.CharField(max_length=150, required=True, label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Password')

    def clean_email(self):
        email_or_username = self.cleaned_data.get('email')

        # Check if the input contains an '@' symbol
        if '@' not in email_or_username:
            # Assume it's a username and append @tg.com
            email_or_username = f"{email_or_username}@tg.com"

        # Validate that the result is a valid email address
        try:
            forms.EmailField().clean(email_or_username)
        except ValidationError:
            raise ValidationError("Please enter a valid email or username.")
        
        return email_or_username

class NewPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='New Password')
