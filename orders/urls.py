from rest_framework import routers
from rest_framework_nested import routers 
from .views import *

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)
router.register(r'order', OrderViewSet)

cart_router = routers.NestedSimpleRouter(router, r'cart', lookup='cart')
cart_router.register(r'items', CartItemsViewSet, basename='items')



urlpatterns = router.urls

