from .serializers import (
    BookSerializer,
    UpdateBookSerializer,
)
from rest_framework.views import APIView
from .models import Book
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOnlyMyBook
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from django.http import response


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        request=BookSerializer,
        responses={"201": BookSerializer, "400": {"default": "Bad request"}},
        description="Создание книги",
    )
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@extend_schema_view(get=extend_schema(description="Все книги"))
class BooksList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        books = Book.objects.all()
        return books


@extend_schema_view(get=extend_schema(description="Все книги в наличии"))
class BooksInStockList(generics.ListAPIView):
    queryset = Book.objects.filter(status='В наличии')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        books = Book.objects.filter(status='В наличии')
        return books


@extend_schema_view(get=extend_schema(description="Книга"))
class BookOneList(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        order = Book.objects.filter(pk=pk)
        serializer = BookSerializer(order, many=True)
        return Response(serializer.data)


@extend_schema_view(
    get=extend_schema(description="Все книги текущего пользователя")
)
class MyBooksList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        books = Book.objects.filter(owner=self.request.user)
        return books
    
@extend_schema_view(
    get=extend_schema(description="Все книги в наличии текущего пользователя")
)
class MyBooksInStockList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        posts = Book.objects.filter(Q(status='В наличии') & (Q(owner=self.request.user)))
        return posts


@extend_schema_view(
    get=extend_schema(
        description="Все выданные книги текущего пользователя"
    )
)
class MyBooksIssuedList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        books = Book.objects.filter(Q(status='Выдана') & (Q(owner=self.request.user)))
        return books


class UpdateMyBook(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = UpdateBookSerializer
    permission_classes = [IsAuthenticated, IsOnlyMyBook]

    @extend_schema(
        request=UpdateBookSerializer,
        responses={"201": UpdateBookSerializer, "400": {"default": "Bad request"}},
        description="Изменение статуса книги владельцем",
    )
    def change_book(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = self.serializer_class(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOnlyMyBook]

    @extend_schema(
        request=BookSerializer,
        responses={
            204: None,
            400: {"default": "Bad request"},
            404: {"default": "Not found."},
        },
        description="Удаление поста автором или администратором",
    )
    def delete_post(self, request, pk):
        post = Book.objects.filter(pk=pk)
        post.delete()
        response.data = {"message": "Успешно"}
        return response
    

class BookSearchView(APIView):
    @extend_schema(
        request=BookSerializer,
        responses={
            201: BookSerializer,
            400: {"default": []},
        },
        description="Поиск книги по номеру названию, автору или году издания по search_query" 
        " среди полей author/title/year. "
        "Пример: ?search_query=Гарри Поттер",
    )

    def get(self, request):
        search_query = request.GET.get("search_query", "")
        books = Book.objects.filter(
                Q(author__icontains=search_query)
                | Q(title__icontains=search_query)
                | Q(year__icontains=search_query)
            )
        serializer = BookSerializer (books, many=True)
        return Response(serializer.data)