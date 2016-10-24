from __future__ import unicode_literals

from django.db import models
from django import forms

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.blocks import FieldBlock, StructBlock, CharBlock, \
    ListBlock, RichTextBlock, StreamBlock, RawHTMLBlock, BooleanBlock, \
    TextBlock, ChoiceBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock


class ParagraphBlock(StructBlock):
    paragraph = RichTextBlock()
    extra_classes = CharBlock(required=False)


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'),
        ('right', 'Wrap right'),
        ('half', 'Half width'),
        ('full', 'Full width'),
        ('fit_content', 'Fit content'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    alignment = ImageFormatChoiceBlock()
    caption = CharBlock(required=False)
    overlay_text = RichTextBlock(required=False)
    attribution = CharBlock(required=False)
    extra_classes = CharBlock(required=False)

    class Meta:
        icon = "image"


class ImageCollection(StructBlock):
    images = ListBlock(StructBlock([
                ('image', ImageChooserBlock(required=True)),
                ('caption', CharBlock(required=False)),
                ('credit', CharBlock(required=False)),
        ]))
    extra_classes = CharBlock(required=False)

    class Meta:
        icon = 'image'


class PullQuoteBlock(StructBlock):
    quote = CharBlock(classname="quote title")
    attribution = CharBlock(required=False)
    extra_classes = CharBlock(required=False)

    class Meta:
        icon = "openquote"


class ChartBlock(StructBlock):
    charts = ListBlock(StructBlock(
        [
            ('Title', CharBlock(classname="title", required=False)),
            ('Subtitle', CharBlock(required=False)),
            ('UniqueID', CharBlock(required=True)),
            ('Blocktype', ChoiceBlock(
                choices=[
                    ('bar', 'Bar Chart'),
                    ('pie', 'Pie Chart'),
                    ('doughnut', 'Doughnut Chart'),
                    ('line', 'Line Chart'),
                ], default='bar', required=True)
            ),
            ('Data', TextBlock(rows=10, required=True, help_text="Data for Chart on the form: label1, value1, label2, value2, ...")),
            ('Options', TextBlock(rows=10, required=False, help_text="Extended options for the chart"))
        ]
    ))
    contained_charts = BooleanBlock(default=False, required=False)
    extra_classes = CharBlock(required=False)

    class Meta:
        icon = 'radio-empty'


class TableBlock(StructBlock):
    table = TextBlock(rows=10, help_text=u'Enter your table as comma separated values, one line for each row.')
    caption = CharBlock(required=False)
    header_row = BooleanBlock(required=False, help_text=u'Render first row as header if checked')
    footer_row = BooleanBlock(required=False, help_text=u'Render last row as footer if checked')
    header_column = BooleanBlock(required=False, help_text=u'Render first column as header if checked')
    extra_classes = CharBlock(required=False)

    class Meta:
        icon = 'icon icon-fa-table'


class GridBlocks(StreamBlock):
    text_block = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", template="blocks/aligned_image_block.html")
    image_collection = ImageCollection(label="Image collection", template="blocks/image_collection_block.html")
    pullquote = PullQuoteBlock(template="blocks/pullquote_block.html")
    raw_html = RawHTMLBlock(label='Raw HTML', icon="code", template="blocks/raw_html_block.html")
    embed = EmbedBlock(icon="code", template="blocks/embed_block.html")
    chart_block = ChartBlock(template="blocks/chart_block.html", icon="image")
    table_block = TableBlock(template="blocks/table_block.html", icon="list-ol")


class GridBlock(StructBlock):
    template = TextBlock(rows=10, help_text='Enter your template as a plain HTML.')
    content_blocks = ListBlock(GridBlocks())
    extra_classes = CharBlock(required=False)

    class Meta:
        icon = 'placeholder'


class StoryBlock(StreamBlock):
    intro = RichTextBlock(template="blocks/intro_block.html", icon="pilcrow")
    paragraph = ParagraphBlock(template="blocks/paragraph_block.html", icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", template="blocks/aligned_image_block.html")
    image_collection = ImageCollection(label="Image collection", template="blocks/image_collection_block.html")
    pullquote = PullQuoteBlock(template="blocks/pullquote_block.html")
    raw_html = RawHTMLBlock(label='Raw HTML', icon="code", template="blocks/raw_html_block.html")
    embed = EmbedBlock(icon="code", template="blocks/embed_block.html")
    grid_block = GridBlock(template="blocks/grid_block.html")
    chart_block = ChartBlock(template="blocks/chart_block.html")
    table_block = TableBlock(template="blocks/table_block.html")
