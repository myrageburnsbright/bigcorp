
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.forms.widgets import PasswordInput, TextInput

User = get_user_model()

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self ).__init__(*args, **kwargs)

        self.fields['email'].label = 'You email address'
        self.fields['email'].required = True
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = 'Confirm your password'

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists() and len(email) > 254:
            raise forms.ValidationError("Email already exists or too long")
        
        return email
        

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')
        exclude = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self ).__init__(*args, **kwargs)

        self.fields['email'].label = 'You email address'
        self.fields['email'].required = True

class AccountPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
