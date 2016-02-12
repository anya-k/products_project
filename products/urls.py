from django.conf.urls import url
from products import views

urlpatterns = [
    url(r'^$', views.CategoryListView.as_view(), name='index'),
    # url(r'^(?P<pk>\d+)/$', views.ProductListView.as_view(), name='product_list'),
    url(r'^help/$', views.ProductListView.as_view(), name='product_list'),
]
