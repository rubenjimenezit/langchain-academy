# from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage

# messages: list[AIMessage | HumanMessage] = [AIMessage(content=f"So you said you were researching ocean mamals?", name="Model")]
# messages.append(HumanMessage(content=f"Yes, that's right.",name="Lance"))
# messages.append(AIMessage(content=f"Great, what would you like to learn about.", name="Model"))
# messages.append(HumanMessage(content=f"I want to learn about the best place to see Orcas in the US.", name="Lance"))

# # for m in messages:
# #     m.pretty_pprint()




# import os, getpass

# def _set_env(var: str):
#     if not os.environ.get(var):
#         os.environ[var] = getpass.getpass(f"{var}: ")

# _set_env("ANTHROPIC_API_KEY")




from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model_name="claude-haiku-4-5")  # type: ignore
# result = llm.invoke(messages)
# type(result)
# print("*** result.content ***")
# print(result.content)
# print("*** result.metadata ***")
# pprint(result.response_metadata)

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

llm_with_tools = llm.bind_tools([multiply])
# tool_call = llm_with_tools.invoke([HumanMessage(content=f"What is 2 multiplied by 3", name="Lance")])
# print("\n\n\n")
# print("*** tool_call.content ***")
# print(tool_call.content)
# print("*** tool_call.metadata ***")
# pprint(tool_call.response_metadata)





# from typing_extensions import TypedDict
# from langchain_core.messages import AnyMessage

# class MessagesState(TypedDict):
#     messages: list[AnyMessage]


# from typing import Annotated
# from langgraph.graph.message import add_messages

# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]

from langgraph.graph import MessagesState

# This class MessagesState is identical to the built-in — but the subclass is in place so you can easily add fields later without restructuring your graph.
# class MessagesState(MessagesState):
#     # Add any keys needed beyond messages, which is pre-built 
#     pass


from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
    
# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

# Render the graph as a PNG and open it in Windows (WSL environment)
import subprocess

png_data = graph.get_graph().draw_mermaid_png()
with open("/tmp/graph.png", "wb") as f:
    f.write(png_data)
subprocess.run(["explorer.exe", r"\\wsl$\Ubuntu\tmp\graph.png"])


messages = graph.invoke({"messages": HumanMessage(content="Hello!")})  #type: ignore
for m in messages['messages']:
    m.pretty_print()

messages = graph.invoke({"messages": HumanMessage(content="Multiply 2 and 3")})  #type: ignore
for m in messages['messages']:
    m.pretty_print()
