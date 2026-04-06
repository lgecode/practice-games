from email.policy import default
from django.db import models
from .choices import Weekday, Level, NetHeight, MeetupGender, RevisitIntention


class Court(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200, blank=True, default="")
    address = models.CharField(max_length=300, blank=True, default="")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


# class Player(models.Model):
#     name = models.CharField(max_length=100)  # 玩家名字
#     level = models.CharField(max_length=50, blank=True)  # 程度（初、中、高）
#     notes = models.TextField(blank=True)  # 特性、位置、打法等
#     created_at = models.DateTimeField(auto_now_add=True)


class SeasonalSlot(models.Model):
    court = models.ForeignKey(Court, on_delete=models.SET_NULL, null=True)
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    levels = models.JSONField(blank=True, default=list)
    # players = models.ManyToManyField(Player, blank=True)


class Meetup(models.Model):
    seasonal_slot = models.ForeignKey(
        SeasonalSlot, on_delete=models.SET_NULL, null=True
    )
    court = models.ForeignKey(Court, on_delete=models.SET_NULL, null=True)
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    net_height = models.CharField(
        max_length=2, choices=NetHeight.choices, blank=True, default=""
    )
    gender = models.CharField(
        max_length=2, choices=MeetupGender.choices, blank=True, default=""
    )
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    levels = models.JSONField(blank=True, default=list)
    cost = models.IntegerField(blank=True, null=True)
    # players = models.ManyToManyField(Player, blank=True)
    notes = models.TextField(blank=True, default="")


class Review(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    level = models.CharField(
        max_length=2, choices=Level.choices, blank=True, default=""
    )
    content = models.TextField(blank=True, default="")
    revisit_intention = models.CharField(
        max_length=20, choices=RevisitIntention.choices, blank=True, default=""
    )
    created_at = models.DateTimeField(auto_now_add=True)
