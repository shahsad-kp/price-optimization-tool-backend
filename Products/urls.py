from rest_framework.routers import DefaultRouter

from Products.apis import ProductViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet)

urlpatterns = router.urls
