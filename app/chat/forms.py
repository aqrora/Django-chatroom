from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=32)

class MessageForm(forms.Form):
    message_text = forms.CharField(max_length=255)
