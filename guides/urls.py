from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FirstAidGuideViewSet

router = DefaultRouter()
router.register(r'guides', FirstAidGuideViewSet, basename="guides")

urlpatterns = [
    path('', include(router.urls)),
]


from django.urls import path, include
from .views import guide_list
urlpatterns += [
    path("guides-ui/", guide_list, name="guide_list"),
]
