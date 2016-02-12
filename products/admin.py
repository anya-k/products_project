from django.contrib import admin

from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at', 'modified_at')
    exclude = ('created_at', 'modified_at', 'slug')
    list_filter = ['created_at']


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    exclude = ('created_at', 'modified_at', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('slug',)
    inlines = [ProductInline,]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)