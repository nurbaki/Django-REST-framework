from rest_framework import routers
from .views import (
    ProductView,
    CategoryView,
    BrandView,
    StockView,
    FirmView,
)

router = routers.DefaultRouter()
router.register('stocks', StockView)
router.register('products', ProductView)
router.register('firms', FirmView)
router.register('category', CategoryView)
router.register('brands', BrandView)
urlpatterns = router.urls