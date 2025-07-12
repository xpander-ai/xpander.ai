<h3 align="center">
  <a name="readme-top"></a>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../../images/Purple%20Logo%20White%20text.png">
    <img
      src="../../images/Purple%20Logo%20Black%20Text.png"
      style="max-width: 100%; height: auto; width: auto; max-height: 170px;"
      alt="xpander.ai Logo"
    >
  </picture>
</h3>

<div align="center">
  <h1>Xpander.ai Travel & Expense Assistant</h1>

<a href="https://pepy.tech/projects/xpander-sdk"><img src="https://static.pepy.tech/badge/xpander-sdk/month"></a>
<a href="https://github.com/xpander-ai/xpander.ai/blob/main/LICENSE"><img src="https://img.shields.io/github/license/xpander-ai/xpander.ai" alt="License"></a> <a href="https://pypi.org/project/xpander-sdk"><img src="https://img.shields.io/pypi/v/xpander-sdk" alt="PyPI Version"></a> <a href="https://npmjs.com/package/xpander-sdk"><img src="https://img.shields.io/npm/v/xpander-sdk" alt="NPM Version"></a> <a href="https://app.xpander.ai"><img src="https://img.shields.io/badge/platform-login-30a46c" alt="Platform Login"></a>

</div>



## Overview

An intelligent AI-powered assistant for seamless **business travel bookings** and **expense tracking**, built using the **Xpander SDK** and **Agno Framework**.



## Quick Start

```bash
# Clone the repository
 git clone [repository-url]
 cd Xpander_Travel_Assisstant

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API credentials
```

## Features

- **Flight Booking**: Book flights using IATA airport codes (e.g., `SVO` for Sheremetyevo).
- **Hotel Reservations**: Reserve hotels with customizable duration, location, and budget.
- **Trip Planning**: Smart bundling of flight + hotel based on your budget preferences.
- **Expense Logging**: Log travel or business expenses by category (e.g., meals, taxi, lodging).
- **Policy Compliance**: Auto-detect and flag violations against company policies.
- **Summaries & Reports**: Generate clear, categorized expense summaries for reporting.
- **Automated Reminders**: Slack-based reminders for pending expense submissions.


## Project Structure

```
Xpander_Travel_Assisstant/
├── core/                   # Core business logic
│   └── travel.py
├── tools/                  # AI tool wrappers
│   └── travel_tools.py
├── orchestrator/           # Agent orchestration logic
│   └── agno_agent.py
├── main.py                 # CLI entry point
├── xpander_handler.py      # Xpander event processing
├── xpander_config.json     # Xpander bot configuration
└── Dockerfile              # Container setup
```



## Prerequisites

- Python `3.8+`
- Access to the **Xpander SDK**
- API keys for:
  - [Aviationstack](https://aviationstack.com/)
  - [Slack Bot API](https://api.slack.com/)
  - [Nebius AI](https://studio.nebius.com/)



## Environment Configuration

Create a `.env` file with the following:

```env
AVIATIONSTACK_KEY=your_aviationstack_key
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_CHANNEL_ID=your_channel_id
NEBIUS_API_KEY=your_nebius_key
```


## Usage

### CLI Mode

```bash
python main.py
```

### Xpander UI Mode

```bash
python xpander_handler.py
```

> 💡 **Note**: You must use your own Xpander account credentials. The provided `xpander_config.json` is tied to a specific user and **cannot be reused** across accounts.
> Ensure you configure your own API keys and authentication details before proceeding.

Once the script is running, follow the terminal prompts. You’ll receive **personalized BAAS (Backend-as-a-Service) links** — simply open them in your browser to begin interacting with the Xpander-powered UI.

### Docker Mode

```bash
docker build -t xpander-travel .
docker run -p 8080:8080 xpander-travel
```



## Example Interactions

**Flight Booking**

```
You: Book a flight from SVO to JFK next week
Assistant: Searching for flights from Sheremetyevo (SVO) to New York (JFK)...
```

**Expense Logging**

```
You: Log an expense of $150 for taxi
Assistant: Logging taxi expense...
```

---

## 🛠️ Development Guide

### Adding a New Feature

1. **Define logic in `core/`:**
   ```python
   # core/your_feature.py
   async def your_feature_impl():
       # Your feature logic here
   ```
2. **Wrap as a tool in `tools/`:**
   ```python
   # tools/your_tools.py
   @tool(name="YourTool")
   async def your_tool():
       return await your_feature_impl()
   ```
3. **Register in the agent:**
   Add to `orchestrator/agno_agent.py`.



## API Reference

### Flight Booking API

- Use IATA codes (e.g., `DEL`, `JFK`)
- Date format: `YYYY-MM-DD`
- Optional: `budget` in local currency

### Hotel Booking API

- Use city name (e.g., "Paris")
- Specify `duration` in nights
- Budget is per night



## 🤝 Contributing

1. Fork the repo
2. Create a new feature branch
3. Commit and push your changes
4. Submit a Pull Request (PR)



## 📝 License

MIT License