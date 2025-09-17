from datetime import datetime
from langchain.agents import Tool



def add_event_to_calendar(title: str, date: str, time: str, location: str = None, attendees: list = None) -> str:
    """
    Simulates adding an event to a calendar.

    Parameters:
        title (str): Event title.
        date (str): Event date in "YYYY-MM-DD".
        time (str): Event time in "HH:MM" (24-hour format).
        location (str, optional): Event location.
        attendees (list of str, optional): List of attendees.

    Returns:
        str: Confirmation message including the event details.
    """
    # Convert time into 12-hour AM/PM format for display
    try:
        time_formatted = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")
    except ValueError:
        time_formatted = time  # fallback if time format is invalid
    
    # Build confirmation message
    message = f"Event '{title}' on {date} at {time_formatted}"
    
    if location:
        message += f" in {location}"
    if attendees:
        message += f" with attendees: {', '.join(attendees)}"
    
    message += " successfully added."

    ###########
    # "add" an event to a simulated calendar system 
    ###########
    
    return message


def add_event_to_calendar_wrapper(tool_input: str) -> str:
    """Wrapper function that handles LangChain tool input format
    
    Args:
        tool_input (str): The input to the tool.
        the tool input is a json string all (keys and values are enclosed in double quotes) with the following keys:
            - title (str): Event title.
            - date (str): Event date in "YYYY-MM-DD".
            - time (str): Event time in "HH:MM" (24-hour format).
            - location (str, optional): Event location.
            - attendees (list of str, optional): List of attendees.

    Returns:
        str: The output of the tool.
    """
    import json
    
    # Parse the JSON input
    try:
        if isinstance(tool_input, str):
            params = json.loads(tool_input)
        else:
            params = tool_input
    except (json.JSONDecodeError, TypeError):
        return "Error: Invalid input format. Expected JSON with title, date, and time."
    
    # Call the original function with unpacked parameters
    return add_event_to_calendar(
        title=params.get('title'),
        date=params.get('date'),
        time=params.get('time'),
        location=params.get('location'),
        attendees=params.get('attendees')
    )




def get_add_event_to_calendar_tool() -> Tool:
    """
    Returns a Tool object that can be used to add an event to the calendar.

    Returns:
        Tool: A Tool object that can be used to add an event to the calendar.
    """
    tool_description = (
        "Adds an event to the calendar. "
        "Expected input parameters (dictionary): all (keys and values are enclosed in double quotes) "
        "- title (str): event title, required; "
        "- date (str): date in 'YYYY-MM-DD', required; "
        "- time (str): time in 'HH:MM' (24-hour) or 'HH:MM AM/PM', required; "
        "- location (str): optional; "
        "- attendees (list[str]): optional list of attendee names or emails."
    )

    return Tool(
        name='Add event to calendar',
        func=add_event_to_calendar_wrapper,
        description=tool_description,
    )
