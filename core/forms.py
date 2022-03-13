from django import forms


class TrendyolUrlForm(forms.Form):
    url = forms.URLField(
        error_messages={
            'invalid': 'لطفا یک آدرس صحیح وارد کنید',
            'required': 'لطفا یک آدرس وارد کنید',
        },
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://www.trendyol.com/...',
            }

        )
    )
