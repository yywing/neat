from normal import views
from utils.routers import DefaultRouter

router = DefaultRouter()
router.register(r'param', views.ParamViewSet, basename='param')
router.register(r'raw-param', views.RawParamViewSet, basename='raw-param')
urlpatterns = router.urls
