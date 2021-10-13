from django import forms
from django.forms import CheckboxInput

from .models import Question

class QuizForm(forms.ModelForm):
    """
    Model form for quiz
    """
    class Meta:
        model = Question
        fields = ['question_text']

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass