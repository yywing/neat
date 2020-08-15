from rest_framework.routers import DefaultRouter
from normal import views

router = DefaultRouter()
router.register(r'param', views.ParamViewSet, basename='param')
router.register(r'raw-param', views.ParamViewSet, basename='raw-param')
urlpatterns = router.urls
