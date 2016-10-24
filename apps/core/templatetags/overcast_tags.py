from django.template.exceptions import TemplateDoesNotExist
from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.assignment_tag
def get_next_sibling_by_order(page):
    sibling = page.get_next_siblings().live().first()

    if sibling:
        return sibling.specific


@register.assignment_tag
def get_prev_sibling_by_order(page):
    sibling = page.get_prev_siblings().live().first()

    if sibling:
        return sibling.specific


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page


def has_menu_children(page):
    if page.get_children().filter(live=True, show_in_menus=True):
        return True
    else:
        return False


@register.filter
def content_type(value):
    return value.__class__.__name__.lower()


@register.simple_tag
def render_block(block, template_prefix):
    if not template_prefix == '':
        new_template = "{}/{}".format(template_prefix, block.block.meta.template)
        try:
            template.loader.get_template(new_template)
            block.block.meta.template = new_template
        except TemplateDoesNotExist:
            pass
    return str(block)


@register.inclusion_tag('core/tags/top_menu.html', takes_context=True)
def top_menu(context, calling_page=None):
    """
    Checks to see if we're in the Play section in order to return pages with
    show_in_play_menu set to True, otherwise retrieves the top menu
    items - the immediate children of the site root.
    """

    menuitems = get_site_root(context).get_children().filter(
        live=True,
        show_in_menus=True
    )
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('core/tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent, calling_page):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.filter(
        live=True,
        show_in_menus=True
    )
    return {
        'calling_page': calling_page,
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the secondary links - only the children of the current page, NOT the siblings, and only when not viewing the homepage
@register.inclusion_tag('core/tags/secondary_menu.html', takes_context=True)
def secondary_menu(context, calling_page=None):
    menuitems = []
    if calling_page and calling_page.id != get_site_root(context).id:
        menuitems = calling_page.get_children().filter(
            live=True,
            show_in_menus=True
        )

        # If no children found and calling page parent isn't the root, get the parent's children
        if len(menuitems) == 0 and calling_page.get_parent().id != get_site_root(context).id:
            menuitems = calling_page.get_parent().get_children().filter(
                live=True,
                show_in_menus=True
            )
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.simple_tag()
def parse_csv_as_table(table_data, table_caption, table_header_row, table_footer_row,
                       table_header_column, separator='|', classes=""):

    rows = table_data.split('\n')

    if table_footer_row:
        classes += " footer-table"
    if table_header_row:
        classes += " header-table"

    html = '<table class="table %s">' % classes

    for row_num, row in enumerate(rows):

        if row_num == 0:
            if table_header_row:
                html += ' <thead>'
            else:
                html += ' <tbody>'

        html += '  <tr>'

        row = row.replace(' %s' % separator, '%s' % separator)
        row = row.replace('%s ' % separator, '%s' % separator)
        cells = row.split('%s' % separator)

        for cell_num, cell in enumerate(cells):

            colspan = "1"
            className = ""
            if cell.startswith('{'):
                if cell[1] == "*":
                    className = "td-collapsed"
                    if cell[2] == "*":
                        className += " border"
                        cell = cell[4:]
                    else:
                        cell = cell[3:]
                else:
                    colspan = cell[1]
                    cell = cell[3:]

            if row_num == 0 and table_header_row:
                html += '   <th colspan="%s" class="%s">%s</th>' % (colspan, className, cell)
            else:
                if cell_num == 0 and table_header_column:
                    html += '   <th colspan="%s" class="%s">%s</th>' % (colspan, className, cell)
                else:
                    html += '   <td colspan="%s" class="%s">%s</td>' % (colspan, className, cell)

        html += '  </tr>'

        if row_num == 0 and table_header_row:
            html += ' </thead>'
            html += ' <tbody>'

    html += ' </tbody>'
    html += '</table>'

    return mark_safe(html)


@register.inclusion_tag('tags/grid_block.html', takes_context=False)
def parse_grid_block(template, blocks):
    regx = re.compile(r'{block\d+}')
    template_list = regx.split(template)
    fin_blocks = []
    for idx, el in enumerate(template_list):
        fin_blocks.append(el)
        if idx < len(blocks):
            fin_blocks.append(blocks[idx])
    return {
        'grid_blocks': fin_blocks,
        'template_list': template_list,
        'template': template,
        'blocks': blocks
    }
