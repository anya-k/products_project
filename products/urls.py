from django.conf.urls import url
from products import views

urlpatterns = [
    url(r'^$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^new/$', views.LastAddProductListView.as_view(), name='product_new'),
    url(r'^(?P<slug>[\w-]+)/$', views.ProductListView.as_view(), name='product_list'),
    url(r'^(?P<slug_category>[\w-]+)/(?P<slug>[\w-]+)/$', views.ProductDetailView.as_view(), name='product_detail'),
]
