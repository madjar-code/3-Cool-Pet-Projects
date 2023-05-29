from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from texts.models import TextBlock
from .serializers import TextBlockSerializer


class TextBlockDetailsView(RetrieveAPIView):
    serializer_class = TextBlockSerializer
    permission_classes = (AllowAny,)
    queryset = TextBlock.active_objects.all()
    lookup_field = 'hash'

    def retrieve(self, request: Request, hash: str) -> Response:
        text_block: TextBlock = TextBlock.active_objects.\
            filter(hash=hash).first()
        if not text_block:
            return Response({'error': 'Object not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer: TextBlockSerializer = self.get_serializer(text_block)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)
