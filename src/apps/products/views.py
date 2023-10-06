from uuid import UUID

from rest_framework import permissions, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)

from src.apps.products.models import ProductCategory, Product
from src.apps.products.serializers import (
    ProductCategoryInputSerializer,
    ProductCategoryOutputSerializer,
    ProductInputSerializer,
    ProductOutputSerializer,
    ProductDetailOutputSerializer
)


class ProductCategoryListCreateAPIView(GenericViewSet, ListModelMixin):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryOutputSerializer
    
    def create(self, request: Request) -> Response:
        pass


class ProductCategoryDetailAPIView(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryOutputSerializer
    service_class = None

    def update(self, request: Request, pk: UUID) -> Response:
        pass
    
    def delete(self, request: Request, pk: UUID) -> Response:
        self.destroy(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPIView(GenericViewSet, ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductOutputSerializer
    
    def create(self, request: Request) -> Response:
        pass


class ProductDetailAPIView(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductDetailOutputSerializer
    service_class = None

    def update(self, request: Request, pk: UUID) -> Response:
        pass
    
    def delete(self, request: Request, pk: UUID) -> Response:
        self.destroy(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
