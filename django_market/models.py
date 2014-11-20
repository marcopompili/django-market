"""
Created on 12/mag/2013

@author: Marco Pompili
"""

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.templatetags.i18n import language_name
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from django_galleries.models import Gallery

__max_url_length__ = 1024


def is_translatable(model, lang_code):
    return hasattr(model, 'slug_%s' % lang_code) and hasattr(model, 'name_%s' % lang_code)


def translate_slug(model, lang_code):
    return slugify(getattr(model, 'name_%s' % lang_code, u""))


def set_translation(model, lang_code, url_i18n):
    setattr(model, 'slug_%s' % lang_code, url_i18n)


class Category(MPTTModel):
    """
        Categories used for grouping products.
        Categories are using the mptt model (django-mptt),
        so can be organized in hierarchies.
    """

    class Meta:
        verbose_name = _(u"category")
        verbose_name_plural = _(u"categories")

    class MPTTMeta:
        order_insertion_by = ['codename']

    codename = models.CharField(max_length=25, unique=True, help_text=_(
        u"The code-name for this category, it's useful for the administration interface."))

    name = models.CharField(max_length=75, blank=False, null=False, help_text=_(
        u"This will displayed and translated, if it's empty the codename will be used."))

    weight = models.IntegerField(_(u"Weight"), blank=True, null=True, help_text=_(u"Custom order for this category"))

    subtitle = models.CharField(max_length=75, blank=True, null=True,
                                help_text=_(u"This will displayed and translated."))

    description = models.TextField(blank=True, null=True, help_text=_(u"This will displayed and translated."))

    showcase = models.BooleanField(_(u"on Show-case"),
                                   help_text=_(u"If checked puts this category on the shop window."))

    background = models.ImageField(upload_to='django_market/backgrounds/', blank=True, null=True,
                                   verbose_name=_(u"Background image"))

    cover = models.OneToOneField('Product', related_name='Product.id', blank=True, null=True)

    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name=_(u"Parent category"),
                            help_text=_(u"The Parent category, if no one is given this will be a root category."))

    slug = models.SlugField(max_length=__max_url_length__, blank=True, editable=False)

    def save(self, *args, **kwargs):
        """
            Weird stuff for making URL (slugs) based on languages
        """

        # checking if is root_node because get_ancestors(include_self=True)
        # doesn't work with a model that has still to be saved.
        # The get_ancestors method will return None.
        if self.is_root_node():
            for lang_code, lang_name in settings.LANGUAGES:
                if is_translatable(self, lang_code):
                    set_translation(self, lang_code, translate_slug(self, lang_code))
        else:
            for lang_code in settings.LANGUAGES:
                ancestors = [
                    translate_slug(ancestor, lang_code)
                    for ancestor in self.get_ancestors(include_self=True)
                    if is_translatable(ancestor, lang_code)
                ]

                set_translation(self, lang_code, '/'.join(ancestors))

        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.codename


class Product(models.Model):
    """
        Basic implementation for a product object.
    """

    class Meta:
        verbose_name = _(u"product")
        verbose_name_plural = _(u"products")

    codename = models.CharField(max_length=25, unique=True,
                                help_text=_(u"The code-name for this product, useful for administration purposes."))
    slug = models.SlugField(max_length=75, blank=True, editable=False)

    name = models.CharField(max_length=75, blank=True, null=True,
                            help_text=_(u"If no product name is set the codename will be used."))

    weight = models.IntegerField(_(u"Weight"), blank=True, null=True, help_text=_(u"Custom order for this product"))

    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(Category, help_text=_(u"The category of the product."))

    gallery = models.OneToOneField(Gallery, blank=True, null=True, verbose_name=_(u"Product gallery"))

    showcase = models.BooleanField(_(u"Put on shop window"),
                                   help_text=_(u"If checked puts the product on the showcase list."))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.codename)
        super(Product, self).save()

    def __unicode__(self):
        return self.codename