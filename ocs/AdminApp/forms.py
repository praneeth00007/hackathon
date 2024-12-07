from django import forms
from .models import CustomUser  # Import your CustomUser model


class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Check if both passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return password2

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        # Set the password using the password1 field and hash it automatically
        user.password = self.cleaned_data['password1']

        if commit:
            user.save()
        return user
