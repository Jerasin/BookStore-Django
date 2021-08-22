from django.urls import path , re_path
from . import views
# Check login
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', views.Index.as_view() , name='index'),
    path('login/', views.login_view , name='login'),
    path('logout/', views.logout_view , name='logout'),
    path('signup/', views.signup_view , name='signup'),
    path('detail/<slug:slug>/', login_required(views.BookDetailView.as_view() , login_url='/login') , name='detail'),
    path('add' , login_required(views.book_add  , login_url='/login') , name='book_add'),
    re_path(r'cart/add/(?P<slug>[\w-]+)/$' , login_required(views.cart_add  , login_url='/login') , name='cart_add'),
    re_path(r'cart/delete/(?P<slug>[\w-]+)/$' , views.cart_delete , name='cart_delete'),
    path('delete_all' , views.cart_delete_all , name='cart_delete_all'),
    path('card_edit' , views.edit_qty , name='edit_qty'),
    path('cart/list/', views.CartListView.as_view() , name='cart_list'),
    path('create_salesorder/<int:user_id>', views.create_salesorder , name='create_salesorder'),
    path('show_history' , login_required(views.HistoryListView.as_view() , login_url='/login') , name='show_history'),
    path('show_detail/<int:salesorder>' , login_required(views.DetailSalesOrderListView.as_view() , login_url='/login') , name='show_detail'),
    path('set_approve/<int:salesorder>' , login_required(views.set_approve , login_url='/login') , name='set_approve')

]