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
  <h1>Xpander.ai GitHub PR Review Agent</h1>

<a href="https://pepy.tech/projects/xpander-sdk"><img src="https://static.pepy.tech/badge/xpander-sdk/month"></a>
<a href="https://github.com/xpander-ai/xpander.ai/blob/main/LICENSE"><img src="https://img.shields.io/github/license/xpander-ai/xpander.ai" alt="License"></a> <a href="https://pypi.org/project/xpander-sdk"><img src="https://img.shields.io/pypi/v/xpander-sdk" alt="PyPI Version"></a> <a href="https://npmjs.com/package/xpander-sdk"><img src="https://img.shields.io/npm/v/xpander-sdk" alt="NPM Version"></a> <a href="https://app.xpander.ai"><img src="https://img.shields.io/badge/platform-login-30a46c" alt="Platform Login"></a>

</div>



An intelligent AI-powered assistant for automated <b>GitHub pull request reviews</b>, <b>Slack-based summaries</b>, and optional <b>auto-merge</b>, powered by <b>Xpander SDK</b> and <b>Agno Framework</b>.


## 🚀 Features

- <b>Summary Generation</b>: Auto-summarizes code changes file-by-file in a clean, structured format.
- <b>Smart Scoring</b>: Assigns a PR score based on heuristics like size, test coverage, and description quality.
- <b>Action Recommendations</b>: Flags missing test cases, large diffs, or policy violations with suggestions.
- <b>Final Decisioning</b>: Produces a clear "✅ Approve" or "❌ Push Back" verdict.
- <b>Slack Integration</b>: Sends concise PR reports to Slack with action items and decision.
- <b>Auto-Merge Support</b>: Automatically merges approved PRs if no conflicts or branch rules block it.



## 🧱 Project Structure

```
Xpander_Auto_PR/
├── core/                   # Core PR review logic and utilities
│   ├── pr_review.py
│   └── slack.py
├── tools/                  # Tool wrapper used by agent
│   └── pr_tools.py
├── orchestrator/           # Agent orchestration logic
│   └── agno_agent.py
├── main.py                 # CLI entry point for agent conversation
├── xpander_handler.py      # Entry point for Xpander UI
├── xpander_config.json     # Xpander bot configuration
├── pr_reviews.db           # SQLite database for review history
└── Dockerfile              # Docker container setup
```


##  Prerequisites

- Python 3.10+
- Access to the <b>Xpander SDK</b>
- GitHub App Token for PR access
- API keys for:
  - [Slack Bot](https://api.slack.com/)
  - [Nebius AI](https://studio.nebius.com/)



## Environment Configuration

Create a `.env` file with the following keys:

```env
GITHUB_TOKEN=your_github_token
SLACK_BOT_TOKEN=your_slack_token
SLACK_CHANNEL_ID=your_channel_id
NEBIUS_API_KEY=your_nebius_key
```

---

## Installation

```bash
# Clone the repository
 git clone <repo>
 cd Xpander_Auto_PR

# Install dependencies
 pip install -r requirements.txt
```

---

##  Usage

### Run via CLI

```bash
python main.py
```

---

### Run via Xpander UI

To launch the Xpander assistant with full UI capability:

```bash
python xpander_handler.py
```

> 💡 Use your own `xpander_config.json` and API credentials to avoid auth failures.

---

### Run as a Docker Service

```bash
docker build -t xpander-pr-review .
docker run -p 8080:8080 xpander-pr-review
```

---

## Example Interactions

```
You: Review this PR — https://github.com/username/repo/pull/42
Agent: PR #42 in username/repo — Score: 9/10
Summary: 3 files changed, 120 additions, 10 deletions
Action Items: Add tests for new utility
Final Decision: ✅ Approve
Merge Status: Success
```

---

## Development Guide

### Add a New Review Heuristic

1. Update scoring in `core/pr_review.py`:

   ```python
   if "TODO" in pr.diff:
       score -= 1
   ```

2. Update final decision logic if needed.


## 📚 API Reference

- <b>GitHub PR Parsing</b>: Accepts standard PR URLs (`https://github.com/org/repo/pull/123`). Uses PyGithub for diff extraction.
- <b>Slack Messaging</b>: Uses `chat.postMessage` to deliver results. Merges PR automatically if score ≥ 7 and branch allows it.



## 🤝 Contributing

1. Fork this repo
2. Create a new feature branch
3. Submit a pull request



## 📝 License

Apache License 2.0


