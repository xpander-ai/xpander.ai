from agno.tools import tool
from core.travel import (
    book_flight_impl,
    book_hotel_impl,
    log_expense_impl,
    check_policy_impl,
    summarize_expenses_impl,
    send_reminder_impl
)

@tool(
    name="FlightTool",
    description="Book a flight from one airport to a destination on a given date within a budget.You always have to comvert orign and destination to iata not actual names example: Sheremetyevo airport means SVO therefore the input will be SVO",
    show_result=True,
    stop_after_tool_call=True
)
async def book_flight(origin, destination, date, budget, user_id, session_id):
    return await book_flight_impl(origin, destination, date, budget, user_id, session_id)

@tool(
    name="HotelTool",
    description="Reserve a hotel at the specified location for a given number of nights within a nightly budget.",
    show_result=True
)
async def book_hotel(destination, nights, budget, user_id, session_id):
    return await book_hotel_impl(destination, nights, budget, user_id, session_id)

@tool(
    name="ExpenseTool",
    description="Log an expense entry by type, amount, and date for a given user and session.",
    show_result=True
)
async def log_expense(expense_type, amount, date, user_id, session_id):
    return await log_expense_impl(expense_type, amount, date, user_id, session_id)

@tool(
    name="PolicyTool",
    description="Check all logged expenses for policy violations (e.g., exceeding set limits).",
    show_result=True
)
async def check_policy_violations(user_id, session_id):
    return await check_policy_impl(user_id, session_id)

@tool(
    name="SummaryTool",
    description="Generate a summary of total expenses, breakdown by category, and number of entries.",
    show_result=True
)
async def summarize_expenses(user_id, session_id):
    return await summarize_expenses_impl(user_id, session_id)

@tool(
    name="ReminderTool",
    description="Send a reminder notification to the user to take action (e.g., upload receipts).",
    show_result=True
)
async def send_reminder(user_id, message):
    return await send_reminder_impl(user_id, message) 