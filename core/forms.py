from django import forms

from .models import Comment
from .models import ContactForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['email', 'name', 'text']

        widgets = {
            "email": forms.EmailInput(),
            "name": forms.TextInput(),
            "text": forms.Textarea(attrs={"id": "message", "cols": "40", "rows": "10"})
        }


class MessageContactForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['email', 'name', 'subject', 'message']

        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email (required)"}),
            "name": forms.TextInput(attrs={"placeholder": "Name (required)"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"id": "message", "cols": "30", "rows": "10", "placeholder": "Message"})
        }
