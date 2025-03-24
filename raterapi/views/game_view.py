from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Game
from .category_view import CategorySerializer


class GameSerializer(serializers.ModelSerializer):
     # Override default serialization to replace foreign keys
    # with expanded related resource. By default, this would
    # be a list of integers (e.g. [2, 4, 9])
    categories = CategorySerializer(many=True)

    # Declare that an ad-hoc property should be included in JSON
    is_owner = serializers.SerializerMethodField()

    # Function containing instructions for ad-hoc property
    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.created_by

    class Meta:
        model = Game
        fields = ['id', 'title', 'description', 'designer', 'year_released', 'number_of_players','play_time','recommended_age','created_by', 'categories','is_owner']


class GameViewSet(viewsets.ViewSet):

    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(
            games, 
            many=True, 
            context={'request': request}) # Allow serializer to access request
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        title = request.data.get('title')
        designer= request.data.get('designer')
        description = request.data.get('description')
        year_released= request.data.get('year_released')
        number_of_players=request.data.get('year_released')
        play_time=request.data.get('year_released')
        recommended_age=request.data.get('recommended_age')
       
    

        # Create a game database row first, so you have a
        # primary key to work with
        game = Game.objects.create(
            title=title,
            designer=designer,
            description=description,
            year_released=year_released,
            number_of_players=number_of_players,
            play_time=play_time,
            recommended_age=recommended_age,
            created_by=request.user)

        # Establish the many-to-many relationships
        category_ids = request.data.get('categories', [])
        game.categories.set(category_ids)

        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:

            game = Game.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this game?
            self.check_object_permissions(request, game)

            serializer = GameSerializer(data=request.data)
            if serializer.is_valid():
                game.title = serializer.validated_data['title']
                game.author = serializer.validated_data['author']
                game.isbn_number = serializer.validated_data['isbn_number']
                game.cover_image = serializer.validated_data['cover_image']
                game.save()

                category_ids = request.data.get('categories', [])
                game.categories.set(category_ids)

                serializer = GameSerializer(game, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            self.check_object_permissions(request, game)
            game.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)