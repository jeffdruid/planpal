from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_email(email)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already taken.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")

        return cleaned_data


class ProfilePictureForm(forms.ModelForm):
    PROFILE_PICTURE_CHOICES = [
        # ("default.png", "Default"),
        ("p1.png", "Profile 1"),
        ("p2.png", "Profile 2"),
        ("p3.png", "Profile 3"),
        ("p4.png", "Profile 4"),
        ("p5.png", "Profile 5"),
        ("p6.png", "Profile 6"),
        ("p7.png", "Profile 7"),
        ("p8.png", "Profile 8"),
        ("p9.png", "Profile 9"),
        ("p10.png", "Profile 10"),
        ("p11.png", "Profile 11"),
        ("p12.png", "Profile 12"),
    ]
    profile_picture = forms.ChoiceField(
        choices=PROFILE_PICTURE_CHOICES, widget=forms.RadioSelect
    )

    class Meta:
        model = UserProfile
        fields = ["profile_picture"]


class FriendSearchForm(forms.Form):
    # commented out for testing purposes
    search_query = forms.CharField(max_length=100, label="", required=False)
    # user = forms.ModelChoiceField(
    #     queryset=User.objects.all(), label="Select User", required=False
    # )
