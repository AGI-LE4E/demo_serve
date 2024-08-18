from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers import CommaSeparatedListOutputParser

from dotenv import load_dotenv

from .schemas import is_jeju_parser, restaurant_or_tour_spot_parser

load_dotenv(override=True)

llm = ChatUpstage(base_url="https://api.upstage.ai/v1/solar")
list_parser = CommaSeparatedListOutputParser()

# Validate the user input to check if it is related to Jeju tourism
validate_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an Assistance system responsible for determining whether a user's input is related to Korea Jeju Island tourism."
            "Please check if the user's input is indeed a question about Jeju Island tourism, and if so, respond with 'YES' If it is not, respond with 'NO'"
            "Even if the input contains the keyword 'Jeju Island,' if the context is unrelated to tourism, please choose 'NO'"
            "Even if the keyword 'Jeju Island' is not included, if the question is related to Jeju Island tourism, please choose 'YES'"
            f"{is_jeju_parser.get_format_instructions()}"
            "Below is the user's input.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

validator_chain = validate_prompt | llm | is_jeju_parser

# Whether the user input is recommended by restaurants or tourist spots
restaurant_or_tour_spot_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an Assistance system responsible for choosing between recommending restaurants or tourist spots."
            "Please check the user's input and respond with 'RESTAURANT' if the user is asking for restaurant recommendations."
            "If the user is asking for tourist spot recommendations, please respond with 'TOUR_SPOT'"
            f"{restaurant_or_tour_spot_parser.get_format_instructions()}"
            "Below is the user's input.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

restaurant_or_tour_spot_chain = (
    restaurant_or_tour_spot_prompt | llm | restaurant_or_tour_spot_parser
)

# Extract the food information from the user input
food_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an Assistance system responsible for extracting food keyword from the user's input."
            "Please extract the food keyword from the user's input and provide it. Keyword should be in Korean."
            "Your response should be a list of comma separated values, eg: `foo, bar, baz`"
            "Below is the user's input.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

food_chain = food_prompt | llm

# Extract the tourist spot information from the user input
tour_spot_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an Assistance system responsible for extracting tourist spot information from the user's input."
            "Please extract the tourist spot information from the user's input and provide it. Keyword should be in Korean."
            "Your response should be a list of comma separated values, eg: `foo, bar, baz`"
            "Below is the user's input.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

tour_spot_chain = tour_spot_prompt | llm
