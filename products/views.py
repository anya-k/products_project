from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.shortcuts import render

from models import Category, Product


def index(request):
    return render(request, 'base.html')


class CategoryListView(ListView):
    model = Category


class ProductListView(ListView):
    model = Product

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        category = Category.objects.filter(slug=slug)
        if category:
            self.queryset = Product.objects.filter(category_id=category[0].id)
        return super(ProductListView, self).get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    query_pk_and_slug = True
    template_name = 'products/product_detail.html'
