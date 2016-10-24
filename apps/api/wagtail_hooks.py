
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Constituency, Election, ElectoralList, Person, Party, Poll


class ElectoralListAdmin(ModelAdmin):
    model = ElectoralList
    #menu_label = 'Page Model'  # ditch this to use verbose_name_plural from model
    #menu_icon = 'doc-full-inverse'  # change as required
    #list_display = ('title', 'example_field2', 'example_field3', 'live')
    #list_filter = ('live', 'example_field2', 'example_field3')

class ElectionAdmin(ModelAdmin):
    model = Election
    list_display = ('title',)
    search_fields = ('title',)


class PartyAdmin(ModelAdmin):
    model = Party
    list_display = ('symbol', 'name',)
    search_fields = ('name',)


class PeopleAdmin(ModelAdmin):
    model = Person
    list_display = ('name',)
    search_fields = ('name',)


class ConstituencyAdmin(ModelAdmin):
    model = Constituency
    list_display = ('name', 'election')
    list_filter = ('election',)
    search_fields = ('name',)


class PollAdmin(ModelAdmin):
    model = Poll
    list_display = ('title', 'source', 'date', 'election')



class ElectionAdminGroup(ModelAdminGroup):
    menu_label = 'Kosningar'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (ElectionAdmin, ConstituencyAdmin, ElectoralListAdmin, PartyAdmin, PeopleAdmin, PollAdmin)

# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(ElectionAdminGroup)
