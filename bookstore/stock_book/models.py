from django.db import models
from django.utils.html import format_html
# Create your models here.

BOOK_LEVEL_CHOICE = (
    ('B', 'Basic'),
    ('M', 'Medium'),
    ('A', 'Advance'),
)


class Category(models.Model):
    name = models.CharField(max_length=100)

    # class Meta ไว้สำหรับเพิ่ม option
    # Verbosename คือ การตั้งชื่อให้กับตัวโมเดลที่แสดงผลภายในเมื่อจัดการข้อมูล
    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Author'

    def __str__(self):
        return self.name


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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='upload', blank=True, null=True)

    class Meta:
        # ถ้าใช้ติดลบจะแสดงผลแบบเรียงจากมากไปน้อย
        # ถ้าใช้ไม่ติดลบจะแสดงผลแบบเรียงจากน้อยไปมาก
        ordering = ['-created']
        verbose_name_plural = 'Book'

    def show_image(self):
        if self.image:
            print(self.image.url)
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
    comment = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)

    class Meta:
        # ถ้าใช้ติดลบจะแสดงผลแบบเรียงจากมากไปน้อย
        # ถ้าใช้ไม่ติดลบจะแสดงผลแบบเรียงจากน้อยไปมาก
        # Django Auto created id
        ordering = ['id']
        verbose_name_plural = 'Book Comment'

    def __str__(self):
        return self.comment

class SalesOrder(models.Model):
    saleorder_code = models.IntegerField(blank=True , null=True , unique=True)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField(blank=True , null=True )
    product_qty = models.IntegerField(blank=True , null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)
    saleorder_status = models.CharField(max_length=100 , blank=True , null=True )
