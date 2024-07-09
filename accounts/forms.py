# accounts/forms.py
from django import forms
from .models import UserProfile


class ProfilePictureForm(forms.ModelForm):
    PROFILE_PICTURE_CHOICES = [
        ("default.png", "Default"),
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
    ]
    profile_picture = forms.ChoiceField(
        choices=PROFILE_PICTURE_CHOICES, widget=forms.RadioSelect
    )

    class Meta:
        model = UserProfile
        fields = ["profile_picture"]
