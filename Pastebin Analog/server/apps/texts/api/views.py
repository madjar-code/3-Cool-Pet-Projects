from enum import Enum
from typing import List
from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache
from django.db.models import F, QuerySet
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.parsers import (
    JSONParser,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from rest_framework.throttling import (
    AnonRateThrottle,
    UserRateThrottle,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from users.models import User
from texts.models import TextBlock
from texts.services.hash import hash_factory
from .serializers import (
    SimpleTextBlockSerializer,
    TextBlockSerializer,
    CUTextBlockSerializer,
)


hash_generator = hash_factory('sha')


class ErrorMessages(str, Enum):
    NO_USER = 'User with `username` no found'
    NO_TEXT_BLOCK = 'Text block with `hash` no found'


class TextBlockListView(ListAPIView):
    parser_classes = (JSONParser,)
    serializer_class = SimpleTextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.text_objects.all()

    @swagger_auto_schema(operation_id='all_text_blocks')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TopTextBlocksView(ListAPIView):
    parser_classes = (JSONParser,)
    serializer_class = SimpleTextBlockSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self) -> QuerySet[TextBlock]:
        queryset = cache.get('top_text_blocks_queryset')
        if queryset is None:                
            queryset = TextBlock.text_objects.order_by('-view_count')
            if queryset.count() > 10:
                queryset = queryset[:10]
            cache.set('top_text_blocks_queryset', queryset, timeout=1000)
        return queryset

    @swagger_auto_schema(operation_id='top_text_blocks')
    def get(self, request: Request) -> Response:
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TextsForUser(ListAPIView):
    parser_classes = (JSONParser,)
    serializer_class = SimpleTextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.text_objects.all()

    @swagger_auto_schema(operation_id='text_blocks_for_user')
    def get(self, request: Request, username: str) -> Response:
        user: User = User.objects.filter(username=username).first()
        if not user:
            return Response({'error': ErrorMessages.NO_USER.value},
                            status=status.HTTP_404_NOT_FOUND)
        text_blocks: QuerySet[TextBlock] = self.queryset.filter(author=user)
        serializer = self.serializer_class(text_blocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def generate_hashes(num_hashes: int) -> None:
    hashes: List[str] = cache.get('hash_generator_cache_key', [])
    if len(hashes) < num_hashes:
        new_hashes: List[str] = []
        for _ in range(num_hashes):
            hash_value: str =\
                hash_generator.create_unique_hash()
            new_hashes.append(hash_value)
        hashes.extend(new_hashes)
        cache.set('hash_generator_cache_key', hashes)


class CustomThrottle(AnonRateThrottle,
                     UserRateThrottle):
    rate = '1/s'


class CreateTextBlockView(CreateAPIView):
    parser_classes = (JSONParser,)
    serializer_class = CUTextBlockSerializer
    permission_classes = (AllowAny,)
    throttle_classes = (CustomThrottle,)

    @swagger_auto_schema(operation_id='create_text_block')
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        hashes: List[str] = cache.get('hash_generator_cache_key', [])

        if len(hashes) > 0:
            hash_value: str = hashes.pop()
            cache.set('hash_generator_cache_key', hashes)
        else:
            with ThreadPoolExecutor() as executor:
                executor.submit(generate_hashes, 20)
            hash_value: str = hash_generator.create_unique_hash()

        current_user: User | AnonymousUser = request.user
        if isinstance(current_user, AnonymousUser):
            current_user = None
        serializer.save(author=current_user, hash=hash_value)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateTextBlockView(GenericAPIView):
    parser_classes = (JSONParser,)
    serializer_class = CUTextBlockSerializer
    queryset = TextBlock.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_id='update_text_block')
    def put(self, request: Request, hash: str) -> Response:
        text_block: TextBlock = self.queryset.filter(hash=hash).first()
        if not text_block:
            return Response({'error': ErrorMessages.NO_TEXT_BLOCK.value},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            text_block, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TextBlockDetailsView(RetrieveAPIView):
    parser_classes = (JSONParser,)
    serializer_class = TextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.text_objects.all()
    lookup_field = 'hash'

    @swagger_auto_schema(operation_id='text_block_detail')
    def get(self, request: Request, hash: str) -> Response:
        text_block: TextBlock = self.queryset.filter(hash=hash).first()
        if not text_block:
            return Response({'error': ErrorMessages.NO_TEXT_BLOCK.value},
                            status=status.HTTP_404_NOT_FOUND)    
        ip_address = request.META.get('REMOTE_ADDR')

        viewed_device, created = text_block.\
            viewed_devices.get_or_create(ip_address=ip_address)
        
        if created:
            text_block.view_count = F('view_count') + 1
            text_block.save()

        text_block.viewed_devices.add(viewed_device)
        text_block.refresh_from_db()
        serializer: TextBlockSerializer = self.serializer_class(text_block)    
        return Response(data=serializer.data, status=status.HTTP_200_OK)
