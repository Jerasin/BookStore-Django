from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
# Create your models here.

# Global Variable
running_id = 1;

BOOK_LEVEL_CHOICE = (
    ('B', 'Basic'),
    ('M', 'Medium'),
    ('A', 'Advance'),

)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    created = models.DateField(auto_now_add=True) 

class Address(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    address = models.TextField()
    created = models.DateField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

class Category(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now=True)

    # class Meta ไว้สำหรับเพิ่ม option
    # Verbosename คือ การตั้งชื่อให้กับตัวโมเดลที่แสดงผลภายในเมื่อจัดการข้อมูล
    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Author'

    def __str__(self):
        return self.name



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    global running_id;
    date_now_from = "upload/{}{}{}{}.jpg".format(year, month, day , running_id)
    running_id = running_id+1;
    return date_now_from

class Book(models.Model):
    code = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.CASCADE)
    author = models.ManyToManyField(Author, blank=True)
    description = models.TextField(null=True, blank=True)
    level = models.CharField(max_length=5, blank=True,
                             null=True, choices=BOOK_LEVEL_CHOICE)
    price = models.FloatField(default=0)
    published = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    image = models.FileField(upload_to=user_directory_path , blank=True, null=True)

    class Meta:
        # ถ้าใช้ติดลบจะแสดงผลแบบเรียงจากมากไปน้อย
        # ถ้าใช้ไม่ติดลบจะแสดงผลแบบเรียงจากน้อยไปมาก
        ordering = ['-created']
        verbose_name_plural = 'Book'

    def show_image(self):
        if self.image:
            # print(self.image.url)
            return format_html('<img src="' + self.image.url + '" height="50px">')
        return ''

    def get_comment_count(self):
        return self.bookcomments_set.count()

    show_image.allow_tags = True
    # ใส่หรือไม่ใส่ก็ได้
    show_image.short_description = 'Image'

    def __str__(self):
        return self.name
    
class BookComments(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)    
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # ถ้าใช้ติดลบจะแสดงผลแบบเรียงจากมากไปน้อย
        # ถ้าใช้ไม่ติดลบจะแสดงผลแบบเรียงจากน้อยไปมาก
        # Django Auto created id
        ordering = ['id']
        verbose_name_plural = 'Book Comment'

    def __str__(self):
        return self.comment

class SalesOrderList(models.Model):
    saleorder_code = models.IntegerField(unique=True)
    grand_total = models.FloatField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    saleorder_status = models.CharField(max_length=100 , default='wait')
    address = models.TextField()

class SalesOrder(models.Model):
    saleorder_code = models.ForeignKey(SalesOrderList , to_field='saleorder_code', on_delete=models.CASCADE , verbose_name='saleorder_code',)
    product_code = models.CharField(max_length=10)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_qty = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    address = models.TextField()

