from typing import Sequence

from langgraph.graph import END, MessageGraph
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.prebuilt import ToolNode

from .chains import validator_chain, restaurant_or_tour_spot_chain
from .schemas import IsJeju, RestaurantOrTourSpot


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
        return END
    elif "TOUR_SPOT" in (state[-1].content).upper():
        return END
    else:
        return END


# Node List
VALIDATOR = "validator"
RESTAURANT_OR_TOUR_SPOT = "restaurant_or_tour_spot"

# Add Nodes
builder = MessageGraph()
builder.add_node(VALIDATOR, validate_node)
builder.add_node(RESTAURANT_OR_TOUR_SPOT, restaurant_or_tour_spot_node)

# Add Edges
builder.set_entry_point(VALIDATOR)
builder.add_conditional_edges(
    VALIDATOR, decide_next_node, [RESTAURANT_OR_TOUR_SPOT, END]
)
builder.add_conditional_edges(RESTAURANT_OR_TOUR_SPOT, decide_next_node2, [END, END])

graph = builder.compile()


__all__ = ["graph"]
