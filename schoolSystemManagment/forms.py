from django import forms
from .models import AdminMessage, Grade


class AdminMessageForm(forms.ModelForm):

    class Meta:
        model = AdminMessage
        fields =('messageContent',)



