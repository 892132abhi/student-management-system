from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from datetime import date
from django import forms
class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email",'profile_pic','date_of_birth')  
        
        widgets={
            'date_of_birth':forms.DateInput(attrs={'type':'date','max':date.today().isoformat()})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ""
class StudentEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'course', 'date_of_birth', 'profile_pic']