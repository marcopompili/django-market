"""
Created on 19/giu/2013

@author: Marco Pompili
"""

from django import template
from django.core import urlresolvers
from django.utils.safestring import mark_safe

from django_market.models import Category

register = template.Library()


class MarketShowcaseNode(template.Node):
    def __init__(self):
        categories = Category.objects.filter(showcase=True)
        self.showcase_list = {category: self.products(category)
                              for category in categories
                              if self.products(category).exists()}

    @staticmethod
    def products(category):
        return category.product_set.filter(showcase=True)

    def render(self, context):
        context['showcase_list'] = self.showcase_list
        return ''


@register.tag
def market_showcase(parser, token):
    """
        Get a list of categories and products with the flag showcase checked.
        The structure used is a dictionary with categories as keys and list
        of products as values.
        
        Usage::
            {% market_showcase %}
    """
    return MarketShowcaseNode()


@register.filter()
def multititle(value):
    """
        Gets the title field only if is set.
        If no title is set the code-name will be used.
        
        Usage::
            {{ category|multititle }}
            {{ product|multititle }}
    """
    return value.name if value.name else value.codename


@register.filter()
def roots(value):
    """
        Filter all but the roots from the category tree (elements a level equal to zero)
    :param value:
    :return
    """

    return [category
            for category in value
            if category.level == 0]

    return value.objects.filter(level=0)


@register.filter()
def order_by_name(value):
    """
        Experimental, needs testing
    :param value:
    :return:
    """

    return sorted((category for category in value), key=lambda x: x.name)


@register.filter()
def order_by_weight(value):
    """
        Orders a list of categories based on their weights.
    :param value:
    :return:
    """

    return sorted((category for category in value), key=lambda x: x.weight)


@register.inclusion_tag('django_market/tags/breadcrumbs.html')
def breadcrumbs(category):
    """
        Renders a category tree path using a customizable delimiter.

        Usage::
            {% breadcrumbs <category> %}

        Example::
            {% breadcrumbs category %}
    """
    return {'ancestors': category.get_ancestors()}