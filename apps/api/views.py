from rest_framework import routers, serializers, viewsets
from .models import Election, Person, Party, Constituency, ElectoralList, \
    ElectoralListSeat, ElectoralListSeatAssignment, Poll, PollResultLink
from rest_framework.response import Response
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from django.shortcuts import get_object_or_404


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.CharField(source='photo.file.url')

    class Meta:
        model = Person
        fields = ('name', 'photo')

class PartySerializer(serializers.HyperlinkedModelSerializer):
    logo = serializers.CharField(source='logo.file.url')

    class Meta:
        model = Party
        fields = ('name', 'logo', 'symbol', 'color')


class SeatSerializer(serializers.HyperlinkedModelSerializer):
    person = PersonSerializer(read_only=True)

    class Meta:
        model = ElectoralListSeatAssignment
        fields = ('seat', 'person')



class ElectoralListSerializer(serializers.HyperlinkedModelSerializer):
    party = PartySerializer()
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = ElectoralList
        fields = ('party', 'seats')


class ConstituencySerializer(serializers.HyperlinkedModelSerializer):

    electoral_lists = ElectoralListSerializer(many=True, read_only=True)

    class Meta:
        model = Constituency
        fields = ('name', 'electoral_lists')



class ElectionSerializer(serializers.HyperlinkedModelSerializer):
    constituencies = ConstituencySerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = ('url', 'title', 'constituencies')


class PollResultSerializer(serializers.HyperlinkedModelSerializer):
    party = PartySerializer()

    class Meta:
        model = PollResultLink
        fields = ('party', 'votes', 'percentage')


class PollSerializer(serializers.HyperlinkedModelSerializer):
    results = PollResultSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('url', 'title', 'date', 'source', 'results', 'total')


#### View sets

class ElectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ConstituencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer


class ElectoralListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ElectoralList.objects.all()
    serializer_class = ElectoralListSerializer


class PollViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PartyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
