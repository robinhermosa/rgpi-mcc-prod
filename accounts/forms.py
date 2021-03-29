from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django import forms
from .models import Profile
from bootstrap_modal_forms.forms import BSModalModelForm    


class UserForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    is_superuser= forms.CheckboxInput()
    is_staff= forms.CheckboxInput()
    is_active= forms.CheckboxInput()

    class Meta:
        model = User
        fields = ('username', 'email','first_name', 'last_name',  'password1', 'password2','group','is_superuser','is_staff','is_active' )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('address', 'contact_no','site','department', 'image')

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['email','first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['bio','address', 'contact_no','site','department', 'image']
