from rest_framework import serializers
from spinner.models import Color


class SpinnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ('id',
                  'hex',
                  'frequency')