import enum


class SpeciesEnum(enum.Enum, str):
    CAT = "cat"
    DOG = "dog"
    NOT_SET = "not_set"


class ActivityEnum(enum.Enum, str):
    CALM = "calm"
    ACTIVE = "active"
    NOT_SET = "not_set"


class HairLengthEnum(enum.Enum, str):
    SHORT = "short"
    LONG = "long"
    NOT_SET = "not_set"


class HairynessEnum(enum.Enum, str):
    HAIRY = "hairy"
    NOT_HAIRY = "not_hairy"
    NOT_SET = "not_set"
