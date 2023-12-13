import enum


class HasValueMixin:
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_  # type: ignore


class PetAdvisorStatesEnum(str, HasValueMixin, enum.Enum):
    GREETING = "greeting"
    CAT_OR_DOG = "cat_or_dog"
    CALM_OR_ACTIVE = "calm_or_active"
    SMALL_OR_LARGE = "small_or_large"
    INDEPENDENT_OR_NOT = "independent_or_not"
    SHORT_OR_LONG_HAIR = "short_or_long_hair"
    HAIRY_OR_NOT = "hairy_or_not"
    RESULT = "result"


class SpeciesEnum(str, HasValueMixin, enum.Enum):
    CAT = "cat"
    DOG = "dog"
    NOT_SET = "not_set"


class ActivityEnum(str, HasValueMixin, enum.Enum):
    CALM = "calm"
    ACTIVE = "active"
    NOT_SET = "not_set"


class IndependenceEnum(str, HasValueMixin, enum.Enum):
    INDEPENDENT = "independent"
    NOT_INDEPENDENT = "not_independent"
    NOT_SET = "not_set"


class SizeEnum(str, HasValueMixin, enum.Enum):
    SMALL = "small"
    LARGE = "large"
    NOT_SET = "not_set"


class HairLengthEnum(str, HasValueMixin, enum.Enum):
    SHORT = "short"
    LONG = "long"
    NOT_SET = "not_set"


class HairynessEnum(str, HasValueMixin, enum.Enum):
    HAIRY = "hairy"
    NOT_HAIRY = "not_hairy"
    NOT_SET = "not_set"
