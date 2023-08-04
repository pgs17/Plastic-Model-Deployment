import PIL.Image
from pathlib import Path
import phonenumbers
from phonenumbers import geocoder
import math
import PIL.ExifTags
from geopy.geocoders import Nominatim

def geo(path):
    
    path=Path('C:/Users/Lenovo/DJI_0023.jpg')
    img=PIL.Image.open(path)

    exif={PIL.ExifTags.TAGS[k]:v
        for k,v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
      
        }
    n=exif['GPSInfo'][2]
    e=exif['GPSInfo'][4]
    ltd=(float)((((n[0]*60)+n[1])*60)+n[2])/60/60
    lng=(float)((((e[0]*60)+e[1])*60)+e[2])/60/60
    return ltd,lng


def live(number):
    divided=phonenumbers.parse(number)

    location=geocoder.description_for_number(divided,"en")
    geolocator=Nominatim(user_agent="geoapiExercises")
    locate=geocoder.description_for_number(divided,'en')
    location=geolocator.geocode(locate)
    lat=location.latitude
    lng=location.longitude
    return lat,lng

def dist(ltd1,lng1,ltd2,lng2):
    d=math.sqrt(((ltd1-ltd2)**2)+((lng1-lng2)**2))
    return d;
