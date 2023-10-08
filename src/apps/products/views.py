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
from django_filters import rest_framework as filters

from src.apps.products.models import ProductCategory, Product
from src.apps.products.serializers import (
    ProductCategoryInputSerializer,
    ProductCategoryOutputSerializer,
    ProductInputSerializer,
    ProductOutputSerializer,
    ProductDetailOutputSerializer,
    ProductUpdateInputSerializer,
    ProductUpdateDataInputSerializer,
)
from src.apps.products.services.product_category_service import (
    ProductCategoryCreateService,
    ProductCategoryUpdateService,
)
from src.apps.products.services.product_service import (
    ProductCreateService,
    ProductUpdateService,
)
from src.apps.products.filters import ProductFilter
from src.core.permissions import StaffOrReadOnly, SellerOrAdmin


class ProductCategoryListCreateAPIView(GenericViewSet, ListModelMixin):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryOutputSerializer
    permission_classes = [StaffOrReadOnly]

    def create(self, request: Request) -> Response:
        service = ProductCategoryCreateService()
        serializer = ProductCategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = service.create_category(request_data=serializer.validated_data)
        return Response(
            self.get_serializer(category).data, status=status.HTTP_201_CREATED
        )


class ProductCategoryDetailAPIView(
    GenericViewSet, RetrieveModelMixin, DestroyModelMixin
):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryOutputSerializer
    permission_classes = [StaffOrReadOnly]

    def update(self, request: Request, pk: UUID) -> Response:
        service = ProductCategoryUpdateService()
        instance = self.get_object()
        serializer = ProductCategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_category = service.update_category(
            request_data=serializer.validated_data, instance=instance
        )
        return Response(
            self.get_serializer(updated_category).data, status=status.HTTP_200_OK
        )

    def delete(self, request: Request, pk: UUID) -> Response:
        self.destroy(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPIView(GenericViewSet, ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductOutputSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [SellerOrAdmin]

    def create(self, request: Request) -> Response:
        service = ProductCreateService()
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = service.product_create(request_data=serializer.validated_data)
        return Response(
            self.get_serializer(product).data, status=status.HTTP_201_CREATED
        )


class ProductDetailAPIView(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductDetailOutputSerializer
    permission_classes = [SellerOrAdmin]

    def update(self, request: Request, pk: UUID) -> Response:
        service = ProductUpdateService()
        instance = self.get_object()
        serializer = ProductUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_product = service.product_update(
            request_data=serializer.validated_data, instance=instance
        )
        return Response(
            self.get_serializer(updated_product).data, status=status.HTTP_200_OK
        )

    def delete(self, request: Request, pk: UUID) -> Response:
        self.destroy(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
