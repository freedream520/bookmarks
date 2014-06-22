from django.http import HttpResponse
from django.shortcuts import render
from photos.models import Photo
import json

def add_photo(request):
    if request.method == 'POST':
        username = request.user
        create_time = request.POST['create_time']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        location = request.POST['location']
        image = request.FILES['image']
        image_type = request.POST['type']
        description = request.POST['description']

        photo = Photo(username=username,
                      create_time=create_time,
                      latitude=latitude,
                      longitude=longitude,
                      location=location,
                      image=image,
                      type=image_type,
                      description=description
                      )
        photo.save()

        response_code = json.dump([{'code': 1, 'msg': 'success'}])
        return HttpResponse(response_code)