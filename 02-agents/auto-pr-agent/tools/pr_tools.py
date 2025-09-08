import os
import asyncio
import httpx
from xpander_sdk import register_tool
from types import SimpleNamespace

 


# ------------------ PR Analysis Helpers ------------------
def summarize_diff_impl(pr_files) -> str:
    if not pr_files:
        return "No files changed in this PR."

    summary_lines = []
    for f in pr_files:
        filename = f.filename
        additions = f.additions
        deletions = f.deletions
        changes = f.changes
        patch = getattr(f, "patch", "") or ""

        summary_lines.append(
            f"📄 **{filename}**\n"
            f"- ➕ {additions} additions\n"
            f"- ➖ {deletions} deletions\n"
            f"- 🔄 {changes} total changes\n"
        )
        if patch:
            diff_preview = "\n".join(patch.splitlines()[:10])
            summary_lines.append(f"```diff\n{diff_preview}\n...```")

        summary_lines.append("")

    return "\n".join(summary_lines)


def score_pr_impl(pr):
    score = 10
    if pr.additions > 500:
        score -= 2
    if pr.deletions > pr.additions:
        score -= 1
    if not pr.body:
        score -= 1
    return max(score, 0)


def generate_action_items_impl(pr):
    items = []
    if "fix" in pr.title.lower() and "test" not in pr.title.lower():
        items.append("Add test cases for the fix.")
    if pr.additions > 1000:
        items.append("Break the PR into smaller parts.")
    return items


def final_decision_impl(score):
    return "✅ Approve" if score >= 7 else "❌ Push Back"


# ------------------ Tools ------------------
@register_tool
async def send_slack_message(text: str) -> dict:
    """
    Send a formatted message to a Slack channel.
    Requires SLACK_BOT_TOKEN and SLACK_CHANNEL_ID in .env
    """
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL_ID")

    if not slack_token or not slack_channel:
        return {"status": "error", "message": "Slack credentials not set in environment variables."}

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": slack_channel,
        "text": text,
        "unfurl_links": False
    }

    try:
        max_retries = 3
        async with httpx.AsyncClient(timeout=15) as client:
            for attempt in range(max_retries):
                response = await client.post(
                    "https://slack.com/api/chat.postMessage",
                    headers=headers,
                    json=payload,
                )
                # Handle HTTP-level rate limiting
                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    wait_s = int(retry_after) if retry_after and retry_after.isdigit() else (2 ** attempt)
                    await asyncio.sleep(wait_s)
                    continue

                result = response.json()
                if result.get("ok"):
                    return {"status": "sent", "response": result}

                # Slack JSON-level rate limiting
                if result.get("error") == "ratelimited" and attempt < max_retries - 1:
                    retry_after = response.headers.get("Retry-After")
                    wait_s = int(retry_after) if retry_after and retry_after.isdigit() else (2 ** attempt)
                    await asyncio.sleep(wait_s)
                    continue

                # Other errors: return immediately
                return {
                    "status": "error",
                    "message": result.get("error") or "Slack API returned error",
                    "response": result,
                    "status_code": response.status_code,
                }

            return {
                "status": "error",
                "message": "Slack API rate-limited or transient failure after retries",
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Public tool wrappers for helper functions
@register_tool
async def summarize_diff(pr_files) -> str:
    return summarize_diff_impl(pr_files)


@register_tool
async def score_pr(pr) -> int:
    return score_pr_impl(pr)


@register_tool
async def generate_action_items(pr) -> list:
    return generate_action_items_impl(pr)


@register_tool
async def final_decision(score: int) -> str:
    return final_decision_impl(score)


# ------------------ Composite Tool: Review a PR ------------------
def extract_repo_and_number(pr_url: str):
    parts = pr_url.strip("/").split("/")
    repo_name = "/".join(parts[-4:-2])
    pr_number = int(parts[-1])
    return repo_name, pr_number


@register_tool
async def review_pr(pr_url: str) -> dict:
    """
    Analyze a GitHub PR: summarize diff, score, action items, final decision;
    attempt auto-merge if approved; send Slack summary.
    Requires GITHUB_TOKEN, SLACK_BOT_TOKEN, SLACK_CHANNEL_ID in env.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL_ID")

    if not github_token or not slack_token or not slack_channel:
        return {
            "status": "error",
            "message": "Missing GITHUB_TOKEN or Slack credentials in environment variables.",
        }

    repo_name, pr_number = extract_repo_and_number(pr_url)

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async with httpx.AsyncClient(timeout=20) as client:
        # Fetch PR metadata
        pr_resp = await client.get(f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}", headers=headers)
        if pr_resp.status_code >= 400:
            return {"status": "error", "message": f"GitHub PR fetch failed: {pr_resp.status_code}", "response": pr_resp.text}
        pr_json = pr_resp.json()

        # Fetch PR files
        files_resp = await client.get(
            f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files",
            headers=headers,
            params={"per_page": 300},
        )
        if files_resp.status_code >= 400:
            return {"status": "error", "message": f"GitHub files fetch failed: {files_resp.status_code}", "response": files_resp.text}
        files_json = files_resp.json()

    # Wrap JSON into simple objects
    pr_obj = SimpleNamespace(
        additions=pr_json.get("additions", 0),
        deletions=pr_json.get("deletions", 0),
        body=pr_json.get("body") or "",
        title=pr_json.get("title") or "",
    )
    pr_files_objs = [
        SimpleNamespace(
            filename=f.get("filename"),
            additions=f.get("additions", 0),
            deletions=f.get("deletions", 0),
            changes=f.get("changes", 0),
            patch=f.get("patch") or "",
        )
        for f in files_json
    ]

    # ✅ Use the registered tools
    summary = await summarize_diff(pr_files_objs)
    score = await score_pr(pr_obj)
    actions = await generate_action_items(pr_obj)
    decision = await final_decision(score)

    # Attempt auto-merge if approved
    merge_status = "Skipped"
    if decision == "✅ Approve":
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                merge_resp = await client.put(
                    f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/merge",
                    headers=headers,
                    json={"commit_message": "Auto-merged by PR Review Agent ✅"},
                )
                if merge_resp.status_code in (200, 201):
                    merge_status = "Success"
                else:
                    if merge_resp.status_code == 403:
                        # Provide actionable guidance on permissions/scopes
                        xoauth = merge_resp.headers.get("X-OAuth-Scopes", "")
                        xaccepted = merge_resp.headers.get("X-Accepted-OAuth-Scopes", "")
                        guidance = (
                            "GitHub returned 403 — token lacks permissions to merge. "
                            "Ensure the token has: Pull requests: write, Contents: write, Metadata: read, and explicit repo access (for fine-grained PATs). "
                            "Classic PATs should have 'repo' scope."
                        )
                        scopes_info = f"X-OAuth-Scopes={xoauth} | X-Accepted-OAuth-Scopes={xaccepted}" if (xoauth or xaccepted) else ""
                        merge_status = (
                            f"Failed: 403 Resource not accessible by token. {guidance} {scopes_info} "
                            f"Body: {merge_resp.text[:200]}"
                        )
                    else:
                        merge_status = f"Failed: {merge_resp.status_code} {merge_resp.text[:200]}"
        except Exception as e:
            merge_status = f"Failed: {str(e)}"

    # Send Slack summary
    action_lines = "\n- ".join(actions) if actions else "None"
    slack_msg = (
        f"*🔍 GitHub PR Review Summary*\n"
        f"📦 Repo: `{repo_name}`\n"
        f"🔢 PR: #{pr_number} — *{pr_json.get('title') or ''}*\n"
        f"📊 Score: `{score}/10`\n"
        f"📝 Summary:\n{summary[:1000]}\n\n"
        f"⚙️ Action Items:\n- {action_lines}\n\n"
        f"✅ Final Decision: *{decision}*\n"
        f"🔁 Merge Status: `{merge_status}`"
    )

    await send_slack_message(slack_msg)

    return {
        "title": pr_json.get("title") or "",
        "summary": summary,
        "score": score,
        "action_items": actions,
        "final_decision": decision,
        "merge_status": merge_status,
    }
