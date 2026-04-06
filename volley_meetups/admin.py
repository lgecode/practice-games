from django.contrib import admin

from .models import Court, SeasonalSlot, Meetup, Review


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    pass


@admin.register(SeasonalSlot)
class SeasonalSlotAdmin(admin.ModelAdmin):
    pass


@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
