from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.shortcuts import render
import datetime
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from models import Category, Product

hours_delta = 24


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

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        category = Category.objects.filter(slug=category_slug)
        if category:
            context['category'] = category[0]
        return context


class ProductDetailView(DetailView):
    model = Product
    query_pk_and_slug = True
    template_name = 'products/product_detail.html'


class LastAddProductListView(ListView):
    model = Product
    template_name = 'products/new_product_list.html'

    def get(self, request, *args, **kwargs):
        date_from = datetime.datetime.now() - datetime.timedelta(hours=hours_delta)
        new_products = Product.objects.filter(created_at__gte=date_from)
        self.queryset = new_products
        return super(LastAddProductListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LastAddProductListView, self).get_context_data(**kwargs)
        category_list = {}
        for product in self.object_list:
            name = product.category
            if name not in category_list:
                category_list.update({name: [product, ]})
            else:
                category_list[name].append(product)

        context['category_list'] = category_list
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LastAddProductListView, self).dispatch(*args, **kwargs)


