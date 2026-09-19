from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "domain", "timeline", "scope", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 bg-surface-container-low rounded-xl text-sm text-on-surface placeholder:text-outline focus:outline-none focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary/20 transition-all",
                "placeholder": "Contoh: Raden Satria",
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-4 py-3 bg-surface-container-low rounded-xl text-sm text-on-surface placeholder:text-outline focus:outline-none focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary/20 transition-all",
                "placeholder": "nama@institusi.com",
            }),
            "domain": forms.RadioSelect(attrs={"class": "w-4 h-4 text-primary accent-primary"}),
            "timeline": forms.Select(attrs={
                "class": "w-full px-4 py-3 bg-surface-container-low rounded-xl text-sm text-on-surface focus:outline-none focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary/20 transition-all",
            }),
            "scope": forms.Select(attrs={
                "class": "w-full px-4 py-3 bg-surface-container-low rounded-xl text-sm text-on-surface focus:outline-none focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary/20 transition-all",
            }),
            "message": forms.Textarea(attrs={
                "class": "w-full px-4 py-3 bg-surface-container-low rounded-xl text-sm text-on-surface placeholder:text-outline focus:outline-none focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary/20 transition-all resize-y",
                "rows": 5,
                "maxlength": 1500,
                "placeholder": "Jelaskan gambaran umum proyek, tantangan teknis yang ingin diselesaikan, konteks sistem yang sudah ada, atau format sesi diskusi...",
                "oninput": "document.getElementById('char-counter').textContent = this.value.length + '/1500'",
            }),
        }
