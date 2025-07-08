
from django.urls import path
from . import views  # importing views from the same app

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book-list'),
    path('members/', views.member_list, name='member-list'),
    path('issue/', views.issue_book, name='issue-book'),
    path('return/<int:transaction_id>/', views.return_book, name='return-book'),
    path('import/', views.import_books, name='import-books'),
]
