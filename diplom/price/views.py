from .serializers import ProgramSerializer
from .models import Program
from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response


class ProgramListView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [AllowAny, ]
    @extend_schema(
        request=ProgramSerializer,
        responses={
            201: ProgramSerializer,
            204: {"default": []},
            400: {"default": "Bad request"},

        },
        description="Цены"  
    )
    def get(self, request):
        price = Program.objects.all()
        serializer = ProgramSerializer(price, many=True)
        return Response(serializer.data)
