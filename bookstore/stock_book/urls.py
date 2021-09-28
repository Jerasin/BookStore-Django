from django.shortcuts import redirect
from django.urls import path , re_path
from . import views
# Check login
from django.contrib.auth.decorators import login_required

redirect_login = '/bookstore/login';

urlpatterns = [
    path('', views.Index.as_view() , name='index'),
    path('login/', views.login_view , name='login'),
    path('logout/', views.logout_view , name='logout'),
    path('signup/', views.signup_view , name='signup'),
    path('detail/<slug:slug>/', login_required(views.BookDetailView.as_view() , login_url=redirect_login) , name='detail'),

    path('book_list' , login_required(views.BookView.as_view()  , login_url=redirect_login) , name='book_list'),

    path('book_list/delete/<int:pk>' , login_required(views.book_delete  , login_url=redirect_login) , name='book_delete'),

    path('add/' , login_required(views.book_add  , login_url=redirect_login) , name='book_add'),
    path('update/<int:pk>' , login_required(views.book_update  , login_url=redirect_login) , name='book_update'),

    re_path(r'cart/add/(?P<slug>[\w-]+)/$' , login_required(views.cart_add  , login_url=redirect_login) , name='cart_add'),

    re_path(r'cart/delete/(?P<slug>[\w-]+)/$' , login_required(views.cart_delete, login_url=redirect_login) , name='cart_delete'),

    path('delete_all/' , login_required(views.cart_delete_all, login_url=redirect_login)  , name='cart_delete_all'),
    
    path('card_edit/' , login_required(views.edit_qty, login_url=redirect_login) , name='edit_qty'),

    path('edit_address/<str:username>' , login_required(views.edit_address, login_url=redirect_login) , name='edit_address'),

    path('cart_list/', login_required(views.CartListView.as_view(), login_url=redirect_login) , name='cart_list'),

    path('create_salesorder/<int:user_id>', login_required(views.create_salesorder, login_url=redirect_login) , name='create_salesorder'),

    path('show_history' , login_required(views.HistoryListView.as_view() , login_url=redirect_login) , name='show_history'),

    path('show_detail/<int:salesorder>' , login_required(views.DetailOrderListView.as_view() , login_url=redirect_login) , name='show_detail'),

    path('salesorder_detail/<int:salesorder>' , login_required(views.DetailSalesOrderListView.as_view() , login_url=redirect_login) , name='salesorder_detail'),

    path('set_approve/<int:salesorder>' , login_required(views.set_approve , login_url=redirect_login) , name='set_approve'),

    path('set_reject/<int:salesorder>' , login_required(views.set_reject , login_url=redirect_login) , name='set_reject'),

    path('dashboard_page' , login_required(views.DashBoardView.as_view() , login_url=redirect_login) , name='dashboard_page'),

    path('search_detail' , login_required(views.SearchDetailView.as_view() , login_url=redirect_login) , name='search_detail'),

    path('author_list' , login_required(views.AuthorView.as_view()  , login_url=redirect_login) , name='author_list'),

    path('author_add' , login_required(views.author_add , login_url=redirect_login) , name='author_add'),

    path('author_delete/<int:pk>' , login_required(views.author_delete , login_url=redirect_login) , name='author_delete'),

    path('category_list' , login_required(views.CategoryView.as_view()  , login_url=redirect_login) , name='category_list'),

    path('category_add' , login_required(views.category_add , login_url=redirect_login) , name='category_add'),

    path('category_delete/<int:pk>' , login_required(views.category_delete , login_url=redirect_login) , name='category_delete'),

    path('comment_add/<slug:slug>' , login_required(views.comment_add , login_url=redirect_login) , name='comment_add'),

    path('updated_address' , login_required(views.updated_address , login_url=redirect_login) , name='updated_address'),

    path('users_list' , login_required(views.UserView.as_view() , login_url=redirect_login) , name='users_list'),

    path('users_delete/<int:pk>' , login_required(views.user_delete , login_url=redirect_login) , name='users_delete'),
    
    path('user_update/<int:pk>' , login_required(views.user_update , login_url=redirect_login) , name='user_update'),

]