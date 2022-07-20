from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from applications.product.views import CategoryView, ProductView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('product', ProductView)

urlpatterns = [
    path('', include(router.urls)),

]
