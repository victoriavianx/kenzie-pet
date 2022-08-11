from rest_framework.views import APIView, status, Request, Response, exceptions
from .serializers import AnimalSerializer
from .models import Animal

class AnimalView(APIView):
    def post(self, request: Request) -> Response:
        serializer = AnimalSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)

class AnimalDetailView(APIView):
    def patch(self, request: Request, animal_id: int) -> Response:
        try:
            animal = Animal.objects.get(pk=animal_id)
            serializer = AnimalSerializer(animal, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
        except Animal.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except exceptions.ValidationError:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        serializer.save()

        return Response(serializer.data)