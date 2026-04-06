from django.db import models
from django.utils.translation import gettext_lazy as _

from . import enums


class Weekday(models.TextChoices):
    SUN = (enums.Weekday.SUN, _('Sunday'))
    MON = (enums.Weekday.MON, _('Monday'))
    TUE = (enums.Weekday.TUE, _('Tuesday'))
    WED = (enums.Weekday.WED, _('Wednesday'))
    THU = (enums.Weekday.THU, _('Thursday'))
    FRI = (enums.Weekday.FRI, _('Friday'))
    SAT = (enums.Weekday.SAT, _('Saturday'))


class Level(models.TextChoices):
    E = (enums.Level.E, _('E'))
    D = (enums.Level.D, _('D'))
    C = (enums.Level.C, _('C'))
    B = (enums.Level.B, _('B'))
    B_PLUS = (enums.Level.B_PLUS, _('B+'))
    A = (enums.Level.A, _('A'))
    A_PLUS = (enums.Level.A_PLUS, _('A+'))
    S = (enums.Level.S, _('S'))
    S_PLUS = (enums.Level.S_PLUS, _('S+'))