from django import forms
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from .models import Venue


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    lib_id = forms.CharField(label="Library ID")
    class_name = forms.IntegerField(label="Class")
    roll_no = forms.IntegerField(label="Roll No.")
    log_pass = forms.CharField(widget=forms.PasswordInput())


class FeedBackForm(forms.Form):
    your_name = forms.CharField(label="Your Name")
    email_id = forms.EmailField(label="Email Id", required=False)
    contact_number = forms.CharField(label="Contact number", required=False, max_length=10)
    birth_date = forms.DateField(widget=forms.SelectDateWidget())
    Rating = forms.IntegerField(label="Rating", required=False)
    suggestion = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(FeedBackForm, self).__init__(*args, **kwargs)

        self.fields['your_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['suggestion'].widget.attrs['placeholder'] = 'Suggestion.....'
        self.fields['Rating'].widget.attrs['placeholder'] = '*****'
        self.fields['email_id'].widget.attrs['placeholder'] = 'abc@gmail.com'
        self.fields['contact_number'].widget.attrs['placeholder'] = 'Mobile Number'


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)

        # self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        # self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        # self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        # self.fields['contact_number'].widget.attrs['placeholder'] = 'Mobile Number'

        # Assigning class and placeholder to form element
        self.fields['first_name'] = forms.EmailField(label=_("First Name"),
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class':'first_name'}))
        self.fields['last_name'] = forms.EmailField(label=_("Last Name"),
                                                widget=forms.TextInput(
                                                    attrs={'placeholder': 'Last Name', 'class': 'last_name'}))
        self.fields['email'] = forms.EmailField(label=_("E-mail"),
                                                widget=forms.TextInput(
                                                    attrs={'placeholder': 'Your Email', 'class': 'email'}))
        self.fields['contact_number'] = forms.EmailField(label=_("Contact Number"),
                                                widget=forms.TextInput(
                                                    attrs={'placeholder': 'Contact number', 'class': 'contact_number'}))
