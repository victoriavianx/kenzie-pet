from rest_framework.views import APIView, status, Request, Response
from .serializers import AnimalSerializer

class AnimalView(APIView):
    def post(self, request: Request):
        serializer = AnimalSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)