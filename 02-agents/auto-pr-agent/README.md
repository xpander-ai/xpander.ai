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
├── tools/
│   └── pr_tools.py         # PR review tools (GitHub REST + Slack)
├── xpander_handler.py      # Agent orchestrator (Agno + Xpander SDK)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container setup
└── .env                    # Environment variables (not committed)
```


##  Prerequisites

- Python 3.10+
- Access to the <b>Xpander SDK</b> (installed via requirements)
- GitHub token with repo:read and merge permissions
- Slack Bot token with chat:write and target channel ID
- OpenAI API key (for the Agno agent in `xpander_handler.py`)



## Environment Configuration

Create a `.env` file with the following keys:

```env
GITHUB_TOKEN=ghp_xxx_or_fine_grained_token
SLACK_BOT_TOKEN=xoxb-xxx
SLACK_CHANNEL_ID=C0123456789
OPENAI_API_KEY=sk-xxx
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

## Usage

### Run the Agent (streaming CLI / Xpander)

Start the agent orchestrator that can call tools like `review_pr` and stream responses:

```bash
python3 xpander_handler.py
```

> 💡 Use your own `xpander_config.json` and API credentials to avoid auth failures.

---

### Run as a Docker Container

```bash
# Build
docker build -t xpander-pr-review .

# Provide env at runtime (recommended) and execute agent
docker run --rm \
  -e GITHUB_TOKEN \
  -e SLACK_BOT_TOKEN \
  -e SLACK_CHANNEL_ID \
  -e OPENAI_API_KEY \
  xpander-pr-review python3 xpander_handler.py
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

1. Update scoring in `tools/pr_tools.py` (function `score_pr_impl`):

   ```python
   def score_pr_impl(pr):
       score = 10
       if pr.additions > 500:
           score -= 2
       if not pr.body:
           score -= 1
       # Add your custom rules here
       return max(score, 0)
   ```

2. Update final decision logic if needed.


## 📚 API Reference

- <b>GitHub PR Parsing</b>: Accepts PR URLs like `https://github.com/org/repo/pull/123`. Fetches PR metadata and files via GitHub REST (`httpx`).
- <b>Slack Messaging</b>: Sends a compact review summary to Slack using `chat.postMessage` with simple retry on rate limiting.
- <b>Auto‑Merge</b>: If the PR is approved (score ≥ 7), attempts a merge via the GitHub merge endpoint.



## 🤝 Contributing

1. Fork this repo
2. Create a new feature branch
3. Submit a pull request



## 📝 License

MIT License


