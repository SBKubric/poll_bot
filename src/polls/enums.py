import enum


class PetAdvisorStatesEnum(str, enum.Enum):
    GREETING = "greeting"
    CAT_OR_DOG = "cat_or_dog"
    CALM_OR_ACTIVE = "calm_or_active"
    SMALL_OR_LARGE = "small_or_large"
    INDEPENDENT_OR_NOT = "independent_or_not"
    SHORT_OR_LONG_HAIR = "short_or_long_hair"
    HAIRY_OR_NOT = "hairy_or_not"
    RESULT = "result"


class SpeciesEnum(str, enum.Enum):
    CAT = "cat"
    DOG = "dog"
    NOT_SET = "not_set"


class ActivityEnum(str, enum.Enum):
    CALM = "calm"
    ACTIVE = "active"
    NOT_SET = "not_set"


class IndependanceEnum(str, enum.Enum):
    INDEPENDANT = "independent"
    NOT_INDEPENDENT = "not_independent"
    NOT_SET = "not_set"


class SizeEnum(str, enum.Enum):
    SMALL = "small"
    LARGE = "large"
    NOT_SET = "not_set"


class HairLengthEnum(str, enum.Enum):
    SHORT = "short"
    LONG = "long"
    NOT_SET = "not_set"


class HairynessEnum(str, enum.Enum):
    HAIRY = "hairy"
    NOT_HAIRY = "not_hairy"
    NOT_SET = "not_set"
