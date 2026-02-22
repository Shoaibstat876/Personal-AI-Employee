from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


TZ_PK = timezone(timedelta(hours=5))


def now_pk() -> datetime:
    return datetime.now(tz=TZ_PK)


def iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def safe_read_text(p: Path) -> Optional[str]:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return None


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


@dataclass
class RevenueInfo:
    this_week: float
    month_to_date: float
    currency: str
    source_note: str


def read_revenue(vault: Path, period_start: datetime, period_end: datetime) -> RevenueInfo:
    """
    Optional revenue sources (best-effort):
      1) AI_Employee_Vault/Accounting/revenue.json  (recommended)
         Example:
         { "currency":"PKR", "transactions":[{"date":"2026-02-20","amount":1200.0}, ...] }
      2) AI_Employee_Vault/Accounting/revenue.txt (single number)
    If nothing exists, returns zeros with a note.
    """
    acct = vault / "Accounting"
    rev_json = acct / "revenue.json"
    rev_txt = acct / "revenue.txt"

    # Default
    currency = "PKR"
    tx: List[Dict[str, Any]] = []

    if rev_json.exists():
        raw = safe_read_text(rev_json)
        if raw:
            try:
                data = json.loads(raw)
                currency = str(data.get("currency") or currency)
                tx = list(data.get("transactions") or [])
                # Expect tx items: {"date":"YYYY-MM-DD", "amount": number}
                this_week = 0.0
                month_to_date = 0.0
                for item in tx:
                    d = item.get("date")
                    amt = float(item.get("amount", 0.0))
                    try:
                        dt = datetime.fromisoformat(d).replace(tzinfo=TZ_PK)
                    except Exception:
                        # try YYYY-MM-DD
                        try:
                            dt = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=TZ_PK)
                        except Exception:
                            continue

                    if period_start <= dt <= period_end:
                        this_week += amt

                    if dt.year == period_end.year and dt.month == period_end.month and dt <= period_end:
                        month_to_date += amt

                return RevenueInfo(
                    this_week=round(this_week, 2),
                    month_to_date=round(month_to_date, 2),
                    currency=currency,
                    source_note="Revenue from Accounting/revenue.json (best-effort).",
                )
            except Exception:
                pass

    if rev_txt.exists():
        raw = safe_read_text(rev_txt)
        if raw:
            try:
                val = float(raw.strip())
                return RevenueInfo(
                    this_week=round(val, 2),
                    month_to_date=round(val, 2),
                    currency=currency,
                    source_note="Revenue from Accounting/revenue.txt (single-number mock).",
                )
            except Exception:
                pass

    return RevenueInfo(
        this_week=0.0,
        month_to_date=0.0,
        currency=currency,
        source_note="No revenue source found (Accounting/revenue.json or revenue.txt). Using 0.00.",
    )


def list_done_items(vault: Path, period_start: datetime) -> Tuple[int, List[str]]:
    """
    Counts files under AI_Employee_Vault/Done that were modified within the period.
    If /Done doesn't exist, returns 0 and a note.
    """
    done_dir = vault / "Done"
    if not done_dir.exists():
        return 0, ["Done folder not found (AI_Employee_Vault/Done)."]

    items: List[Path] = [p for p in done_dir.rglob("*") if p.is_file()]
    recent: List[Path] = []
    for p in items:
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=TZ_PK)
            if mtime >= period_start:
                recent.append(p)
        except Exception:
            continue

    # Return just a few names for the briefing
    recent_sorted = sorted(recent, key=lambda x: x.stat().st_mtime, reverse=True)
    sample_names = [p.name for p in recent_sorted[:10]]
    return len(recent), sample_names


def append_audit_jsonl(vault: Path, event: str, risk_level: str, details: Dict[str, Any]) -> Path:
    logs = vault / "Logs"
    ensure_dir(logs)
    log_path = logs / f"action_log_{now_pk().strftime('%Y-%m-%d')}.jsonl"

    entry = {
        "timestamp": iso(now_pk()),
        "event": event,
        "actor": "executor",
        "task_id": "CEO_BRIEFING_GENERATION",
        "run_id": None,
        "risk_level": risk_level,
        "details": details,
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return log_path


def write_briefing(vault: Path, out_path: Path) -> None:
    end = now_pk()
    start = end - timedelta(days=7)

    revenue = read_revenue(vault, start, end)
    done_count, done_samples_or_notes = list_done_items(vault, start)

    ensure_dir(out_path.parent)

    period_str = f"{start.date().isoformat()} to {end.date().isoformat()}"

    # Build markdown
    md = []
    md.append("---")
    md.append("type: ceo_briefing")
    md.append(f"generated_at: {iso(end)}")
    md.append(f"period: {period_str}")
    md.append("source: local_vault")
    md.append("---")
    md.append("")
    md.append("# Monday Morning CEO Briefing")
    md.append("")
    md.append("## Executive Summary")
    md.append(f"- Generated automatically from local vault state ({period_str}).")
    md.append(f"- Completed items observed: **{done_count}** (best-effort).")
    md.append("- Pending approvals and execution actions are not auto-run in Gold.")
    md.append("")
    md.append("## Revenue / Money (if available)")
    md.append(f"- This week: **{revenue.currency} {revenue.this_week:.2f}**")
    md.append(f"- Month-to-date: **{revenue.currency} {revenue.month_to_date:.2f}**")
    md.append(f"- Note: {revenue.source_note}")
    md.append("")
    md.append("## Completed Work (sample)")
    if done_count == 0:
        md.append("- (No Done items detected in last 7 days, or Done folder missing.)")
    else:
        for name in done_samples_or_notes[:10]:
            md.append(f"- [x] {name}")
    md.append("")
    md.append("## Bottlenecks / Risks")
    md.append("| Area | Risk | Why | Suggested Fix |")
    md.append("|------|------|-----|---------------|")
    md.append("| Operations | medium | Review pending approvals regularly | Daily 2-min review in Obsidian |")
    md.append("| Logging | low | Keep action_log JSONL append-only | Rotate weekly into archive if large |")
    md.append("")
    md.append("## Pending Approvals")
    pend = vault / "Pending_Approval"
    approved = vault / "Approved"
    rejected = vault / "Rejected"
    md.append(f"- Pending folder exists: **{pend.exists()}**")
    md.append(f"- Approved folder exists: **{approved.exists()}**")
    md.append(f"- Rejected folder exists: **{rejected.exists()}**")
    md.append("")
    md.append("## Next 7 Days Focus")
    md.append("- 1) Keep Gold deterministic + auditable (no hidden actions).")
    md.append("- 2) Expand CEO briefing with real data sources later (Platinum/Enhancement).")
    md.append("- 3) Improve demo clarity with clean proof packs and video script.")
    md.append("")
    md.append("---")
    md.append("*Generated by Personal AI Employee (Gold).*")
    md.append("")

    out_path.write_text("\n".join(md), encoding="utf-8")

    # Audit log entry
    audit_path = append_audit_jsonl(
        vault=vault,
        event="CEO_BRIEFING_GENERATED",
        risk_level="low",
        details={
            "briefing_file": str(out_path).replace("\\", "/"),
            "period": period_str,
            "done_count": done_count,
            "revenue": {
                "currency": revenue.currency,
                "this_week": revenue.this_week,
                "month_to_date": revenue.month_to_date,
                "source_note": revenue.source_note,
            },
        },
    )

    # Also record where audit was written (useful for proof)
    _ = audit_path  # intentional


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate Monday CEO Briefing (Gold-safe, local-only).")
    ap.add_argument("--vault", default="AI_Employee_Vault", help="Path to vault root.")
    ap.add_argument(
        "--out",
        default="AI_Employee_Vault/Briefings",
        help="Output directory for briefings (folder).",
    )
    args = ap.parse_args()

    repo_root = Path.cwd()
    vault = (repo_root / args.vault).resolve()

    out_dir = (repo_root / args.out).resolve()
    fname = f"{now_pk().strftime('%Y-%m-%d')}_Monday_CEO_Briefing.md"
    out_path = out_dir / fname

    if not vault.exists():
        raise SystemExit(f"Vault not found: {vault}")

    write_briefing(vault=vault, out_path=out_path)
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())