from raw import views
from utils.rest.routers import DefaultRouter

router = DefaultRouter()
router.register(r'raw', views.RawViewSet, basename='raw')
router.register(r'url', views.UrlViewSet, basename='url')
router.register(r'request', views.RequestViewSet, basename='request')
router.register(r'response', views.ResponseViewSet, basename='response')
urlpatterns = router.urls
