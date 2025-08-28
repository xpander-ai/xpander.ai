import os
from xpander_sdk import register_tool
from core.travel import (
    book_flight_impl,
    book_hotel_impl,
    log_expense_impl,
    check_policy_impl,
    summarize_expenses_impl,
    send_reminder_impl
)

@register_tool
async def ta_book_flight(origin: str, destination: str, date: str, budget: float) -> dict:
    """
    Book a flight from one airport to a destination on a given date within a budget.
    IMPORTANT: Convert origin and destination to IATA codes (e.g., Sheremetyevo airport -> SVO).
    User/session are inferred from the current conversation context.
    """
    uid = os.getenv("AGENT_USER_ID") or "default-user"
    sid = os.getenv("AGENT_SESSION_ID") or "default-session"
    return await book_flight_impl(origin, destination, date, budget, uid, sid)

@register_tool
async def ta_book_hotel(destination: str, nights: int, budget: float) -> dict:
    """
    Reserve a hotel at the specified location for a given number of nights within a nightly budget.
    User/session are inferred from the current conversation context.
    """
    uid = os.getenv("AGENT_USER_ID") or "default-user"
    sid = os.getenv("AGENT_SESSION_ID") or "default-session"
    return await book_hotel_impl(destination, nights, budget, uid, sid)

@register_tool
async def ta_log_expense(expense_type: str, amount: float, date: str) -> dict:
    """
    Log an expense entry by type, amount, and date for a given user and session.
    User/session are inferred from the current conversation context.
    """
    uid = os.getenv("AGENT_USER_ID") or "default-user"
    sid = os.getenv("AGENT_SESSION_ID") or "default-session"
    return await log_expense_impl(expense_type, amount, date, uid, sid)

@register_tool
async def ta_check_policy_violations() -> dict:
    """
    Check all logged expenses for policy violations (e.g., exceeding set limits).
    User/session are inferred from the current conversation context.
    """
    uid = os.getenv("AGENT_USER_ID") or "default-user"
    sid = os.getenv("AGENT_SESSION_ID") or "default-session"
    return await check_policy_impl(uid, sid)

@register_tool
async def ta_summarize_expenses() -> dict:
    """
    Generate a summary of total expenses, breakdown by category, and number of entries.
    User/session are inferred from the current conversation context.
    """
    uid = os.getenv("AGENT_USER_ID") or "default-user"
    sid = os.getenv("AGENT_SESSION_ID") or "default-session"
    return await summarize_expenses_impl(uid, sid)

@register_tool
async def ta_send_reminder(message: str | None = None) -> dict:
    """
    Send a reminder notification to the user to take action (e.g., upload receipts).
    User is inferred from the current conversation context.
    """
    uid = os.getenv("AGENT_USER_ID") or "default-user"
    return await send_reminder_impl(uid, message)
