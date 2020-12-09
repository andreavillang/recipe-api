from django.contrib.auth import get_user_model

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the users object
    """

    class Meta:
        # this line grabs the user model
        model = get_user_model()
        # this is required. We are making a list that states that I require these fields
        fields = ('email', 'password', 'name')
        # For the password, we have a variable kwards, stands for keyword arguements. 
        # This states that the password has some validation and restrictions in this case its the password.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it
        """
        # we made this function, now we just call it with the data we've already validated.
        return get_user_model().objects.create_user(**validated_data)
