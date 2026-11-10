from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm

from .models import User


class UserAdminCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name")


class UserAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"