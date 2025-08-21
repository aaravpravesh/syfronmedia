from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["your_html_code", "your_css_code"]
        widgets = {
            "your_html_code": forms.Textarea(attrs={
                "rows": 12,
                "class": "form-control font-monospace border-0 rounded-bottom-4",
                "placeholder": "Write your HTML here..."
            }),
            "your_css_code": forms.Textarea(attrs={
                "rows": 12,
                "class": "form-control font-monospace border-0 rounded-bottom-4",
                "placeholder": "Write your CSS here..."
            }),
        }


from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 5, 'placeholder': 'Your Message'}),
        }
