from rest_framework.viewsets import ModelViewSet
from store.serializers import BooksSerializer
from store.models import Book


class BooksViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
