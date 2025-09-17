from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)
urlpatterns = router.urls

