import argparse
import logging
import sys
from datetime import date

from processor import InputError, classify, load_candidates
from reporting import write_reports
from time_savings import calculate_time_savings


def configure_logging(log_path):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(log_path, encoding="utf-8")],
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Automate BrightPath Logistics onboarding document checks")
    parser.add_argument("--input", default="data/employees.csv", help="Input CSV path")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Review date in YYYY-MM-DD format")
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging("onboarding.log")

    try:
        as_of = date.fromisoformat(args.as_of)
    except ValueError:
        logging.error("--as-of must use YYYY-MM-DD format: %s", args.as_of)
        return 2

    try:
        candidates, errors = load_candidates(args.input)
    except InputError as exc:
        logging.error("Input validation failed: %s", exc)
        return 2

    processed = [classify(candidate, as_of) for candidate in candidates]
    exception_count = sum(record.status != "Ready" for record in processed)
    savings = calculate_time_savings(len(processed), exception_count)

    json_path, text_path = write_reports(processed, errors, savings, args.output, as_of)

    logging.info("Processed %d valid records and %d invalid records", len(processed), len(errors))
    logging.info("Time saved for this batch: %.2f hours (%.1f%%)", savings["hours_saved"], savings["percent_reduction"])
    print(text_path.read_text(encoding="utf-8"), end="")
    logging.info("JSON report: %s", json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
