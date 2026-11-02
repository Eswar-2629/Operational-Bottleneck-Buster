import json
import logging
from pathlib import Path


def write_reports(records, errors, time_savings, output_dir, as_of):
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    counts = {"Ready": 0, "Needs follow-up": 0, "Blocked": 0}
    priority_counts = {"Urgent": 0, "High": 0, "Standard": 0}
    for record in records:
        counts[record.status] += 1
        priority_counts[record.priority] += 1

    payload = {
        "as_of": as_of.isoformat(),
        "processed_records": len(records),
        "invalid_records": len(errors),
        "status_counts": counts,
        "priority_counts": priority_counts,
        "records": [record.to_dict() for record in records],
        "errors": errors,
        "time_savings": time_savings,
    }
    json_path = destination / "onboarding_report.json"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    text_path = destination / "onboarding_dashboard.txt"
    lines = [
        "OPERATIONAL BOTTLENECK BUSTER - ONBOARDING DASHBOARD",
        "=" * 58,
        f"As of: {as_of.isoformat()}",
        f"Processed records: {len(records)}",
        f"Invalid records: {len(errors)}",
        "",
        "STATUS SUMMARY",
        "-" * 58,
        f"Ready:             {counts['Ready']:>3}",
        f"Needs follow-up:   {counts['Needs follow-up']:>3}",
        f"Blocked:           {counts['Blocked']:>3}",
        "",
        "TIME SAVINGS FOR THIS BATCH",
        "-" * 58,
        f"Manual time:       {time_savings['manual_hours']:>6.2f} hours",
        f"Automated time:    {time_savings['automated_hours']:>6.2f} hours",
        f"Time saved:        {time_savings['hours_saved']:>6.2f} hours",
        f"Work reduction:    {time_savings['percent_reduction']:>5.1f}%",
        "",
        "ACTION QUEUE",
        "-" * 58,
    ]
    for record in sorted(records, key=lambda item: (item.priority != "Urgent", item.priority != "High", item.start_date)):
        if record.status != "Ready":
            missing = ", ".join(record.missing_items) if record.missing_items else "None"
            lines.append(
                f"[{record.priority}] {record.full_name} | {record.status} | Missing: {missing}"
            )
    lines.append("")

    if errors:
        lines.extend(["VALIDATION ERRORS", "-" * 58])
        lines.extend(f"Row {error['row']}: {error['error']}" for error in errors)

    text_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logging.info("Wrote %s and %s", json_path, text_path)
    return json_path, text_path
