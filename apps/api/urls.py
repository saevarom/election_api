from rest_framework_nested import routers

from django.conf.urls import url, include

from .views import ElectionViewSet, ConstituencyViewSet, ElectoralListViewSet, PersonViewSet, PollViewSet, PartyViewSet


router = routers.DefaultRouter()
router.register(r'elections', ElectionViewSet)
router.register(r'constituencies', ConstituencyViewSet)
router.register(r'electoral_lists', ElectoralListViewSet)
router.register(r'person', PersonViewSet)
router.register(r'polls', PollViewSet)
router.register(r'party', PartyViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
