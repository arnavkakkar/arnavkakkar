#!/usr/bin/env python3
import datetime
import json
import os
import re
import sys
import urllib.request

USERNAME = os.environ.get("GH_PROFILE_USER", "arnavkakkar")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


def fetch_days():
    req = urllib.request.Request(URL, headers={"User-Agent": "profile-readme-bot/1.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching contributions: {e}", file=sys.stderr)
        sys.exit(1)

    tds = re.findall(r'<td[^>]*data-date="([0-9]{4}-[0-9]{2}-[0-9]{2})"[^>]*id="([^"]+)"', html)
    if not tds:
        tds = [(d, i) for i, d in re.findall(r'id="([^"]+)"[^>]*data-date="([0-9]{4}-[0-9]{2}-[0-9]{2})"', html)]

    tooltips = {}
    for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', html, re.DOTALL):
        tooltips[m.group(1)] = m.group(2).strip()

    days = []
    for date, td_id in tds:
        txt = tooltips.get(td_id, "")
        if "no contributions" in txt.lower():
            cnt = 0
        else:
            match = re.search(r"(\d+)\s+contribution", txt, re.I)
            cnt = int(match.group(1)) if match else 0
        days.append({"date": date, "count": cnt})

    days.sort(key=lambda d: d["date"])
    return days


def compute_current_streak(days):
    idx = len(days) - 1
    if days and days[idx]["count"] == 0:
        idx -= 1
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0 or not days:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end


def build_data(days):
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"] if days else "", "end": days[-1]["date"] if days else ""},
        "total_contributions": total,
        "active_days": active_days,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "days": days,
    }


if __name__ == "__main__":
    days = fetch_days()
    data = build_data(days)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {OUT_PATH}: {data['total_contributions']} contributions found for {USERNAME}.")
