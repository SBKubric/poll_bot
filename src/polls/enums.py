import enum


class PetAdvisorStatesEnum(enum.Enum, str):
    GREETING = "greeting"
    CAT_OR_DOG = "cat_or_dog"
    CALM_OR_ACTIVE = "calm_or_active"
    SMALL_OR_LARGE = "small_or_large"
    INDEPENDENT_OR_NOT = "independent_or_not"
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


class IndependanceEnum(enum.Enum, str):
    INDEPENDENT = "independent"
    NOT_INDEPENDENT = "not_independent"
    NOT_SET = "not_set"


class SizeEnum(enum.Enum, str):
    SMALL = "small"
    LARGE = "large"
    NOT_SET = "not_set"


class HairLengthEnum(enum.Enum, str):
    SHORT = "short"
    LONG = "long"
    NOT_SET = "not_set"


class HairynessEnum(enum.Enum, str):
    HAIRY = "hairy"
    NOT_HAIRY = "not_hairy"
    NOT_SET = "not_set"
