from django.shortcuts import render

from django.http.response import HttpResponse, JsonResponse
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import api_view

from spinner.models import Color
from spinner.serializers import SpinnerSerializer
from spinner.utilities import isValidHex


# TODO:  Check naming and verify that things are the right convention after getting them to work. Possibly
# https://www.webforefront.com/django/multiplemodelrecords.html
# https://ilovedjango.com/django/rest-api-framework/views/tips/how-to-return-multiple-queryset-from-api-view/
# the spinner gets and deletes should be good/safe to work with now
@api_view(['GET', 'DELETE'])
def spinner(request):

    color_freq_pairs = Color.objects.all()
    if len(color_freq_pairs) == 0:
        return JsonResponse({'message': 'No color frequency pairs exist'}, 
            status=status.HTTP_417_EXPECTATION_FAILED)

    # GET all color/frequency pairs
    if request.method == 'GET':
        serialized_spinner = SpinnerSerializer(color_freq_pairs, many=True)
        return JsonResponse(serialized_spinner.data, safe=False, status=status.HTTP_200_OK)

    # DELETE clear all color/frequency pairs
    elif request.method == 'DELETE':
        color_freq_pairs.delete()
        return JsonResponse({'message': 'All color frequency pairs were deleted successfully'},
            status=status.HTTP_204_NO_CONTENT)
    
    # Is this needed?
    return HttpResponse(status=status.HTTP_404_NOT_FOUND)

# For all requests, https://www.bezkoder.com/django-crud-mysql-rest-framework/
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def color(request, color):

    # #FF0000 is read
    # #0000FF is blue
    # For all requests, check if color code is valid
    if not isValidHex(color):
        return JsonResponse({'message': 'An invalid hex code was entered'}, status=status.HTTP_400_BAD_REQUEST)

    color = '#'+color # append

    # This will either be one or zero.
    color_freq_pair = Color.objects.all().filter(hex=color)
    pair_exists = len(color_freq_pair)

    if request.method == "POST":
        if not pair_exists:
            serialized_obj = SpinnerSerializer(data={'hex': color})
            if serialized_obj.is_valid():
                serialized_obj.save() # Might not need to send new obj as json here
                return JsonResponse({'message': 'Added hex code: ' + color}, status=status.HTTP_201_CREATED)
            return JsonResponse({'message': 'An error occurred while serializing the Color'}, status=status.HTTP_400_BAD_REQUEST)
        # If the color does exist
        return JsonResponse({'message': 'The hex code: ' + color + ' already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # The rest of the requests will handle the pair not existing the same way
    if not pair_exists:
        return JsonResponse({'message': 'The hex code: ' + color + ' does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "GET":
       # color_freq_pair = SpinnerSerializer(color_freq_pair)
        color_freq_pair = list(color_freq_pair.values('frequency'))
        return JsonResponse(color_freq_pair[0], safe=False, status=status.HTTP_200_OK)

    # Should these look for errors and if so how?
    if request.method == "PUT":
        color_freq_pair.update(frequency = F('frequency') + 1)
        return HttpResponse(status=status.HTTP_200_OK)
    
    if request.method == "DELETE":
        color_freq_pair.delete()
        return HttpResponse(status=status.HTTP_200_OK)

    # Is this needed?
    return HttpResponse(status=status.HTTP_404_NOT_FOUND)