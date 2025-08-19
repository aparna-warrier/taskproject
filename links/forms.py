from django import forms
from .models import ShortURL

class ShortenForm(forms.Form):
    original_url = forms.URLField(
        label='Long URL',
        widget=forms.URLInput(attrs={'placeholder': 'https://example.com/some/very/long/url'})
    )
    custom_code = forms.CharField(
        label='Custom short code (optional)',
        required=False,
        min_length=4,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. my-link'})
    )

    def clean_custom_code(self):
        code = self.cleaned_data.get('custom_code', '').strip()
        if code:
            # only allow letters, numbers, hyphen & underscore
            import re
            if not re.fullmatch(r'[A-Za-z0-9_-]+', code):
                raise forms.ValidationError("Use only letters, numbers, - and _")
            if ShortURL.objects.filter(short_code=code).exists():
                raise forms.ValidationError("This short code is taken. Try another.")
        return code
