"""
Created on 28/mag/2013

@author: Marco Pompili
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from mptt.forms import TreeNodeChoiceField

from .models import Category, Product


def get_treenode_mptt_field(category_id=None, **kwargs):
    """
        Filter categories based on the current category.
    """
    required = kwargs.pop('required', False)

    if category_id:
        return TreeNodeChoiceField(queryset=Category.objects.exclude(id=category_id), required=required)
    else:
        return TreeNodeChoiceField(queryset=Category.objects.all(), required=required)


def get_cover_choice_field(category_id):
    """
        Filter products based on the current category.
    """
    return forms.ModelChoiceField(queryset=Product.objects.filter(category=category_id),
                                  label=_(u"use product as cover"),
                                  help_text=_(u"Choose the product to use as cover icon for this category."),
                                  required=False)


class CategoryForm(forms.ModelForm):
    """
        Form based on the Category model, but with no filtering.
    """
    class Meta:
        model = Category

    parent = get_treenode_mptt_field()


class ProductForm(forms.ModelForm):
    """
        Form based on the Product model, but without filtering.
    """
    class Meta:
        model = Product

    category = get_treenode_mptt_field(required=True)