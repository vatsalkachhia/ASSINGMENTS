from langgraph.graph import StateGraph, END
from core.pydentic_models import AgentState


from core.tools import make_tool_node, tools_set_reasoning_layer, tools_set_action_layer
from core.components import llm_for_action_layer, action_layer, should_continue_action_layer, finalize_action_layer
from core.components import reasoning_layer, finalize_reasoning_layer, should_continue_reasoning_layer
from core.components import chat_bot_layer, should_continue_chat_bot, finalize_chat_bot, upload_layer



graph = StateGraph(AgentState)
# reasoning layer nodes
graph.add_node("reasoning_layer", reasoning_layer)
graph.add_node("finalize_reasoning_layer", finalize_reasoning_layer)

graph.add_node("reasoning_layer_tools", make_tool_node("reasoning_layer_messages", AgentState, tools_set_reasoning_layer))

# action layer nodes
graph.add_node("action_layer", action_layer)
graph.add_node("finalize_action_layer", finalize_action_layer)

graph.add_node("action_layer_tools", make_tool_node("action_layer_messages", AgentState, tools_set_action_layer))

# learning layer nodes
graph.add_node("chat_bot", chat_bot_layer)
graph.add_node("finalize_chat_bot", finalize_chat_bot)
graph.add_node("upload_layer", upload_layer)

# reasoning layer edges
graph.set_entry_point("reasoning_layer")

graph.add_conditional_edges(
    "reasoning_layer",
    should_continue_reasoning_layer,
    {
        "continue": "reasoning_layer_tools",
        "end": "finalize_reasoning_layer",
    },
)

graph.add_edge("reasoning_layer_tools", "reasoning_layer")
graph.add_edge("finalize_reasoning_layer", "action_layer")

# action layer edges
graph.add_conditional_edges(
    "action_layer",
    should_continue_action_layer,
    {
        "continue": "action_layer_tools",
        "end": "finalize_action_layer",
    },
)

graph.add_edge("action_layer_tools", "action_layer")
graph.add_edge("finalize_action_layer", "chat_bot")

# learning layer edges
graph.add_conditional_edges(
    "chat_bot",
    should_continue_chat_bot,
    {
        "continue": "chat_bot",  # Loop back to ask next question
        "end": "finalize_chat_bot",
    },
)

graph.add_edge("finalize_chat_bot", "upload_layer")
graph.add_edge("upload_layer", END)

app = graph.compile()

def print_stream(stream):
    for s in stream:
        if len(s["reasoning_layer_messages"]) == 0:
            continue
        message = s["reasoning_layer_messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()