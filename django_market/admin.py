"""
Created on 12/mag/2013

@author: Marco Pompili
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail.admin.current import AdminImageWidget
from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin, TranslationStackedInline

from django_galleries import models as django_galleries_models
from django_galleries import admin as django_galleries_admin

from .models import Product, Category
from .forms import ProductForm, CategoryForm, get_treenode_mptt_field, get_cover_choice_field

# Check note
# from sorl.thumbnail.admin import AdminImageMixin


class ProductInline(TranslationStackedInline):
    model = Product
    extra = 2

    fieldsets = (
        (_(u'Administration Options'),
         {
             'fields': ('codename', 'category', 'gallery', 'weight',)
         }),
        (_(u'Name'),
         {
             'classes': ('collapse',),
             'fields': ('name',)
         }),
        (_(u'Description'),
         {
             'classes': ('collapse',),
             'fields': ('description',)
         }),
        (_(u'Advanced Options'),
         {
             'classes': ('collapse',),
             'fields': ('showcase',)
         }),
    )


class CategoryAdmin(MPTTModelAdmin, TranslationAdmin):
    form = CategoryForm
    search_fields = ['codename']
    list_display = ('codename', 'parent', 'cover', 'description',)
    ordering = ['parent', 'codename']
    group_fields = True
    actions = ['update_category']

    def get_actions(self, request):
        # TODO, FIX: I've removed the delete action for now, to avoid a bug of django-mptt.
        actions = super(CategoryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions

    def update_category(self, request, queryset):
        for category in queryset:
            category.save()

    update_category.short_description = _("Resave the selected categories (Dev)")

    def get_form(self, request, obj=None, **kwargs):
        # TODO, FIX: _do_get_form_or_formset not present in django-modeltranslation >= 0.8
        kwargs = self._do_get_form_or_formset(request, obj, **kwargs)
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)

        if obj:
            # Show only the products related with the current category
            form.base_fields['cover'] = get_cover_choice_field(obj.id)
            # Exclude the editing category from the select list
            form.base_fields['parent'] = get_treenode_mptt_field(obj.id)

        # Forcing the ImageField to use the AdminImageWidget
        # Without this model-translation is probably overriding the behavior of sorl-thumbnail.
        form.base_fields['background'].widget = AdminImageWidget()

        # Quite dirty way for making the name_* translations mandatory, buy hey...
        for key, field in self.form.base_fields.items():
            if key.startswith("name_"):
                field.required = True

        return form

    fieldsets = [
        (_(u'Administration Options'),
         {
             'fields': ('codename', 'parent', 'cover', 'weight',),
         }),
        (_(u'Name'),
         {
             'fields': ('name',)
         }),
        (_(u'Subtitle'),
         {
             'classes': ('collapse',),
             'fields': ('subtitle',)
         }),
        (_(u'Description'),
         {
             'classes': ('collapse',),
             'fields': ('description',)
         }),
        (_(u'Advanced Options'),
         {
             'fields': ('background', 'showcase',)
         }),
    ]

    inlines = [ProductInline]


class ProductAdmin(TabbedTranslationAdmin):
    form = ProductForm
    search_fields = ['codename']
    list_display = ('category', 'codename', 'weight', 'gallery',)
    list_display_links = ('codename',)
    list_editable = ('weight',)
    ordering = ['category', 'weight', 'codename']

    fieldsets = (
        (_(u'Administration Options'),
         {
             'fields': ('codename', 'category', 'gallery', 'weight')
         }),
        (_(u'Name'),
         {
             'fields': ('name',)
         }),
        (_(u'Description'),
         {
             'classes': ('collapse',),
             'fields': ('description',)
         }),
        (_(u'Advanced Options'),
         {
             'fields': ('showcase',)
         }),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)


class GalleryAdmin(django_galleries_admin.GalleryAdmin):
    list_display = ("codename", "title", "product",)

    def product(self, obj):
        return Product.objects.get(gallery=obj.id)


admin.site.unregister(django_galleries_models.Gallery)
admin.site.register(django_galleries_models.Gallery, GalleryAdmin)
