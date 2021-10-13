from django.urls import path
from . import views
from django.views.generic.dates import ArchiveIndexView
from .models import Author

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('get_name/', views.GetNameView.as_view(), name='name'),
    path('author/', views.AuthorListView.as_view(), name='author'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='detail_author'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('feedback/', views.feedback, name='feedback'),
    path('Dellogin/', views.Dellogin, name='Dellogin'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('add_venue/', views.FeedbackFormView.as_view(), name='add-venue'),
    path('create_auth/', views.AuthorCreateView.as_view(), name='create-auth'),
    path('update_auth/<int:pk>/', views.AuthorUpdateView.as_view(), name='update-auth'),
    path('delete_auth/<int:pk>/', views.AuthorDeleteView.as_view(), name='delete-auth'),
    path('archive/',ArchiveIndexView.as_view(model=Author, date_field="date_of_birth"),
         name="article_archive"),
]
