from django.db import models
from .choices import Weekday, Level


class Court(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField( max_length=200, blank=True, default='')
    address = models.CharField(max_length=300, blank=True, default='')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


# class Player(models.Model):
#     name = models.CharField(max_length=100)  # 玩家名字
#     level = models.CharField(max_length=50, blank=True)  # 程度（初、中、高）
#     notes = models.TextField(blank=True)  # 特性、位置、打法等
#     created_at = models.DateTimeField(auto_now_add=True)


class SeasonalSlot(models.Model):
    court = models.ForeignKey(
        Court, on_delete=models.SET_NULL, null=True
    )
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    level = models.CharField(max_length=2, choices=Level.choices, blank=True, null=True)
    # players = models.ManyToManyField(Player, blank=True)


class Meetup(models.Model):
    seasonal_slot = models.ForeignKey(
        SeasonalSlot, on_delete=models.SET_NULL, null=True
    )
    date = models.DateField()
    # players = models.ManyToManyField(Player, blank=True)
    cost = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)


class Review(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)

    content = models.TextField()
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    """
會想再去嗎? 想 都可 (除非沒其他選擇) 完全不想
強度


    """
