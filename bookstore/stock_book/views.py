from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Category , Book
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.


class Index(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'
    paginate_by = 8

    def get_queryset(self):
        # เอาไว้ log ดู attibutes ของ class ทั้งหมด
        # print(dir(self))

        categoried_id = self.request.GET.get('categoryid')

        # print(categoried_id)
        if categoried_id:
           return Book.objects.filter(published=True, category=categoried_id)
        else:
            return Book.objects.filter(published=True)

    def get_context_data(self, *args, **kwargs):
        cd = super(Index, self). get_context_data(*args, **kwargs)
        categoried_id = self.request.GET.get('categoryid')
        cd.update({
            'categories': Category.objects.all(),
            'categoried_id': categoried_id
        })
       

        return cd

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/detail.html'
    slug_url_kwarg = 'slug'

def cart_add(request,slug):
    # query ข้อมูลที่ Model ที่ชื่อ Book โดย where จาก slug
    book = get_object_or_404(Book,slug=slug)
    print(book)
    # ดึงค่า seesion จาก key = 'cart_items' ถ้าไม่มีค่าให้ส่งเป็น [] แทน
    cart_items = request.session.get('cart_items') or []
    
    # update item
    duplicated = False
    for item in cart_items:
        if item.get('slug') == book.slug:
            item['qty'] = int(item.get('qty') or '1') + 1
            duplicated = True

    # insert new item
    if not duplicated:
        cart_items.append({
            'id': book.id,
            'slug': book.slug,
            'code': book.code,
            'name': book.name,
            'price': book.price,
            'qty': 1,
        })

    request.session['cart_items'] = cart_items

    # ไปเรียก function cart_list อิ้ง path จาก urls.py
    return HttpResponseRedirect(reverse('stock_book:index', kwargs={}))

def cart_list(request):
    # เอาค่า session มาเก็บไว้ที่ตัวแปร cart_items ถ้าไม่มีค่าให้ใส่เป็น []
    cart_items = request.session.get('cart_items') or []
    total_qty = 0

    # วนลูปบวกจำนวน qty
    for item in cart_items:
        total_qty = total_qty + int(item.get('qty'))

    # สร้าง session cart_qty และเก็บค่า total_qty
    request.session['cart_qty'] = total_qty
    return render(request , 'book/cart.html' , {
        'cart_items': cart_items,
    })

def cart_delete(request,slug):
    cart_items = request.session.get('cart_items') or []
    for item in range(len(cart_items)):
        if cart_items[item]['slug'] == slug:
            del cart_items[item]
            break
    
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('stock_book:cart_list' , kwargs={}))

def edit_qty(request):
    reqQty = request.POST.get("qty")
    reqSlug = request.POST.get("slug")
    print(reqQty , reqSlug )
    cart_items = request.session['cart_items'] or []
    for index in range(len(cart_items)):
        print(cart_items[index]['slug'])
        print(reqSlug)
        if cart_items[index]['slug'] == reqSlug:
            cart_items[index]['qty'] = reqQty
            break
    request.session['cart_items'] = cart_items
    print(cart_items)
    return HttpResponseRedirect(reverse('stock_book:cart_list' , kwargs={} ))







