from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter

# Create your views here.
from .models import Category
from .serializer import CategorySerializer
from paginations import CustomPageNumerPagination


class CategoryApiView(generics.ListCreateAPIView):
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    pagination_class = CustomPageNumerPagination
    search_fields = ('name', 'position')
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetilAPiView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
