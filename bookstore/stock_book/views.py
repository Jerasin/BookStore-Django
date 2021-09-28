# import buildin class Model method
from django.db.models.base import Model

# import buildin class View method
from django.views.generic import ListView, DetailView

# import buildin  function  paginator
from django.core import paginator

# import buildin  function  messages
from django.contrib import messages

# import buildin class function  paginator
from django.shortcuts import render, get_object_or_404, redirect

# import Models from models.py
from .models import Category, Book, SalesOrder, SalesOrderList, Address, CustomUser, BookComments, Author

# import buildin  function  urls
from django.urls import reverse

# import buildin  function  http
from django.http import HttpResponseRedirect

# import buildin  function  slugify
from slugify import slugify

# import Forms from forms.py
from .forms import BookForm, CreateUserForm, AddressForm, CreateAuthorForm, CreateCategoryForm, CreateCommentForm, CustomUserForm

# import buildin class  Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# import buildin class  Email
from django.core.mail import EmailMessage

# import buildin function  login and logout
from django.contrib.auth import login, logout
# Create Form Authentication
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from calendar import HTMLCalendar
from datetime import datetime

from django.views.generic.list import MultipleObjectMixin

from django.db.models import Sum

import os
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


class BookView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'
    paginate_by = 8

    def get_queryset(self):

        book = Book.objects.all()
        return book

    def get_context_data(self, *args, **kwargs):
        cd = super(BookView, self). get_context_data(*args, **kwargs)
        return cd


class UserView(ListView):
    model = CustomUser
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    paginate_by = 8

    def get_queryset(self):

        book = CustomUser.objects.all()
        return book

    def get_context_data(self, *args, **kwargs):
        cd = super(UserView, self). get_context_data(*args, **kwargs)
        return cd


def user_delete(request, pk):
    user_delete = CustomUser.objects.get(id=pk)
    user_delete.delete()
    messages.success(request, 'Delete Success')
    return HttpResponseRedirect(reverse('stock_book:users_list', kwargs={}))


def user_update(request, pk):
    session = CustomUser.objects.get(id=pk)
    if request.method == 'GET':
        form = CustomUserForm(instance=session)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
        # form.save_m2m()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('stock_book:users_list', kwargs={}))
    return render(request, 'users/user_edit.html', {
        'form': form,
    })


class BookDetailView(DetailView, MultipleObjectMixin):
    model = Book
    template_name = 'book/detail.html'
    slug_url_kwarg = 'slug'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        object_list = BookComments.objects.filter(book_id=self.object.pk)
        context = super(BookDetailView, self).get_context_data(
            object_list=object_list, **kwargs)
        return context


class AuthorView(ListView):
    model = Author
    template_name = 'book/author_list.html'
    context_object_name = 'authors'
    paginate_by = 8

    def get_queryset(self):

        author = Author.objects.all()
        return author

    def get_context_data(self, *args, **kwargs):
        cd = super(AuthorView, self). get_context_data(*args, **kwargs)
        return cd


def author_add(request):
    # form
    form = CreateAuthorForm()

    if request.method == 'POST':
        form = CreateAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('stock_book:author_list', kwargs={}))
        messages.error(request, 'Save Failed')
    return render(request, 'book/author_form.html', {
        'form': form,
    })


def author_delete(request, pk):
    author_delete = Author.objects.get(id=pk)
    author_delete.delete()
    messages.success(request, 'Delete Success')
    return HttpResponseRedirect(reverse('stock_book:author_list', kwargs={}))


class CategoryView(ListView):
    model = Category
    template_name = 'book/category_list.html'
    context_object_name = 'categories'
    paginate_by = 8

    def get_queryset(self):

        category = Category.objects.all()
        return category

    def get_context_data(self, *args, **kwargs):
        cd = super(CategoryView, self). get_context_data(*args, **kwargs)
        return cd


def category_add(request):
    # form
    form = CreateCategoryForm()

    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('stock_book:category_list', kwargs={}))
        messages.error(request, 'Save Failed')
    return render(request, 'book/category_form.html', {
        'form': form,
    })


def category_delete(request, pk):
    category_delete = Category.objects.get(id=pk)
    category_delete.delete()
    messages.success(request, 'Delete Success')
    return HttpResponseRedirect(reverse('stock_book:category_list', kwargs={}))


def book_add(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by_id = request.user.id
            book.slug = slugify(book.name)
            book.published = True
            book.save()
            form.save_m2m()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('stock_book:index', kwargs={}))
    return render(request, 'book/add.html', {
        'form': form,
    })


def book_update(request, pk):
    session = Book.objects.get(id=pk)
    imageUrl = ''
    imageDeletePath = ''
    if session.image:
        imageDeletePath = session.image.path
        imageUrl = "/media/{}".format(session.image)
    if request.method == 'GET':
        form = BookForm(instance=session)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=session)
        if form.is_valid():
            if request.FILES and imageDeletePath:
                os.remove(imageDeletePath)
            # book.created_by_id = request.user.id
            # book.slug = slugify(book.name)
            # book.published = True
            form.save()
            # form.save_m2m()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('stock_book:index', kwargs={}))
        messages.error(request, 'Save Failed')
    return render(request, 'book/add.html', {
        'form': form,
        'imageUrl': imageUrl,

    })


def book_delete(request, pk):
    book_delete = Book.objects.get(id=pk)
    if book_delete.image:
        book_delete.delete()
        os.remove(book_delete.image.path)
    else:
        book_delete.delete()
    messages.success(request, 'Delete Success')
    return HttpResponseRedirect(reverse('stock_book:book_list', kwargs={}))


def comment_add(request, slug):
    # form
    form = CreateCommentForm()

    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            book_id = Book.objects.get(slug=slug).id
            comment.book_id = book_id
            comment.users_id = request.user.id
            comment.save()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('stock_book:index', kwargs={}))
        messages.error(request, 'Save Failed')
    return render(request, 'book/comment_form.html', {
        'form': form,
    })


def cart_add(request, slug):
    # query ข้อมูลที่ Model ที่ชื่อ Book โดย where จาก slug
    book = get_object_or_404(Book, slug=slug)
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


class CartListView(ListView):
    template_name = 'book/cart.html'
    context_object_name = 'cart_items'
    paginate_by = 5

    def get_queryset(self):
        # เอาไว้ log ดู attibutes ของ class ทั้งหมด
        # print(dir(self))
        cart_items = self.request.session.get('cart_items') or []
        total_qty = 0

        # วนลูปบวกจำนวน qty
        for item in cart_items:
            total_qty = total_qty + int(item.get('qty'))

        # สร้าง session cart_qty และเก็บค่า total_qty
        self.request.session['cart_qty'] = total_qty
        return cart_items

    def get_context_data(self, *args, **kwargs):
        cd = super(CartListView, self). get_context_data(*args, **kwargs)
        return cd


def cart_delete(request, slug):
    cart_items = request.session.get('cart_items') or []
    for item in range(len(cart_items)):
        if cart_items[item]['slug'] == slug:
            del cart_items[item]
            break

    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('stock_book:cart_list', kwargs={}))


def cart_delete_all(request):
    cart_items = []
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('stock_book:cart_list', kwargs={}))


def edit_address(request, username):
    try:
        get_user_id = CustomUser.objects.get(username=username)
        get_address = Address.objects.get(user_id=get_user_id)
        cart_items = request.session.get('cart_items') or []
        total_qty = 0
        total_price = 0
    except:
        get_user_id = CustomUser.objects.get(username=username)
        get_address = ''
        cart_items = request.session.get('cart_items') or []
        total_qty = 0
        total_price = 0
    for item in cart_items:
        # print(item['qty'])
        total_qty = int(total_qty) + int(item['qty'])
        total_price = float(total_price) + \
            (float(item['price']) * int(item.get('qty')))
    # print('total_qty',total_qty)
    # print('total_price',total_price)
    # print('saleorder_code_running',saleorder_code_running)
    return render(request, 'book/address.html', {
        'get_address': get_address,
        'saleorder_code_running': saleorder_code_running,
        'total_qty': total_qty,
        'total_price': total_price,
    })


def updated_address(request):
    if request.method == "POST":
        username = request.user
        if request.POST.get('address'):
            Address.objects.filter(user_id=request.user.id).update(
                address=request.POST.get('address'))
            messages.success(request, 'Update Address Success')
        else:
            messages.error(request, 'Save Failed')
        url = reverse('stock_book:edit_address', kwargs={'username': username})
        return HttpResponseRedirect(url)


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

    return HttpResponseRedirect(reverse('stock_book:cart_list', kwargs={}))


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
            return redirect('stock_book:index')
    else:
        # สร้าง form login
        form = AuthenticationForm()
    return render(request, 'account/login.html', {
        'form': form,
    })


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('stock_book:index')


def signup_view(request):
    if request.method == 'POST':
        users_form = CreateUserForm(request.POST)
        address_form = AddressForm(request.POST)
        get_username = request.POST.get('username')
        get_address = request.POST.get('address')
        if users_form.is_valid() and get_address:
            user = users_form.save()
            # หาค่า id จาก username
            # sql statement = SELECT id FROM CustomUser WHERE username = 'get_username'
            get_id = CustomUser.objects.get(username=get_username).id
            created_address = Address(user_id=get_id, address=get_address)
            address = created_address.save()
            login(request, user)
            return redirect('stock_book:index')
    else:
        users_form = CreateUserForm()
        address_form = AddressForm()
    return render(request, 'account/signup.html', {
        'users_form': users_form,
        'address_form': address_form
    })


saleorder_code_running = 1006


def create_salesorder(request, user_id):
    grand_total = 0
    global saleorder_code_running
    cart_items = request.session['cart_items'] or []
    address = Address.objects.get(user_id=user_id)
    try:
        salesorder_list_save = SalesOrderList.objects.create(
            saleorder_code=saleorder_code_running,
            grand_total=grand_total,
            created_by_id=user_id,
            address=address
        )
        for value in cart_items:
            sum_price = float(value['price']) * float(value['qty'])
            grand_total += sum_price
            salesorder_save = SalesOrder.objects.create(saleorder_code_id=saleorder_code_running,
                                                        product_code=value['code'],
                                                        product_name=value['name'],
                                                        product_price=value['price'],
                                                        product_qty=value['qty'],
                                                        created_by_id=user_id,
                                                        address=address,
                                                        )
        SalesOrderList.objects.filter(
            saleorder_code=saleorder_code_running).update(grand_total=grand_total, )
        saleorder_code_running += 1
        # print(saleorder_code_running)

        # Reset Session
        request.session['cart_items'] = []
        request.session['cart_qty'] = []

        return redirect('stock_book:index')
    except Exception as e:
        # print(saleorder_code_running)
        current_saleorder_code_running = saleorder_code_running
        while saleorder_code_running <= current_saleorder_code_running:
            saleorder_code_running += 1
        return create_salesorder(request, user_id)


class HistoryListView(ListView):
    template_name = 'book/history.html'
    context_object_name = 'history'
    paginate_by = 5

    def get_queryset(self):
        # เอาไว้ log ดู attibutes ของ class ทั้งหมด
        # print(dir(self))
        # เช็คว่าเป็น Super CustomUser รึป่าว
        # print(self.request.user.is_superuser)
        checkSuperUser = self.request.user.is_superuser

        if checkSuperUser:
            history = SalesOrderList.objects.all()
        else:
            get_user_id = CustomUser.objects.get(username=self.request.user)
            history = SalesOrderList.objects.filter(
                created_by_id=get_user_id).all()
        return history

    def get_context_data(self, *args, **kwargs):
        cd = super(HistoryListView, self). get_context_data(*args, **kwargs)
        return cd


class DetailOrderListView(ListView):
    Model = SalesOrder
    template_name = 'book/detail_salesorder.html'
    context_object_name = 'detail'
    paginate_by = 5
    ordering = ['product_price']

    def get_queryset(self):
        # เอาไว้ log ดู attibutes ของ class ทั้งหมด
        saleorder_code = self.kwargs['salesorder']
        return SalesOrder.objects.filter(saleorder_code_id=saleorder_code)

    def get_context_data(self, *args, **kwargs):
        cd = super(DetailOrderListView,
                   self). get_context_data(*args, **kwargs)
        saleorder_code = self.kwargs['salesorder']

        cd.update({
            'saleorder_code': saleorder_code,
        })
        return cd


class DetailSalesOrderListView(ListView):
    Model = SalesOrder
    template_name = 'book/salesorder.html'
    context_object_name = 'detail'
    paginate_by = 5
    ordering = ['product_price']

    def get_queryset(self):
        # เอาไว้ log ดู attibutes ของ class ทั้งหมด
        saleorder_code = self.kwargs['salesorder']
        return SalesOrder.objects.filter(saleorder_code_id=saleorder_code)

    def get_context_data(self, *args, **kwargs):
        cd = super(DetailSalesOrderListView,
                   self). get_context_data(*args, **kwargs)
        saleorder_code = self.kwargs['salesorder']
        saleorder_status = SalesOrderList.objects.filter(
            saleorder_code=saleorder_code)
        for item in saleorder_status:
            if item.saleorder_status == 'wait':
                saleorder_status = False
            else:
                saleorder_status = True
        cd.update({
            'saleorder_code': saleorder_code,
            'saleorder_status': saleorder_status
        })
        return cd


def set_approve(request, salesorder):
    SalesOrderList.objects.filter(
        saleorder_code=salesorder).update(saleorder_status='approve')
    return redirect('stock_book:dashboard_page')


def set_reject(request, salesorder):
    SalesOrderList.objects.filter(
        saleorder_code=salesorder).update(saleorder_status='reject')
    return redirect('stock_book:dashboard_page')


class DashBoardView(ListView):
    Model = SalesOrderList
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'salesorder_list'
    paginate_by = 5

    def get_queryset(self):
        # เอาไว้ log ดู attibutes ของ class ทั้งหมด
        salesorder_list = ''
        return salesorder_list

    def get_context_data(self, *args, **kwargs):
        cd = super(DashBoardView, self). get_context_data(*args, **kwargs)
        count_customers = CustomUser.objects.all().count()
        count_orders_approve = SalesOrderList.objects.filter(
            saleorder_status='approve').all().count()
        count_orders_wait = SalesOrderList.objects.filter(
            saleorder_status='wait').all().count()
        count_orders_reject = SalesOrderList.objects.filter(
            saleorder_status='reject').all().count()

        grand_total = {'grand_total__sum': 0}
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        date_now_from = "{}-{}-{}".format(year, month, day)
        date_now_to = "{}-{}-{}".format(year, month, day)
        cd.update({
            'count_customers': count_customers,
            'count_orders_approve': count_orders_approve,
            'count_orders_wait': count_orders_wait,
            'count_orders_reject': count_orders_reject,
            'date_now_from': date_now_from,
            'date_now_to': date_now_to,
            'grand_total': grand_total,
        })
        return cd


class SearchDetailView(ListView):
    Model = SalesOrderList
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'salesorder_list'
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):

        current_date_from = self.request.POST.get('date_from')
        current_date_to = self.request.POST.get('date_to')
        customer_name = self.request.POST.get('customer_name')
        salesorder_code = self.request.POST.get('salesorder_code')

        if current_date_from and current_date_to and customer_name and salesorder_code:
            user_id = CustomUser.objects.get(username=customer_name).id
            salesorder_list = SalesOrderList.objects.filter(created__range=[
                                                            current_date_from, current_date_to], created_by_id=user_id, saleorder_code=salesorder_code).all()
        elif current_date_from and current_date_to and customer_name:
            user_id = CustomUser.objects.get(username=customer_name).id
            salesorder_list = SalesOrderList.objects.filter(
                created__range=[current_date_from, current_date_to], created_by_id=user_id).all()
        elif current_date_from and current_date_to and salesorder_code:
            user_id = CustomUser.objects.get(username=customer_name).id
            salesorder_list = SalesOrderList.objects.filter(created__range=[
                                                            current_date_from, current_date_to], saleorder_code=salesorder_code).all()
        else:
            salesorder_list = SalesOrderList.objects.filter(
                created__range=[current_date_from, current_date_to]).all()
        return salesorder_list

    def get_context_data(self, *args, **kwargs):
        cd = super(SearchDetailView, self). get_context_data(*args, **kwargs)
        count_customers = CustomUser.objects.all().count()
        count_orders_approve = SalesOrderList.objects.filter(
            saleorder_status='approve').all().count()
        count_orders_wait = SalesOrderList.objects.filter(
            saleorder_status='wait').all().count()
        count_orders_reject = SalesOrderList.objects.filter(
            saleorder_status='reject').all().count()

        current_date_from = self.request.POST.get('date_from')
        current_date_to = self.request.POST.get('date_to')

        current_date_from = self.request.POST.get('date_from')
        current_date_to = self.request.POST.get('date_to')
        customer_name = self.request.POST.get('customer_name')
        salesorder_code = self.request.POST.get('salesorder_code')

        if current_date_from and current_date_to and customer_name and salesorder_code:
            user_id = CustomUser.objects.get(username=customer_name).id
            grand_total = SalesOrderList.objects.filter(created__range=[
                                                        current_date_from, current_date_to], created_by_id=user_id, saleorder_code=salesorder_code).all().aggregate(Sum('grand_total'))
        elif current_date_from and current_date_to and customer_name:
            user_id = CustomUser.objects.get(username=customer_name).id
            grand_total = SalesOrderList.objects.filter(created__range=[
                                                        current_date_from, current_date_to], created_by_id=user_id).all().aggregate(Sum('grand_total'))
        elif current_date_from and current_date_to and salesorder_code:
            user_id = CustomUser.objects.get(username=customer_name).id
            grand_total = SalesOrderList.objects.filter(created__range=[
                                                        current_date_from, current_date_to], saleorder_code=salesorder_code).all().aggregate(Sum('grand_total'))
        else:
            grand_total = SalesOrderList.objects.filter(created__range=[
                                                        current_date_from, current_date_to]).all().aggregate(Sum('grand_total'))

        if grand_total['grand_total__sum'] == None:
            grand_total = {'grand_total__sum': 0}

        cd.update({
            'count_customers': count_customers,
            'count_orders_approve': count_orders_approve,
            'count_orders_wait': count_orders_wait,
            'count_orders_reject': count_orders_reject,
            'date_now_from': current_date_from,
            'date_now_to': current_date_to,
            'grand_total': grand_total,
        })
        return cd
