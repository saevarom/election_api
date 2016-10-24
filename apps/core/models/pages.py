from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, \
    InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField

from modelcluster.fields import ParentalKey
from .mixins import SiteSettingsTemplateMixin
from .blocks import StoryBlock


# ===============================================================
#
#       DO NOT EDIT THIS FILE! MAKE ALL EDITS/OVERRIDES IN
#                   PROJECT SPECIFIC FOLDERS!
#
# ===============================================================


# A couple of abstract classes that contain commonly used fields
class ContentBlock(models.Model):
    content = RichTextField()

    panels = [
        FieldPanel('content'),
    ]

    class Meta:
        abstract = True


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True


# Carousel items
class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'core.OvercastImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Related links
class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Custom image
class OvercastImage(AbstractImage):
    credit = models.CharField(max_length=255, blank=True)

    @property
    def credit_text(self):
        return self.credit

    admin_form_fields = Image.admin_form_fields + (
        'credit',
    )


# Receive the pre_delete signal and delete the file associated with
# the model instance.
@receiver(pre_delete, sender=OvercastImage)
def image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


class OvercastRendition(AbstractRendition):
    image = models.ForeignKey('OvercastImage', related_name='renditions')

    admin_form_fields = Image.admin_form_fields + (
        'credit',
    )

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


# Receive the pre_delete signal and delete the file associated with the model
# instance.
@receiver(pre_delete, sender=OvercastRendition)
def rendition_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


COMMON_PANELS = (
    FieldPanel('slug'),
    FieldPanel('seo_title'),
    FieldPanel('show_in_menus'),
    FieldPanel('search_description'),
)


class StandardPageContentBlock(Orderable, ContentBlock):
    page = ParentalKey('core.StandardPage', related_name='content_block')


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('core.StandardPage', related_name='related_links')


class BaseStandardPage(SiteSettingsTemplateMixin, Page):
    header_image = models.ForeignKey(
        'core.OvercastImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    feed_image = models.ForeignKey(
        'core.OvercastImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    indexed_fields = ('title',)
    search_name = None

    class Meta:
        abstract = True


BASESTANDARDPAGE_CONTENT_PANELS = [
    FieldPanel('title', classname="full title"),
    ImageChooserPanel('header_image'),
    InlinePanel('content_block', label="Content block"),
    InlinePanel('related_links', label="Related links"),
]

BASESTANDARDPAGE_PROMOTE_PANELS = [
    MultiFieldPanel(COMMON_PANELS, "Common page configuration"),
    ImageChooserPanel('feed_image'),
]


class StandardPage(BaseStandardPage):
    streamfield = StreamField(StoryBlock())

StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    ImageChooserPanel('header_image'),
    StreamFieldPanel('streamfield'),
    InlinePanel('content_block', label="Content block"),
    InlinePanel('related_links', label="Related links"),
]

StandardPage.promote_panels = BASESTANDARDPAGE_PROMOTE_PANELS