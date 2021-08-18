from django.contrib import admin
from .models import Category, Author, Book, BookComments
from django.contrib.auth.models import User
# Register your models here.


# กำหนดบรรทัดเริ่มต้นมาให้อัตโนมัติ
class BookCommentsStackedInline(admin.StackedInline):
    model = BookComments

# กำหนดบรรทัดเริ่มต้นแบบกำหนดเอง กำหนดผ่าน Extra


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
     list_display = ['email' , 'username', 'last_login', 'is_staff' , 'is_active']


admin.site.register(Category)
admin.site.register(Author)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Book,BookAdmin)
