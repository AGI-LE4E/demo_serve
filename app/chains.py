from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from dotenv import load_dotenv

from .schemas import is_jeju_parser, restaurant_or_tour_spot_parser
from .tools import find_location_by_keyword_from_csv

load_dotenv(override=True)

llm = ChatUpstage(base_url="https://api.upstage.ai/v1/solar")

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
            "You are an Assistance system responsible for extracting food name from the user's input."
            "Please extract the food name from the user's input and provide it. Food Name should be in Korean."
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

# Search for the location of the user's input
search_location_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an Assistance system responsible for searching the location based on the extracted keyword."
            "Below is the extracted keyword.",
        ),
        MessagesPlaceholder(variable_name="keywords"),
        MessagesPlaceholder(variable_name="category"),
        (
            "system",
            "Please search the location based on the extracted keyword."
            "find_location_by_keyword_from_csv - Find the location from the keyword."
            "You can use below tools to search the location.",
        ),
        MessagesPlaceholder(variable_name="tool_choice"),
    ]
)

tools = [find_location_by_keyword_from_csv]

search_location_chain = search_location_prompt | llm.bind_tools(tools)
