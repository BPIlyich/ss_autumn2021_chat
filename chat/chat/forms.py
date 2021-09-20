from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LoginForm(forms.Form):
    """
    Форма для входа в чат-комнату под выбранным ником
    """
    username = forms.CharField(label=_('Your name'), max_length=100)

    def get_or_create_user(self):
        return User.objects.get_or_create(username=self.cleaned_data['username'])[0]
