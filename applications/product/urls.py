from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from applications.product.views import CategoryView, ProductView, CommentView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('comment', CommentView)
router.register('product', ProductView)


urlpatterns = [
    path('', include(router.urls)),
    # TODO: реаизовать комментарии и переопределить to representation на вывод комментов
]
