from langchain.output_parsers.enum import EnumOutputParser

from enum import Enum


class IsJeju(Enum):
    YES = "YES"
    NO = "NO"


class RestaurantOrTourSpot(Enum):
    RESTAURANT = "RESTAURANT"
    TOUR_SPOT = "TOUR_SPOT"


is_jeju_parser = EnumOutputParser(enum=IsJeju)
restaurant_or_tour_spot_parser = EnumOutputParser(enum=RestaurantOrTourSpot)
