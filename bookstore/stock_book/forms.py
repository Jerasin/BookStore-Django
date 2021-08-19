from django import forms
from . models import Book

class BookForm(forms.ModelForm):
    class Meta:
        # เลือกโมเดลที่จะใช้ทำฟอร์ม
        model = Book
        # กรองบางฟิลออก [] ในวงเล็บคือไม่เอา
        exclude = ['id' , 'slug' ,  'published' , 'created' , 'updated']

    def __init__(self , *args, **kwargs):
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
            self.add_error('category' , 'Please select category name')

        if not cd.get('level'):
            self.add_error('level' , 'Please select level')
        
        if not cd.get('author'):
            self.add_error('author' , "Please select author name")