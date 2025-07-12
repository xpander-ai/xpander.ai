from agno.tools import tool
from github import Github
from Xpander_Auto_PR.core.pr_review import (
    summarize_diff, score_pr, generate_action_items,
    final_decision, store_review
)
from Xpander_Auto_PR.core.slack import send_slack_message
from dotenv import load_dotenv
import os

load_dotenv()

@tool(
    name="PRReviewTool",
    description="Analyze a GitHub PR, generate summary, score, action items, decision, and auto-merge if approved.",
    show_result=True,
    stop_after_tool_call=True
)
async def review_pr(pr_url: str):
    github_token = os.getenv("GITHUB_TOKEN")
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL_ID")

    if not github_token or not slack_token or not slack_channel:
        return {
            "status": "error",
            "message": "Missing GITHUB_TOKEN or Slack credentials in environment variables."
        }

    g = Github(github_token)
    repo_name, pr_number = extract_repo_and_number(pr_url)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr_files = pr.get_files()

    summary = summarize_diff(pr_files)
    score = score_pr(pr)
    actions = generate_action_items(pr)
    decision = final_decision(score)

    # Save review to DB
    store_review(repo_name, pr_number, pr.title, summary, score, actions, decision)

    # Attempt auto-merge if decision is Approve
    merge_status = "Skipped"
    if decision == "✅ Approve":
        try:
            pr.merge(commit_message="Auto-merged by PR Review Agent ✅")
            merge_status = "Success"
        except Exception as e:
            merge_status = f"Failed: {str(e)}"

    # Send Slack summary
    slack_msg = (
        f"*🔍 GitHub PR Review Summary*\n"
        f"📦 Repo: `{repo_name}`\n"
        f"🔢 PR: #{pr_number} — *{pr.title}*\n"
        f"📊 Score: `{score}/10`\n"
        f"📝 Summary:\n{summary[:1000]}\n\n"
        f"⚙️ Action Items:\n- {'\n- '.join(actions) if actions else 'None'}\n\n"
        f"✅ Final Decision: *{decision}*\n"
        f"🔁 Merge Status: `{merge_status}`"
    )

    send_slack_message(slack_msg)

    return {
        "title": pr.title,
        "summary": summary,
        "score": score,
        "action_items": actions,
        "final_decision": decision,
        "merge_status": merge_status
    }
def extract_repo_and_number(pr_url):
    parts = pr_url.strip("/").split("/")
    repo_name = "/".join(parts[-4:-2])
    pr_number = int(parts[-1])
    return repo_name, pr_number
