from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from texts.models import TextBlock
from .serializers import (
    SimpleTextBlockSerializer,
    TextBlockSerializer,
)


class TextBlockListView(ListAPIView):
    parser_classes = (JSONParser,)
    serializer_class = SimpleTextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.active_objects.all()


class TextBlockDetailsView(RetrieveAPIView):
    parser_classes = (JSONParser,)
    serializer_class = TextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.active_objects.all()
    lookup_field = 'hash'

    def retrieve(self, request: Request, hash: str) -> Response:
        text_block: TextBlock = self.queryset.filter(hash=hash).first()
        if not text_block:
            return Response({'error': 'Object not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer: TextBlockSerializer = self.serializer_class(text_block)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
