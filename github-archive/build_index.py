#!/usr/bin/env python3
"""Render the exported GitHub JSON into browsable Markdown indexes."""
import json
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).parent


def load(name):
    """gh --paginate --slurp yields a list of pages; flatten to a flat list."""
    data = json.loads((HERE / name).read_text())
    out = []
    for page in data:
        out.extend(page) if isinstance(page, list) else out.append(page)
    return out


issues = load("issues.json")
pulls = load("pulls.json")
comments = load("issue_comments.json")
review_comments = load("review_comments.json")

reviews = defaultdict(list)
for line in (HERE / "reviews.ndjson").read_text().splitlines():
    rec = json.loads(line)
    reviews[rec["pr"]] = rec["reviews"]

by_issue = defaultdict(list)
for c in comments:
    by_issue[int(c["issue_url"].rsplit("/", 1)[1])].append(c)
for c in review_comments:
    by_issue[int(c["pull_request_url"].rsplit("/", 1)[1])].append(c)


def user(obj):
    u = obj.get("user") or {}
    return u.get("login", "ghost")


def render(items, title, is_pr):
    lines = [f"# {title}", ""]
    lines.append(f"Exported from `autowarefoundation/autoware-deb-packages`. {len(items)} entries.")
    lines.append("")
    lines.append("| # | State | Title | Author | Created |")
    lines.append("|---|---|---|---|---|")
    for it in sorted(items, key=lambda x: -x["number"]):
        state = it["state"]
        if is_pr and it.get("merged_at"):
            state = "merged"
        t = it["title"].replace("|", "\\|")
        lines.append(
            f"| [{it['number']}](#{'pr' if is_pr else 'issue'}-{it['number']}) "
            f"| {state} | {t} | {user(it)} | {it['created_at'][:10]} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    for it in sorted(items, key=lambda x: -x["number"]):
        n = it["number"]
        anchor = f"{'pr' if is_pr else 'issue'}-{n}"
        lines.append(f"## <a id=\"{anchor}\"></a>#{n} — {it['title']}")
        lines.append("")
        meta = [f"**State:** {it['state']}", f"**Author:** {user(it)}",
                f"**Created:** {it['created_at']}"]
        if is_pr:
            meta.append(f"**Merged:** {it.get('merged_at') or 'no'}")
            if it.get("head"):
                meta.append(f"**Branch:** `{it['head'].get('ref')}` → `{it['base'].get('ref')}`")
        meta.append(f"**URL:** {it['html_url']}")
        lines.append("  \n".join(meta))
        lines.append("")
        body = (it.get("body") or "").strip()
        lines.append(body if body else "_(no description)_")
        lines.append("")
        for r in reviews.get(n, []):
            rb = (r.get("body") or "").strip()
            lines.append(f"> **Review by {user(r)}** ({r.get('state')})"
                         + (f": {rb}" if rb else ""))
            lines.append("")
        for c in sorted(by_issue.get(n, []), key=lambda x: x["created_at"]):
            cb = (c.get("body") or "").strip()
            lines.append(f"> **{user(c)}** on {c['created_at'][:10]}:")
            for ln in cb.splitlines():
                lines.append(f"> {ln}")
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


pr_numbers = {p["number"] for p in pulls}
real_issues = [i for i in issues if i["number"] not in pr_numbers and "pull_request" not in i]

(HERE / "ISSUES.md").write_text(render(real_issues, "Issues", False))
(HERE / "PULLS.md").write_text(render(pulls, "Pull Requests", True))

print(f"issues: {len(real_issues)}  pulls: {len(pulls)}  "
      f"comments: {len(comments)}  review_comments: {len(review_comments)}  "
      f"reviews: {sum(len(v) for v in reviews.values())}")
