
from django_countries.fields import CountryField
from django import forms
from .models import Contact, Lead, Prospect, Customer
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django_countries.widgets import CountrySelectWidget
from django.core.validators import MaxValueValidator, MinValueValidator


class LeadCreateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('first_name', 'last_name', 'age', 'email', 'phone_number',
                  'address', 'country', 'profile_picture')
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial='IN'),

        }


class ProspectCreateForm(forms.ModelForm):
    score = forms.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)])

    class Meta:
        model = Prospect
        fields = ('first_name', 'last_name', 'age', 'email', 'phone_number',
                  'address', 'country', 'score', 'profile_picture')
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial='IN'),

        }


class CustomerCreateForm(forms.ModelForm):
    score = forms.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)])

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'age', 'email', 'phone_number',
                  'address', 'country', 'score', 'profile_picture')
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial='IN'),

        }


class LeadPromoteForm(forms.Form):
    score = forms.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)])
