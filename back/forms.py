from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.utils import timezone


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserModifyForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "current_password"]

    def clean(self):
        cleaned_data = super(UserModifyForm, self).clean()
        current_password = cleaned_data.get("current_password")
        if not check_password(current_password, self.instance.password):
            self.add_error("current_password", "Your password is incorrect.")

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate."
                % (
                    self.instance._meta.object_name,
                    "created" if self.instance._state.adding else "changed",
                )
            )
        user = super(UserModifyForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user
