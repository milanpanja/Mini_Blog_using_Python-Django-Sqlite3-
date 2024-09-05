from django.contrib import admin
from .models import Podt
# Register your models here.
@admin.register(Podt)
class PodtModelAdmin(admin.ModelAdmin):
    list_display=['id','title','desc']