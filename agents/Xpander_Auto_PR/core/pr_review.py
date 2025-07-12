import json
import sqlite3
import os
from github import Github
import difflib
from datetime import datetime

DB_PATH = "pr_reviews.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pr_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo TEXT,
            pr_number INTEGER,
            title TEXT,
            summary TEXT,
            score INTEGER,
            actions TEXT,
            decision TEXT,
            reviewed_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def summarize_diff(pr_files) -> str:
    if not pr_files:
        return "No files changed in this PR."

    summary_lines = []
    for f in pr_files:
        filename = f.filename
        additions = f.additions
        deletions = f.deletions
        changes = f.changes
        patch = f.patch or ""

        summary_lines.append(
            f"📄 **{filename}**\n"
            f"- ➕ {additions} additions\n"
            f"- ➖ {deletions} deletions\n"
            f"- 🔄 {changes} total changes\n"
        )
        if patch:
            # Keep patch short and clean for Slack (e.g., first 10 lines)
            diff_preview = "\n".join(patch.splitlines()[:10])
            summary_lines.append(f"```diff\n{diff_preview}\n...```")

        summary_lines.append("")  # spacing between files

    return "\n".join(summary_lines)


def score_pr(pr):
    score = 10
    if pr.additions > 500:
        score -= 2
    if pr.deletions > pr.additions:
        score -= 1
    if not pr.body:
        score -= 1
    return max(score, 0)

def generate_action_items(pr):
    items = []
    if "fix" in pr.title.lower() and "test" not in pr.title.lower():
        items.append("Add test cases for the fix.")
    if pr.additions > 1000:
        items.append("Break the PR into smaller parts.")
    return items

def final_decision(score):
    return "✅ Approve" if score >= 7 else "❌ Push Back"

def store_review(repo, pr_number, title, summary, score, actions, decision):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pr_reviews (repo, pr_number, title, summary, score, actions, decision, reviewed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (repo, pr_number, title, summary, score, json.dumps(actions), decision, datetime.now().isoformat()))
    conn.commit()
    conn.close()
