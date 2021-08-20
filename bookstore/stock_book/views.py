from django.views.generic import ListView , DetailView
from django.core import paginator
from django.contrib import messages
from django.shortcuts import render, get_object_or_404 , redirect
from .models import Category, Book
from django.urls import reverse
from django.http import HttpResponseRedirect
from slugify import slugify
from .forms import BookForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
# Authentication
from django.contrib.auth import login , logout
# Create Form Authentication
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
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

def book_add(request):
    # form
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.slug = slugify(book.name)
            book.published = True
            book.save()
            form.save_m2m()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('stock_book:index', kwargs={}))
        messages.error(request, 'Save Failed')
    return render(request, 'book/add.html', {
        'form': form,
    })

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

    total_qty = 0

    # วนลูปบวกจำนวน qty
    for item in cart_items:
        total_qty = total_qty + int(item.get('qty'))

    # สร้าง session cart_qty และเก็บค่า total_qty
    request.session['cart_qty'] = total_qty
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

def cart_delete_all(request):
    cart_items = []
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('stock_book:cart_list' , kwargs={}))



def edit_qty(request):
    queryDict_to_Dict = dict(request.POST.lists())
    cart_items = request.session['cart_items'] or []
    for item in range(len(queryDict_to_Dict['slug'])):
        # print(queryDict_to_Dict['slug'][item])
        # print(queryDict_to_Dict['qty'][item])
        for index in range(len(cart_items)):
        # print(cart_items[index]['slug'])
        # print(reqSlug)
            if cart_items[index]['slug'] == queryDict_to_Dict['slug'][item]:
                cart_items[index]['qty'] = queryDict_to_Dict['qty'][item]
                break
    request.session['cart_items'] = cart_items
    
    return HttpResponseRedirect(reverse('stock_book:cart_list' , kwargs={} ))


def login_view(request):
    if request.method == "POST":
        # เอาข้อมูลที่ส่งมาหลังจาก user กด submit
        form = AuthenticationForm(data=request.POST)
        # ตรวจสอบว่ามีข้อมูลไหม
        if form.is_valid():
            # get ข้อมูลที่กรอกมาจาก form
            user = form.get_user()
            # เช็คว่ามีใน db ไหม
            login(request, user)
            # return HttpResponseRedirect(reverse('book:index'))
            # หรือใช้ 
            print('Login')
            return redirect('stock_book:index')
    else:
        # สร้าง form login
        form =AuthenticationForm()
    return render(request , 'account/login.html' , {
            'form': form,
    })

def logout_view(request):
        if request.method == 'POST':
            logout(request)
            print('Logout')
            return redirect('stock_book:index')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('stock_book:index')
    else:
        form = UserCreationForm()
    return render(request , 'account/signup.html', {
        'form': form,
    })

def create_salesorder(request):
    cart_items = request.session['cart_items'] or []
    print(cart_items)
    return redirect('stock_book:cart_list')







