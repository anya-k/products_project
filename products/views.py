from django.views.generic.list import ListView

from models import Category, Product


class CategoryListView(ListView):
    model = Category


class ProductListView(ListView):
    model = Product
