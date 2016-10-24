from django.utils.html import format_html_join, format_html
from django.conf import settings

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, allow_without_attributes


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'p': attribute_rule({'class': True, 'style': True}),
        'blockquote': allow_without_attributes,
        'span': attribute_rule({'class': True}),
        'sub': allow_without_attributes,
        'sup': allow_without_attributes,
    }


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'js/hallo-custombuttons.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('subbutton');
            registerHalloPlugin('supbutton');
            registerHalloPlugin('hallojustifyovercast');
            registerHalloPlugin('halloheadings', {{formatBlocks: ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']}});
            registerHalloPlugin('hallohtmlovercast');
            delete halloPlugins['hallohr'];
        </script>
        """
    )
