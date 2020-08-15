from rest_framework.routers import DefaultRouter
from raw import views

router = DefaultRouter()
router.register(r'raw', views.RawViewSet, basename='raw')
router.register(r'url', views.RawViewSet, basename='url')
router.register(r'request', views.RawViewSet, basename='request')
router.register(r'response', views.RawViewSet, basename='response')
urlpatterns = router.urls
