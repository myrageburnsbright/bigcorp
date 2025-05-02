from django.contrib import admin
from .models import Category,Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['parent','name','slug']
    ordering = ['name',]
    
    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('name',)
            }
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):    
    list_display = ['id','category','title','brand','slug', 'available', 'price', 'updated_at', 'created_at']
    ordering = ['title',]
    list_filter = ['available', 'created_at', 'updated_at']

    def get_prepopulated_fields(self, request, obj = None):
        return {
            'slug': ('title',)
            }