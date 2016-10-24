from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel


class BaseTemplate(models.Model):
    title = models.CharField(max_length=255, blank=True)
    filename = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('filename'),
    ]

    def __unicode__(self):
        return self.title

register_snippet(BaseTemplate)


@register_setting
class GeneralSiteSettings(BaseSetting):
    base_template = models.ForeignKey(BaseTemplate, null=True)
    template_dir = models.CharField(max_length=255, blank=True)
    google_analytics_property = models.CharField(max_length=255, blank=True)

    panels = [
        SnippetChooserPanel('base_template'),
        FieldPanel('template_dir'),
        FieldPanel('google_analytics_property'),

    ]


class SiteSettingsTemplateMixin(object):

    def get_template(self, request):
        app_settings = GeneralSiteSettings.for_site(request.site)
        template = super(SiteSettingsTemplateMixin, self).get_template(request)

        if app_settings.template_dir != '':
            return "%s/%s" % (app_settings.template_dir, template)
        return template
