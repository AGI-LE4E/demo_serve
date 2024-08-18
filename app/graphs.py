from typing import Sequence

from langgraph.graph import END, MessageGraph
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.prebuilt import ToolNode

from .chains import validator_chain
from .schemas import IsJeju


# Define Nodes
## Defind Validate Node
def validate_node(state: Sequence[BaseMessage]):
    res: IsJeju = validator_chain.invoke(input={"messages": [state[-1].content]})

    return res.value


## Define Next Node Decider
def decide_next_node(state: Sequence[BaseMessage]):
    if "Yes" in state[-1].content:
        return END
    elif "No" in state[-1].content:
        return END
    else:
        return END


# Node List
VALIDATOR = "validator"

# Add Nodes
builder = MessageGraph()
builder.add_node(VALIDATOR, validate_node)

# Add Edges
builder.set_entry_point(VALIDATOR)
builder.add_conditional_edges(VALIDATOR, decide_next_node, [END, END])

graph = builder.compile()


__all__ = ["graph"]
