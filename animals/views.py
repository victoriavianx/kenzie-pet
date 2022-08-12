from rest_framework.views import APIView, status, Request, Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http.response import Http404, HttpResponse
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
        animals = get_list_or_404(Animal)
        serializer = AnimalSerializer(animals, many=True)
        
        return Response(serializer.data)

class AnimalDetailView(APIView):
    def get(self, request: Request, animal_id: int) -> Response:
        try:
            animal = get_object_or_404(Animal, id=animal_id)
            serializer = AnimalSerializer(animal)
            
        except Http404:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

    def patch(self, request: Request, animal_id: int) -> Response:
        try:
            animal = get_object_or_404(Animal, id=animal_id)
            serializer = AnimalSerializer(animal, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

        except Http404:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer.save()

        return Response(serializer.data)
    
    def delete(self, request: Request, animal_id: int) -> Response:
        try:
            animal = get_object_or_404(Animal, id=animal_id)

        except Http404:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)

        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)