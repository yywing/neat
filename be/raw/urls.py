from raw import views
from utils.routers import DefaultRouter

router = DefaultRouter()
router.register(r'raw', views.RawViewSet, basename='raw')
router.register(r'url', views.RawViewSet, basename='url')
router.register(r'request', views.RawViewSet, basename='request')
router.register(r'response', views.RawViewSet, basename='response')
urlpatterns = router.urls
