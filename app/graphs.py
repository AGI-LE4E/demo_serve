from typing import Sequence

from langgraph.graph import END, MessageGraph
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import ToolNode

from .chains import (
    validator_chain,
    restaurant_or_tour_spot_chain,
    food_chain,
    tour_spot_chain,
    search_location_chain,
)
from .tools import find_location_by_keyword_from_csv
from .schemas import IsJeju, RestaurantOrTourSpot

# Node List
VALIDATOR = "validator"
RESTAURANT_OR_TOUR_SPOT = "restaurant_or_tour_spot"
RESTAURANT = "restaurant"
TOUR_SPOT = "tour_spot"
SEARCH_LOCATION = "search_location"
SEARCH_TOOL = "search_tool"
search_tool_node = ToolNode([find_location_by_keyword_from_csv])


# Define Nodes
## Defind Validate Node
def validate_node(state: Sequence[BaseMessage]):
    res: IsJeju = validator_chain.invoke(input={"messages": [state[0].content]})

    return res.value


## Define Restaurant or Tour Spot Node
def restaurant_or_tour_spot_node(state: Sequence[BaseMessage]):
    res: RestaurantOrTourSpot = restaurant_or_tour_spot_chain.invoke(
        input={"messages": [state[0].content]}
    )

    return res.value


## Define Restaurant Node
def restaurant_node(state: Sequence[BaseMessage]):
    res = food_chain.invoke(input={"messages": [state[0].content]})

    return res.content


## Define Tour Spot Node
def tour_spot_node(state: Sequence[BaseMessage]):
    res = tour_spot_chain.invoke(input={"messages": [state[0].content]})

    return res.content


def search_location_node(state: Sequence[BaseMessage]):
    res = search_location_chain.invoke(
        input={
            "keywords": [state[-1].content],
            "category": [state[-2].content],
            "tool_choice": ["find_location_by_keyword_from_csv"],
        }
    )

    return res


## Define Next Node Decider
def decide_next_node(state: Sequence[BaseMessage]):
    if "YES" in (state[-1].content).upper():
        return RESTAURANT_OR_TOUR_SPOT
    elif "NO" in (state[-1].content).upper():
        return END
    else:
        return END


## Define Next Node Decider2
def decide_next_node2(state: Sequence[BaseMessage]):
    if "RESTAURANT" in (state[-1].content).upper():
        return RESTAURANT
    elif "TOUR_SPOT" in (state[-1].content).upper():
        return TOUR_SPOT
    else:
        return END


# Add Nodes
builder = MessageGraph()
builder.add_node(VALIDATOR, validate_node)
builder.add_node(RESTAURANT_OR_TOUR_SPOT, restaurant_or_tour_spot_node)
builder.add_node(RESTAURANT, restaurant_node)
builder.add_node(TOUR_SPOT, tour_spot_node)
builder.add_node(SEARCH_LOCATION, search_location_node)
builder.add_node(SEARCH_TOOL, search_tool_node)

# Add Edges
builder.set_entry_point(VALIDATOR)
builder.add_conditional_edges(
    VALIDATOR, decide_next_node, [RESTAURANT_OR_TOUR_SPOT, END]
)
builder.add_conditional_edges(
    RESTAURANT_OR_TOUR_SPOT, decide_next_node2, [RESTAURANT, TOUR_SPOT, END]
)
builder.add_edge(RESTAURANT, SEARCH_LOCATION)
builder.add_edge(TOUR_SPOT, SEARCH_LOCATION)
builder.add_edge(SEARCH_LOCATION, SEARCH_TOOL)
builder.add_edge(SEARCH_TOOL, END)

graph = builder.compile()


__all__ = ["graph"]
