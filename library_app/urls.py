from django.contrib import admin
from django.urls import path,include

from library_app import views



urlpatterns = [
    path('',views.index,name='index'),
     path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('registration/',views.registration,name='registration'),
    path('register/',views.register,name='register'),
    path('member_login/',views.member_login,name='member_login'),
    path('search/',views.search,name='search'),

    path('login/',views.login,name='login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('user_home/',views.user_home,name='user_home'),
    path('logout/',views.logout,name='logout'),
    path('member_profile/',views.member_profile,name='member_profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('add_book/',views.add_book,name='add_book'),
    path('edit_book/<int:book_id>/',views.edit_book,name='edit_book'),
    path('add_category/',views.add_category,name='add_category'),

    path('book_list_all/',views.book_list_all,name='book_list_all'),
    path('delete_book/<int:book_id>/',views.delete_book,name='delete_book'),

    path('book_list/<int:book_id>/',views.book_list,name='book_list'),
    path('request_book/<int:book_id>/', views.request_book, name='request_book'),
    path('book_list_student/<int:book_id>/', views.book_list_student, name='book_list_student'),
    path('all_requested_books/',views.all_requested_books,name='all_requested_books'),
    path('cancelled_requests/',views. cancelled_requests, name='cancelled_requests'),

    path('proceed_request/<int:request_id>/', views.proceed_request, name='proceed_request'),
    path('cancel_book/<int:request_id>/',views.cancel_book,name='cancel_book'),
    path('issued_books/',views.issued_books,name='issued_books'),
    path('returned_books/',views.returned_books,name='returned_books'),
    path('return_book/<int:issued_book_id>/',views.return_book,name='return_book'),
    path('returned_books_admin/',views.returned_books_admin,name='returned_books_admin'),
    path('add_penalty/<int:return_id>/', views.add_penalty, name='add_penalty'),

    path('category_list/',views.category_list,name='category_list'),    
    path('category_books/<int:category_id>/',views.category_books,name='category_books'),
    path('search_books_student/',views.search_books_student,name='search_books_student'),
    path('cancel_return/<int:return_id>/', views.cancel_return, name='cancel_return'),
    path('proceed_return/<int:return_id>/', views.proceed_return, name='proceed_return'),
    path('show_members/',views.show_members,name='show_members'),

    path('delete_member/<int:member_id>/',views.delete_member,name='delete_member'),
    path('penalty_list/',views.penalty_list,name='penalty_list'),

 




    
]