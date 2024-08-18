from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.openai_tools import (
    PydanticToolsParser,
)

from dotenv import load_dotenv

from .schemas import is_jeju_parser

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
