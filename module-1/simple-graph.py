from typing_extensions import TypedDict

# State schema: defines the shared data structure passed between nodes
class State(TypedDict):
    graph_state: str

# Node 1: always runs first, appends "I am" to the state
def node_1(state: State) -> State:
    return {"graph_state": state["graph_state"] + "I am"}

# Node 2: happy outcome — appended when decide_mood returns "node_2"
def node_2(state: State) -> State:
    return {"graph_state": state["graph_state"] + " happy! :)"}

# Node 3: sad outcome — appended when decide_mood returns "node_3"
def node_3(state: State) -> State:
    return {"graph_state": state["graph_state"] + "  sad :("}

import random
from typing import Literal

# Conditional edge function: randomly routes to node_2 or node_3
def decide_mood(state: State) -> Literal["node_2", "node_3"]:
    return random.choice(["node_2", "node_3"])


from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

# Build the graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Define edges: START -> node_1, then branch based on mood, then END
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Compile the graph into a runnable
graph = builder.compile()

# Render the graph as a PNG and open it in Windows (WSL environment)
import subprocess

png_data = graph.get_graph().draw_mermaid_png()
with open("/tmp/graph.png", "wb") as f:
    f.write(png_data)
subprocess.run(["explorer.exe", r"\\wsl$\Ubuntu\tmp\graph.png"])


# Invoke the graph with an initial state and print the final result
result = graph.invoke({"graph_state": "Hi, this is Lance. "})
print(result)

