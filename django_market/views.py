"""
Created on 12/mag/2013

@author: Marco Pompili
"""

from django.views import generic

from .models import Category, Product


class CategoriesListView(generic.ListView):
    model = Category
    context_object_name = "categories"
    template_name = "django_market/category/index.html"


class GenericMarketDetailView(generic.DetailView):
    def get_context_data(self, **kwargs):
        context = super(GenericMarketDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by("weight")
        return context


class CategoryDetailView(GenericMarketDetailView):
    model = Category
    context_object_name = "category"
    template_name = "django_market/category/detail.html"

    def get_context_data(self, **kwargs):
        category = self.get_object()
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category=category.id).order_by('id')[:]
        return context


class ProductDetailView(GenericMarketDetailView):
    model = Product
    context_object_name = "product"
    template_name = 'django_market/product/detail.html'

    def get_context_data(self, **kwargs):
        product = self.get_object()
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['category'] = product.category
        return context