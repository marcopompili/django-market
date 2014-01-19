"""
Created on 23/gen/2014

@author: Marco Pompili
"""

from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Product


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug', 'subtitle', 'description',)


translator.register(Category, CategoryTranslationOptions)


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


translator.register(Product, ProductTranslationOptions)