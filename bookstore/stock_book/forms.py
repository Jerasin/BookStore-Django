from django import forms
from . models import Book , Address , CustomUser , Author , Category , BookComments
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# Custom fields Email Require
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.utils.safestring import mark_safe
from django.forms import ImageField

   
class BookForm(forms.ModelForm):
    class Meta:
        # เลือกโมเดลที่จะใช้ทำฟอร์ม
        model = Book
        # กรองบางฟิลออก [] ในวงเล็บคือไม่เอา
        exclude = ['id', 'slug', 'created', 'updated' , 'created_by']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

        # Custom Validation input Code
        self.fields['code'].error_messages = {
            'required': 'Please enter book code',
        }
        # Custom Validation input Name
        self.fields['name'].error_messages = {
            'required': 'Please enter book name',
        }
        # Custom Validation input Price
        self.fields['price'].error_messages = {
            'required': 'Please enter book price',
            'invalid': 'Please enter a valid book price',
        }

    def clean(self):
        cd = super(BookForm, self).clean()
        if not cd.get('category'):
            self.add_error('category', 'Please select category name')

        if not cd.get('level'):
            self.add_error('level', 'Please select level')

        if not cd.get('author'):
            self.add_error('author', "Please select author name")


class CreateUserForm(UserCreationForm):    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    # function Check Email Address  is unique
    # def clean(self):
    #    email = self.cleaned_data.get('email')
    #    if User.objects.filter(email=email).exists():
    #         raise ValidationError("Email exists")
    #    return self.cleaned_data

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address']

class CreateAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = BookComments
        fields = ['comment' , 'rating']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ['password' , 'last_login' , 'date_joined']
