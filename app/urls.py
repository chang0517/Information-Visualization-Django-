from django.contrib import admin
from django.urls import path, include
from app.views import index, results

urlpatterns = [
    path('', index, name = 'index'),
    path('results/', results, name='results')
]
