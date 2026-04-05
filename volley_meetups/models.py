from django.db import models


class Court(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)  # 地址
    equipment = models.TextField(blank=True)  # 設備（球、網、空調、飲水等）
    floor_type = models.CharField(max_length=50, blank=True)  # 木地板、PU、室外等
    notes = models.TextField(blank=True)  # 補充說明
    created_at = models.DateTimeField(auto_now_add=True)


# class Player(models.Model):
#     name = models.CharField(max_length=100)  # 玩家名字
#     level = models.CharField(max_length=50, blank=True)  # 程度（初、中、高）
#     notes = models.TextField(blank=True)  # 特性、位置、打法等
#     created_at = models.DateTimeField(auto_now_add=True)


class SeasonalSlot(models.Model):
    court = models.ForeignKey(
        Court, on_delete=models.SET_NULL, null=True
    )  # 本次活動在哪個球場
    weekday = models.DateField()  # 星期幾
    start_time = models.TimeField(blank=True, null=True)  # 開始時間
    end_time = models.TimeField(blank=True, null=True)  # 結束時間
    level = models.IntegerField(blank=True, null=True)  # 規定程度
    players = models.ManyToManyField(Player, blank=True)  # 參加的玩家名單（可不寫）
    cost = models.IntegerField(blank=True, null=True)  # 場地費（你付的）


class Meetup(models.Model):
    date = models.DateField()  # 日期
    start_time = models.TimeField(blank=True, null=True)  # 開始時間
    end_time = models.TimeField(blank=True, null=True)  # 結束時間
    intensity = models.IntegerField(blank=True, null=True)  # 強度（1–5）
    your_performance = models.IntegerField(
        blank=True, null=True
    )  # 自己當天的評價（1–5）
    notes = models.TextField(blank=True)  # 今日心得
    players = models.ManyToManyField(Player, blank=True)  # 參加的玩家名單（可不寫）
    cost = models.IntegerField(blank=True, null=True)  # 場地費（你付的）
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
