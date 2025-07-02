from django.contrib import admin

# Register your models here.
from django.contrib import admin
from helloworld.models import Helloworld
from .models import User, Lecture, Review
# Register your models here.
admin.site.register(Helloworld)

admin.site.register(User)
#admin.site.register(Manager)
admin.site.register(Lecture)
admin.site.register(Review)
