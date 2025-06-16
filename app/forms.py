from django import forms
from .models import Users, Events

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['username', 'firstname', 'lastname', 'email', 'phone_number', 'user_types', 'profile_picture', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = [
            'event_name', 'description', 'start_date', 'end_date',
            'venue_name', 'venue_address', 'city', 'country',
            'thumbnail', 'gallery_image_url', 'category',
            'status', 'is_featured', 'is_trending', 'planners'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
