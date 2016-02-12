from django.contrib import admin

from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    # list_display = ('name', 'price', 'category')
    list_display = ('name', 'price', 'category', 'created_at', 'modified_at', 'slug')
    exclude = ('created_at', 'modified_at', 'slug')
    list_filter = ['created_at']


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    exclude = ('created_at', 'modified_at', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    exclude = ('slug',)
    inlines = [ProductInline,]

    def get_form(self, request, obj=None, **kwargs):
        request.current_object = obj
        return super(CategoryAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        instance = request.current_object
        if db_field.name == "category":
            if instance:
                kwargs["queryset"] = Product.objects.filter(category=instance.id)
            else:
                kwargs["queryset"] = Product.objects.filter(category=None)
        return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)