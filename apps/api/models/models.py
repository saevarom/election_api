from django.db import models
from wagtail.wagtailadmin.edit_handlers import InlinePanel, FieldPanel
from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.models import Orderable, Page
from modelcluster.fields import ParentalKey
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


class Person(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ForeignKey(
        'core.OvercastImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('photo'),
    ]

    def __unicode__(self):
        return self.name

register_snippet(Person)

class Party(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    logo = models.ForeignKey(
        'core.OvercastImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    color = models.CharField(max_length=30, blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('symbol'),
        FieldPanel('color'),
        ImageChooserPanel('logo'),
    ]

    def __unicode__(self):
        return self.name

register_snippet(Party)


class Election(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)

    @property
    def constituencies(self):
        return self.constituency_set.all()

    def __unicode__(self):
        return self.title

register_snippet(Election)


class ElectionResult(models.Model):
    election = models.ForeignKey(Election)
    party = models.ForeignKey(Party)
    votes = models.IntegerField()




class PollResult(models.Model):
    party = models.ForeignKey(Party)
    votes = models.IntegerField()

    panels = [
        FieldPanel('votes'),
        SnippetChooserPanel('party'),
    ]

    def percentage(self):
        return 100.0*self.votes/self.pollresultlink.poll.total


class PollResultLink(Orderable, PollResult):
    poll = ParentalKey('Poll', related_name='poll_results')


class Poll(ClusterableModel):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    date = models.DateField()
    election = models.ForeignKey(Election)

    def __unicode__(self):
        return u"%s - %s" % (self.title, self.date)

    panels = [
        FieldPanel('title'),
        FieldPanel('source'),
        FieldPanel('date'),
        InlinePanel('poll_results', label="Results"),
    ]

    @property
    def results(self):
        return self.poll_results.all()

    @property
    def total(self):
        return self.results.aggregate(models.Sum('votes'))['votes__sum']



class Constituency(models.Model):
    name = models.CharField(max_length=255)
    voters = models.IntegerField()
    available_seats = models.IntegerField()
    extra_seats = models.IntegerField()
    election = models.ForeignKey('Election')

    def __unicode__(self):
        return "%s - %s" % (self.name, self.election)

    def electoral_lists(self):
        return self.electorallist_set.all()

    panels = [
        FieldPanel('name'),
        FieldPanel('voters'),
        FieldPanel('available_seats'),
        FieldPanel('extra_seats'),
        SnippetChooserPanel('election'),
    ]


class ElectoralListSeat(models.Model):
    seat = models.IntegerField()
    person = models.ForeignKey(Person, null=True, blank=True)
    #electoral_list = models.ForeignKey(ElectoralList)

    panels = [
        FieldPanel('seat'),
        SnippetChooserPanel('person'),
    ]


class ElectoralListSeatAssignment(Orderable, ElectoralListSeat):
    seats = ParentalKey('ElectoralList', related_name='electoral_list_seats')


class ElectoralList(ClusterableModel):
    """
    The electoral list model represents a list of candidates for a single party
    in a single constituency.
    """
    constituency = models.ForeignKey(Constituency)
    party = models.ForeignKey(Party)

    def __unicode__(self):
        return u"%s - %s" % (self.party, self.constituency)

    panels = [
        FieldPanel('constituency'),
        FieldPanel('party'),
        InlinePanel('electoral_list_seats', label="Seats"),
    ]

    def seats(self):
        return self.electoral_list_seats.all()
