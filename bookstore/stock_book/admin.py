from django.contrib import admin
from .models import Category, Author, Book, BookComments , Address , CustomUser
from django.contrib.auth.models import User
# Custom User Model
from django.conf import settings
# Register your models here.


# กำหนดบรรทัดเริ่มต้นมาให้อัตโนมัติ
class BookCommentsStackedInline(admin.StackedInline):
    model = BookComments

# กำหนดบรรทัดเริ่มต้นแบบกำหนดเอง กำหนดผ่าน Extra

class AddressStackedInline(admin.StackedInline):
    model = Address

class BookTabularInline(admin.TabularInline):
    model = BookComments
    extra = 2


class BookAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category',
                    'price', 'published', 'show_image']
    list_filter = ['published']
    search_fields = ['name', 'code']
    prepopulated_fields = {'slug': ['name']}
    fieldsets = (
        (None, {'fields': ['name', 'slug', 'code', 'description',
         'level',  'price', 'published', 'image']}),
        ('Category', {'fields': ['category',
         'author'], 'classes': ['collapse']}),
    )
    inlines = [BookTabularInline]

class UserAdmin(admin.ModelAdmin):
     model = CustomUser
     list_display = ['email' , 'username', 'last_login', 'is_superuser' , 'is_staff' , 'is_active' , 'address']
     



admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Address)
# admin.site.unregister(CustomUser)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Book,BookAdmin)
