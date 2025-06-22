from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from users.models import User, EventPlanner

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password1  = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        min_length= 8
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        min_length= 8
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number','firstname','lastname',
                  'profile_picture','user_types',)
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1']) # hash password
        if commit:
            user.save()
        return user
    
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ('username', 'email', 'phone_number','firstname','lastname',
              'profile_picture','user_types', 'password1', 'password2'),
        }),
    )

admin.site.register(User, CustomUserAdmin),
admin.site.register(EventPlanner),