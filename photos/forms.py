from django import forms
from photos.models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('user')

    def get_latitude(self):
        return self.clean_data['latitude']

    def get_longitude(self):
        return self.cleaned_data['longitude']

    def get_create_time(self):
        return self.cleaned_data['create_time']

    def get_location(self):
        return self.cleaned_data['location']

    def get_name(self):
        return self.cleaned_data['name']

    def get_type(self):
        return self.celeaned_data['type']

    def get_