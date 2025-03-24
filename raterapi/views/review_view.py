from django.utils import timezone
from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from raterapi.models import Review, Game

class ReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ["id", "game", "user", "rating", "comment", "created_on", "is_owner"]
        read_only_fields = ["user"]

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review
        return self.context["request"].user == obj.user


class ReviewViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        # Get all reviews
        reviews = Review.objects.all()

        # Serialize the objects, and pass request to determine owner
        serializer = ReviewSerializer(reviews, many=True, context={"request": request})
        # Return the serialized data with 200 status codereturn
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            # Get the requested review
            review = Review.objects.get(pk=pk)
            # Serialize the object (make sure to pass the request as context)
            serializer = ReviewSerializer(review, context={"request": request})
            # Return the review with 200 status code
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Create a new instance of a review and assign property
        # values from the request payload using `request.data`
        rating = request.data.get("rating")
        comment = request.data.get("comment")
        try:
            chosen_game = Game.objects.get(pk=request.data["game"])
        except Game.DoesNotExist:
            return Response({"reason": "Invalid game id sent"}, status=status.HTTP_404_NOT_FOUND)
        

        # Save the review
        review = Review.objects.create(
            game=chosen_game,
            user=request.user,
            rating=rating,
            comment=comment,
            created_on=timezone.now(),
        )

        try:
            # Serialize the objects, and pass request as context
            serializer = ReviewSerializer(review, context={"request": request})
            # Return the serialized data with 201 status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            # Get the requested review
            review = Review.objects.get(pk=pk)

            # Check if the user has permission to delete
            # Will return 403 if authenticated user is not author
            if review.user.id != request.user.id:
                return Response('You are not the user who wrote this review',status=status.HTTP_403_FORBIDDEN)

            # Delete the review
            review.delete()

            # Return success but no body
            return Response("Review has been deleted",status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
