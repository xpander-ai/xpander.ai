import sqlite3
import os
import requests
import certifi
import json

os.environ["CURL_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()

DB_PATH = "travel_expenses.db"

# --- INIT DB ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            session_id TEXT,
            type TEXT,
            destination TEXT,
            date TEXT,
            nights INTEGER,
            price REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            session_id TEXT,
            type TEXT,
            amount REAL,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

AVIATIONSTACK_KEY = os.environ.get("AVIATIONSTACK_KEY")

def date_only(dt_str):
    return dt_str.split("T")[0] if dt_str else None

async def book_flight_impl(origin, destination, date, budget, user_id, session_id):
    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": AVIATIONSTACK_KEY,
        "limit": 100
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        flights = response.json().get("data", [])
    except Exception as e:
        return {"status": "error", "message": str(e)}
    for flight in flights:
        dep = flight.get("departure", {})
        arr = flight.get("arrival", {})
        flight_date = date_only(dep.get("scheduled"))
        if (
            dep.get("iata") == origin and
            arr.get("iata") == destination and
            flight_date == date
        ):
            airline = flight["airline"]["name"]
            flight_number = flight["flight"]["iata"]
            departure_time = dep["scheduled"]
            arrival_time = arr["scheduled"]
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bookings (user_id, session_id, type, destination, date, price)
                VALUES (?, ?, 'flight', ?, ?, ?)
            ''', (user_id, session_id, destination, departure_time, float(budget)))
            conn.commit()
            conn.close()
            return {
                "status": "booked",
                "message": (
                    f"✅ Your flight has been booked!\n\n"
                    f"✈️ **{airline} {flight_number}**\n"
                    f"📍 From: {origin} → To: {destination}\n"
                    f"🕒 Departure: {departure_time}\n"
                    f"🕓 Arrival: {arrival_time}\n"
                    f"💰 Price: ₹{budget}"
                ),
                "flight": {
                    "airline": airline,
                    "flight_number": flight_number,
                    "from": origin,
                    "to": destination,
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "price": budget
                }
            }
    return {"status": "no flights found"}

async def book_hotel_impl(destination, nights, budget, user_id, session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (user_id, session_id, type, destination, nights, price)
        VALUES (?, ?, 'hotel', ?, ?, ?)
    ''', (user_id, session_id, destination, nights, budget))
    conn.commit()
    conn.close()
    return {"status": "booked", "hotel": {
        "location": destination, "nights": nights, "price_per_night": budget
    }}

async def log_expense_impl(expense_type, amount, date, user_id, session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (user_id, session_id, type, amount, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, session_id, expense_type, amount, date))
    conn.commit()
    conn.close()
    return {"status": "logged", "expense": {
        "type": expense_type, "amount": amount, "date": date
    }}

async def check_policy_impl(user_id, session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT type, amount FROM expenses
        WHERE user_id = ? AND session_id = ?
    ''', (user_id, session_id))
    rows = cursor.fetchall()
    conn.close()
    violations = [
        {"type": t, "reason": "Exceeds allowed limit", "amount": a}
        for t, a in rows if a > 5000
    ]
    return {"violations": violations}

async def summarize_expenses_impl(user_id, session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT type, amount FROM expenses
        WHERE user_id = ? AND session_id = ?
    ''', (user_id, session_id))
    rows = cursor.fetchall()
    conn.close()
    total = sum(a for _, a in rows)
    categories = {}
    for t, a in rows:
        categories[t] = categories.get(t, 0) + a
    return {"total": total, "categories": categories, "count": len(rows)}

async def send_reminder_impl(user_id, message):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_CHANNEL_ID")
    if not slack_token or not slack_channel:
        return {
            "status": "error",
            "message": "Slack credentials not set in environment variables."
        }
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": slack_channel,
        "text": message or f"Reminder for user {user_id}: Please take the required action (e.g., upload receipts).",
        "unfurl_links": False
    }
    try:
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            data=json.dumps(payload)
        )
        result = response.json()
        if result.get("ok"):
            return {"status": "reminder_sent", "user": user_id, "slack_ts": result.get("ts")}
        else:
            return {"status": "error", "message": result.get("error")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Initialize DB on import
init_db() 