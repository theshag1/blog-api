from django.urls import path
from .views import CategoryApiView , CategoryDetilAPiView
urlpatterns = [
    path('', CategoryApiView.as_view() , name='category'),
    path('<int:pk>', CategoryDetilAPiView.as_view() , name='category-detil'),

]
