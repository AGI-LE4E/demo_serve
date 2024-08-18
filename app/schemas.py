from langchain.output_parsers.enum import EnumOutputParser

from enum import Enum


class IsJeju(Enum):
    YES = "YES"
    NO = "NO"


is_jeju_parser = EnumOutputParser(enum=IsJeju)
