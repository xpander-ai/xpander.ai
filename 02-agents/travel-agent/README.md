# Travel Agent

An intelligent AI-powered assistant for seamless **business travel bookings** and **expense tracking**, built using the **Xpander SDK** and **Agno Framework**.

## Features

- **Flight Booking**: Book flights using IATA airport codes with real-time API integration and offline fallback
- **Hotel Reservations**: Reserve hotels with customizable duration, location, and budget
- **Trip Planning**: Smart bundling of flight + hotel based on your budget preferences
- **Expense Logging**: Log travel or business expenses by category with SQLite persistence
- **Policy Compliance**: Auto-detect and flag violations against company policies (₹5000+ limit)
- **Summaries & Reports**: Generate clear, categorized expense summaries for reporting
- **Automated Reminders**: Daily Slack-based reminders at 17:00 IST for pending submissions

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd travel-agent

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

## Creates new backend configuration
xpander agent new --name "travel-agent" --framework "agno"

## Downloads the backend configurtion locally
xpander agent init "travel-agent"

## Runs the agent locally
xpander agent dev
```

## Example Usage

Ask the agent questions like:

- "Book a flight from SVO to JFK on 2025-09-15 with budget ₹50000"
- "Plan a trip from SFO to JFK from 2025-09-01 to 2025-09-05 under $1000"
- "Log an expense of ₹3000 for taxi on 2025-08-20"
- "Check my policy violations"
- "Summarize my expenses"

## Capabilities

✅ Flight booking with IATA codes  
✅ Hotel reservations  
✅ Trip planning (flight + hotel)  
✅ Expense tracking and logging  
✅ Policy violation detection  
✅ Automated Slack reminders  
✅ SQLite-based persistence  

## Environment Configuration

Create a `.env` file with the following:

```env
# Required - Xpander Platform Configuration
XPANDER_API_KEY=your_xpander_api_key
XPANDER_ORGANIZATION_ID=your_organization_id
XPANDER_AGENT_ID=your_agent_id

# Required - OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Optional - Flight booking (has offline fallback)
AVIATIONSTACK_KEY=your_aviationstack_key

# Optional - Slack reminders
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_CHANNEL_ID=your_channel_id
```

## Project Structure

```
travel-agent/
├── core/
│   ├── __init__.py
│   └── travel.py           # Core business logic & database operations
├── tools/
│   ├── __init__.py
│   └── travel_tools.py     # Xpander SDK tool registrations
├── xpander_handler.py      # Agno agent orchestrator & task handler
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container setup
├── .gitignore
└── README.md
```

## Requirements

- Python 3.8+
- Xpander SDK configured with appropriate credentials
- Valid API keys for external services
- SQLite for data persistence

## License

MIT
