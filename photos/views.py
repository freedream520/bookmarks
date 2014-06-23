from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from photos.models import Photo
import os
import json

UPLOAD_TO = "./upload/photos"

UPLOAD_SUCCESS = 0
ERROR_USER_INFO = UPLOAD_SUCCESS + 1
UNKNOW_ERROR = ERROR_USER_INFO + 1

def add_photo(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user.is_active:
            _save_photo(request, username)
            return HttpResponse(json.dump({'code': UPLOAD_SUCCESS, "msg": 'upload success'}))
        else:
            return HttpResponse(json.dump({'code': ERROR_USER_INFO, "msg": 'error user info'}))
    else:
        return HttpResponse(json.dump({'code': UNKNOW_ERROR, "msg": 'unknow error'}))

def _save_photo(request, username):
        create_time = request.POST['create_time']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        location = request.POST['location']
        image_name = request.POST['image_name']
        image_type = request.POST['type']
        description = request.POST['description']
        _handle_uploaded_file(request.FILES['image_file'], os.path.join(UPLOAD_TO, image_name))
        photo = Photo(username=username,
                      create_time=create_time,
                      latitude=latitude,
                      longitude=longitude,
                      location=location,
                      image_name=image_name,
                      type=image_type,
                      description=description
                      )
        photo.save()


def _handle_uploaded_file(f, save_path):
    with open(save_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)