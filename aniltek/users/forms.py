from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    FIRST_NAME_CHOICES = [
        ('Company', 'Company'),
        ('Employee', 'Employee'),
    ]

    first_name = forms.ChoiceField(choices=FIRST_NAME_CHOICES, label="Choose an option")
    class Meta :
        model = User
        fields = ['first_name' , 'email' , 'username' , 'password1' , 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

    
