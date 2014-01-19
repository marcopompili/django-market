"""
Created on 12/mag/2013

@author: Marco Pompili
"""

from django.conf.urls import patterns, url

from .views import CategoriesListView, CategoryDetailView, ProductDetailView

urlpatterns = patterns('',
                       # example with unordered list
                       # url(r'^categories/$', CategoriesListView.as_view(), name="categories"),
                       url(r'^(?P<slug>[-_\w/]+)/$', CategoryDetailView.as_view(), name="category"),
                       url(r'^(?P<pk>\d+)/(?P<slug>[-_\w]+)/$', ProductDetailView.as_view(), name='product'),
)