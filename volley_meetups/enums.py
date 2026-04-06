from enum import IntEnum, StrEnum


class Weekday(IntEnum):
    SUN = 0
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6


class Level(StrEnum):
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    B_PLUS = "B+"
    A = "A"
    A_PLUS = "A+"
    S = "S"
    S_PLUS = "S+"


class NetHeight(StrEnum):
    MALE = "M"
    FEMALE = "F"
    MIXED = "X"


class MeetupGender(StrEnum):
    MALE = "M"
    FEMALE = "F"
    MIXED = "X"


class RevisitIntention(StrEnum):
    NEVER = "Never"
    MAYBE = "Maybe"
    NEUTRAL = "Neutral"
    AGREE = "Agree"
    STRONGLY_AGREE = "Strongly agree"
