import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.url = reverse('book-list')
        self.book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=50, author_name='Author 2')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=55, author_name='Author 2')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        response = self.client.get(self.url, data={'price': 55})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = BooksSerializer(self.book_3).data
        self.assertEqual(serializer_data, *response.json())

    def test_get_search(self):
        response = self.client.get(self.url, data={'search': 'Author 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(Book.objects.all().count(), 3)
        data = {
            'name': 'Programming in Python 3',
            'price': 500,
            'author_name': 'Mark Summerfield',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.all().count(), 4)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id, ))
        data = {
            'name': self.book_1.name,
            'price': 228,
            'author_name': self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_1.refresh_from_db()
        self.assertEqual(228, self.book_1.price)

    def test_delete(self):
        self.assertEqual(Book.objects.all().count(), 3)
        url = reverse('book-detail', args=(self.book_1.id, ))
        data = {
            'name': self.book_1.name,
            'price': self.book_1.price,
            'author_name': self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.delete(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.all().count(), 2)
