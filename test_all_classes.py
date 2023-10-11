#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new User --")
my_user = User()
my_user.first_name = "Betty"
my_user.last_name = "Bar"
my_user.email = "airbnb@mail.com"
my_user.password = "root"
my_user.save()
print(my_user)


print("-- Create a new State --")
state = State()
state.name = "Kenya"
state.save()
print(state)

print("-- Create a new City --")
city = City()
city.state_id = state.id
city.name = "Kanairo"
city.save()
print(city)

print("-- Create a new Amenity --")
amenity = Amenity()
amenity.name = "Water"
amenity.save()
print(amenity)

print("-- Create a new Place --")
place = Place()
place.city_id = city.id
place.user_id = my_user.id
place.name = "Nice"
place.description = "Testing this"
place.number_rooms = 3
place.number_bathrooms = 2
place.max_guest = 2
place.price_per_night = 3000
place.latitude = 12.0
place.longitude = 1.0
place.amenity_ids = [amenity.id]
place.save()
print(place)

print("-- Create a new Review --")
review = Review()
review.place_id = place.id
review.user_id = my_user.id
review.text = "It was nice"
review.save()
print(review)
