

def calculate_time_savings(record_count, exception_count, manual_minutes=18, auto_ready_minutes=1.5, auto_exception_minutes=7):
    if record_count < 0 or exception_count < 0 or exception_count > record_count:
        raise ValueError("Record count and exception count are invalid")

    manual_total = record_count * manual_minutes
    ready_count = record_count - exception_count
    automated_total = (ready_count * auto_ready_minutes) + (exception_count * auto_exception_minutes)
    minutes_saved = manual_total - automated_total
    percent_reduction = (minutes_saved / manual_total * 100) if manual_total else 0

    return {
        "manual_minutes": manual_total,
        "automated_minutes": round(automated_total, 1),
        "minutes_saved": round(minutes_saved, 1),
        "percent_reduction": round(percent_reduction, 1),
        "manual_hours": round(manual_total / 60, 2),
        "automated_hours": round(automated_total / 60, 2),
        "hours_saved": round(minutes_saved / 60, 2),
    }
