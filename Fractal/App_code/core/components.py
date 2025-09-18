from core.pydentic_models import AgentState
from core.tools import tools_set_reasoning_layer, tools_set_action_layer
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
import json 

from core.dummy import recommend_actions_from_root

from utils.config_utils import load_config
from utils.llm import get_llm


config = load_config()


# Reasoning layer
llm_for_reasoning_layer = get_llm(model = config["agent"]["reasoning_layer"]["llm"]["model"])


def reasoning_layer(state: AgentState) -> AgentState:
    """
    reasoning layer
    """
    # print("reasoning_layer...")
    system_prompt = SystemMessage(
        content="You are a helpful assistant that finds the root cause of a defect based on the defect type and environmental conditions."\
            "if satisfactory response is received from tool and cause of issue is known then just show root cause given by tool if following format without addition text:"\
            "Root Cause: <root cause>"
    )

    # Build prompt internally from state (no user-provided prompt needed)
    defect_type = state.get("defect_type", "unknown")
    environment = state.get("environment", "unspecified")
    if len(state["reasoning_layer_messages"]) == 0:
        # print("running reasoning layer prompt....")
        prompt = (
            "Find the root cause of the defect based on the info below.\n"
            f"- defect type: {defect_type}\n"
            f"- environmental conditions: {environment}\n"
            "Respond with the likely root cause and brief reasoning."
        )
        state["reasoning_layer_messages"].append(HumanMessage(content=prompt))

    # Call the LLM with your internal messages
    response = llm_for_reasoning_layer.bind_tools(tools_set_reasoning_layer).invoke([system_prompt] + state["reasoning_layer_messages"])
    state["reasoning_layer_messages"].append(response)
    return state


def should_continue_reasoning_layer(state: AgentState): 
    messages = state["reasoning_layer_messages"]
    last_message = messages[-1]
    if not last_message.tool_calls: 
        return "end"
    else:
        return "continue"


def finalize_reasoning_layer(state: AgentState) -> AgentState:
    reasoning_layer_messages = state["reasoning_layer_messages"]
    last_message = reasoning_layer_messages[-1]
    state["reasoning_layer_output"] = last_message.content
    print("reasoning_layer_output", state["reasoning_layer_output"])
    return state


# Action layer
llm_for_action_layer = get_llm(model = config["agent"]["action_layer"]["llm"]["model"])


def action_layer(state: AgentState) -> AgentState:
    """
    reasoning layer
    """
    # print("action_layer...")
    system_prompt = ("You are a helpful assistant that can adjust spray parameters via PLC integration, trigger maintenance workflows, or inform human operators based on the defect type."\
        "based on the defect type, environmental conditions, root cause, and suggested solution you can take appropriate action to fix the issue."\
        "if issue is critical only then: trigger maintenance workflows, or inform human operators based on the issue type"\
        "once done with the action, just return the action taken in the following format:"\
        "Action Taken: [action taken + information received from tool]"
    )

    # Build prompt internally from state (no user-provided prompt needed)
    defect_type = state.get("defect_type", "unknown")
    issue_critical = state.get("issue_critical", False)

    environment = state.get("environment", "unspecified")
    temperature_c = environment.get("temperature_c", "unspecified")
    humidity_pct = environment.get("humidity_pct", "unspecified")
    spray_pressure_bar = environment.get("spray_pressure_bar", "unspecified")
    reasoning_layer_output = state.get("reasoning_layer_output", "unspecified")

    # Rule based later could be replaced with more advanced version
    solution_context = recommend_actions_from_root(defect_type, issue_critical, temperature_c, humidity_pct, spray_pressure_bar, reasoning_layer_output)


    if len(state["action_layer_messages"]) == 0:
        # print("running reasoning layer prompt....")
        prompt = (
            "Based on the defect type, environmental conditions, root cause, and suggested solution, you can take appropriate action to fix the issue."
            f"defect type: ```{defect_type}```"
            f"environmental conditions: ```{environment}```"
            f"root cause: ```{reasoning_layer_output}```"
            f"suggested solution: ```{solution_context}```"

        )
        state["action_layer_messages"].append(HumanMessage(content=prompt))

    # Call the LLM with your internal messages
    response = llm_for_action_layer.bind_tools(tools_set_action_layer).invoke([system_prompt] + state["action_layer_messages"])
    state["action_layer_messages"].append(response)
    return state


def should_continue_action_layer(state: AgentState): 
    messages = state["action_layer_messages"]
    last_message = messages[-1]
    if not last_message.tool_calls: 
        return "end"
    else:
        return "continue"


def finalize_action_layer(state: AgentState) -> AgentState:
    action_layer_messages = state["action_layer_messages"]
    last_message = action_layer_messages[-1]
    state["action_layer_output"] = last_message.content
    print("action_layer_output", state["action_layer_output"])
    return state

#learning layer
def chat_bot_layer(state: AgentState) -> AgentState:
    """
    Chat bot layer that asks questions and collects feedback
    """
    # Initialize flags if not present
    if not state.get("learning_layer_flags"):
        state["learning_layer_flags"] = {
            "confirmed_defect_type": False,
            "confirmed_root_cause": False, 
            "was_issue_resolved_by_suggested_changes": False
        }
    
    if not state.get("learning_layer_correct_values"):
        state["learning_layer_correct_values"] = {
            "defect_type": "",
            "root_cause": "",
            "issue_resolved": ""
        }
    
    # Questions to ask
    questions = [
        ("confirmed_defect_type", f"Was the detected defect type '{state.get('defect_type', 'unknown')}' correct? (yes/no): "),
        ("confirmed_root_cause", f"Was the detected root cause '{state.get('reasoning_layer_output', 'unknown')}' correct? (yes/no): "),
        ("was_issue_resolved_by_suggested_changes", f"Was the issue resolved by suggested changes '{state.get('action_layer_output', 'unknown')}'? (yes/no): ")
    ]
    
    # Find the first unanswered question
    for flag_key, question in questions:
        if not state["learning_layer_flags"][flag_key]:
            print(question)
            response = input().strip().lower()
            
            if response in ['yes', 'y']:
                state["learning_layer_flags"][flag_key] = True
                # Store the correct values
                if flag_key == "confirmed_defect_type":
                    state["learning_layer_correct_values"]["defect_type"] = state.get('defect_type', '')
                elif flag_key == "confirmed_root_cause":
                    state["learning_layer_correct_values"]["root_cause"] = state.get('reasoning_layer_output', '')
                elif flag_key == "was_issue_resolved_by_suggested_changes":
                    state["learning_layer_correct_values"]["issue_resolved"] = "yes"
                    state["suggestion_to_resolve_issue"] = ""
            elif response in ['no', 'n']:
                state["learning_layer_flags"][flag_key] = True
                # Ask for correct value
                if flag_key == "confirmed_defect_type":
                    correct_value = input("What is the correct defect type? ")
                    state["learning_layer_correct_values"]["defect_type"] = correct_value
                elif flag_key == "confirmed_root_cause":
                    correct_value = input("What is the correct root cause? ")
                    state["learning_layer_correct_values"]["root_cause"] = correct_value
                elif flag_key == "was_issue_resolved_by_suggested_changes":
                    state["learning_layer_correct_values"]["issue_resolved"] = "no"
                    correct_value = input("What would be optimal way to resolve this issue? ")
                    state["suggestion_to_resolve_issue"] = correct_value
                    
            break
    
    return state


def should_continue_chat_bot(state: AgentState) -> str:
    """Check if all questions have been answered"""
    flags = state.get("learning_layer_flags", {})
    
    # Check if all flags are True
    required_flags = ["confirmed_defect_type", "confirmed_root_cause", "was_issue_resolved_by_suggested_changes"]
    all_answered = all(flags.get(flag, False) for flag in required_flags)
    
    if all_answered:
        return "end"
    else:
        return "continue"


def finalize_chat_bot(state: AgentState) -> AgentState:
    """Finalize the chat bot layer"""
    print("\n=== Feedback Collection Complete ===")
    print("Collected Information:")
    print(f"- Defect Type Correct: {state['learning_layer_flags']['confirmed_defect_type']}")
    print(f"- Root Cause Correct: {state['learning_layer_flags']['confirmed_root_cause']}")  
    print(f"- Issue Resolved: {state['learning_layer_flags']['was_issue_resolved_by_suggested_changes']}")
    print(f"- Correct Values: {state['learning_layer_correct_values']}")
    return state


def upload_layer(state: AgentState) -> AgentState:
    """upload the data to upgrade responses"""
    # image, sensors, defect_type(current), defect_type(feedback), root_cause(current), root_cause(feedback)
    data  =  {
        "image": state["image"],
        "sensors":state["environment"],
        "detected_defect_type": state["defect_type"],
        "survey_defect_type": state["learning_layer_correct_values"]["defect_type"],
        "detected_root_cause": state["reasoning_layer_output"],
        "survey_root_cause": state["learning_layer_correct_values"]["root_cause"],
        "suggested_solution": state["action_layer_output"],
        "Issue_Resolved": state['learning_layer_flags']['was_issue_resolved_by_suggested_changes'],
        "suggestion_to_resolve_issue": state["suggestion_to_resolve_issue"]
    }

    with open(config["app"]["save_data_path"],"r") as f:
        json_data = json.load(f) 
    json_data.append(data)

    with open(config["app"]["save_data_path"],"w") as f:
         json.dump(json_data, f, indent=4) 
    print("Data send for improving response")
    
    return state