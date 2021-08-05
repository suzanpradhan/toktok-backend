from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from . import models as store_manager_models


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = store_manager_models.StoreManagerUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = store_manager_models.StoreManagerUser
        fields = ('email',)

# class CustomUserLogin(AuthenticationForm):

#     email = forms.EmailField(widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
#     password = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': '',
#             'id': 'hi',
#         }))