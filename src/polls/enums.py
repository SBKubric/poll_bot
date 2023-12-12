import enum


class PetAdvisorStatesEnum(enum.Enum, str):
    GREETING = "greeting"
    CAT_OR_DOG = "cat_or_dog"
    CALM_OR_ACTIVE = "calm_or_active"
    SHORT_OR_LONG_HAIR = "short_or_long_hair"
    HAIRY_OR_NOT = "hairy_or_not"
    RESULT = "result"


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
