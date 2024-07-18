from django.urls import path
from .views import (
    BookCreateView,
    BooksList,
    BooksInStockList,
    BookOneList,
    MyBooksList,
    MyBooksInStockList,
    MyBooksIssuedList,
    UpdateMyBook,
    BookDeleteView,
    BookSearchView,


)

urlpatterns = [
    path("create_book/", BookCreateView.as_view(), name="create_book"),
    path("books/", BooksList.as_view(), name="books"),
    path("books_in_stock/", BooksInStockList.as_view(), name="books_in_stock"),
    path("single_book/<int:pk>/", BookOneList.as_view(), name="single_book"),
    path("my_books/", MyBooksList.as_view(), name="posts_list"),
    path("my_books_in_stock/", MyBooksInStockList.as_view(), name="my_books_in_stock"),
    path(
        "my_boks_issued/",
        MyBooksIssuedList.as_view(),
        name="my_boks_issued",
    ),
    path("update_my_book/<int:pk>/", UpdateMyBook.as_view(), name="update_my_book"),
    path("book_delete/<int:pk>/", BookDeleteView.as_view(), name="delete_book"),
    path('search/', BookSearchView.as_view(), name='search'),
]