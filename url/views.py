# /url/views.py
import hashlib
import re
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from url.models import URL
from url.serializers import URLSerializer

def redirect_original_url(request, hash):
    try:
        url = URL.objects.get(hash=hash)
        url.visits += 1  # Increment visits count
        url.save()
        regex = r"^(http|https)://"

        if re.search(regex, url.url):
            return redirect(url.url)
        return redirect("http://" + url.url)
    except URL.DoesNotExist:
        return HttpResponseNotFound("Short URL not found")


@api_view(['POST'])
def create_short_url(request):
    if 'url' in request.data:
        original_url = request.data['url']

        # Generate a unique hash for the URL
        hash_value = hashlib.md5(original_url.encode()).hexdigest()[:10]

        # Create a new URL object in the database
        url = URL.objects.create(hash=hash_value, url=original_url)

        # Return the shortened URL in the response
        return JsonResponse({'short_url': f'/url/{hash_value}/'}, status=200)

    return JsonResponse({'error': 'Invalid request data'}, status=400)

@api_view(['GET'])
def get_url_stats(request, hash):
    print("Denemee laaa url statas")
    try:
        url = URL.objects.get(hash=hash)
        serializer = URLSerializer(url)
        return Response(serializer.data)
    except URL.DoesNotExist:
        return Response({'error': 'Short URL not found'}, status=404)


def simple_ui(request):
    ## Get all urls
    urls = URL.objects.all()
    ## Render template
    return render(request, "index.html", {"urls": urls})