# Operational Bottleneck Buster

A free, local Python CLI that automates BrightPath Logistics' onboarding document check. This portfolio project demonstrates how a repeatable administrative workflow can be validated, prioritized, logged, and reported without paid services.

## Problem
BrightPath Logistics, a 50-person operations and logistics company, hires about 20 people per month. The People Operations coordinator currently checks offer letters, identity documents, background checks, and bank details across email threads, then updates a spreadsheet and flags urgent starters manually. The process takes about 18 minutes per employee, can be missed when information arrives across separate messages, and creates avoidable delays for hiring managers and new starters. Across 20 monthly hires, manual work totals approximately 6 hours before data-quality errors and rescheduling are counted.

## Approach
The program treats the employee CSV as a controlled input and applies the same onboarding rules to every row. It validates required fields and dates, labels each record as Ready, Needs follow-up, or Blocked, prioritizes work by the number of days until start, logs invalid rows, and produces text and JSON reports. It also calculates manual and automated effort from explicit assumptions, making the impact defensible and easy to discuss in an interview.

## Before/After Workflow

| Before: manual step | Time per record | Automated equivalent | Time per record |
|---|---:|---|---:|
| Search email for offer, identity, background, and banking documents | 3 min | CSV ingestion | included in batch execution |
| Compare documents with a checklist | 5 min | Rule-based field validation and status assignment | included in batch execution |
| Check start date and classify urgency | 2 min | Start-date priority calculation | included in batch execution |
| Update spreadsheet/status | 4 min | Generate text and JSON reports | included in batch execution |
| Email affected hiring manager or HR partner | 4 min | Produce a sorted action queue | 1.5 min Ready / 7 min exception review |
| **Total** | **18 min** | **Estimated automated handling** | **1.5 min Ready / 7 min exception** |

### Current workflow
1. Download information from email or hiring systems.
2. Find four document statuses for each candidate.
3. Compare statuses against BrightPath's checklist.
4. Search for the employee's start date and urgency.
5. Update the tracker.
6. Email managers about missing or blocked items.

### Streamlined workflow
1. Export the approved onboarding batch to CSV.
2. Run the CLI with an optional review date.
3. Review the generated action queue and dashboard.
4. Follow up only on candidates marked Needs follow-up or Blocked.
5. Use the JSON report for downstream systems or future dashboard integration.

## Solution
**Project structure**

```text
Operational-Bottleneck-Buster/
├── README.md
├── data/
│   └── employees.csv
├── src/
│   ├── main.py
│   ├── models.py
│   ├── processor.py
│   ├── reporting.py
│   └── time_savings.py
├── tests/
│   ├── test_processor.py
│   └── test_time_savings.py
└── output/
    ├── onboarding_dashboard.txt
    └── onboarding_report.json
```

**Design decisions**
- `models.py` uses immutable dataclasses for clear data contracts.
- `processor.py` owns input validation and business classification.
- `reporting.py` separates report generation from command-line behavior.
- `time_savings.py` accepts assumptions as parameters, so the formula is testable and can change without rewiring the CLI.
- The program uses only Python's standard library so setup remains free and local.

The implementation is complete in the repository files under [src](src), [data](data), and [tests](tests). Each module has one responsibility, which makes it easier to explain and extend.

## Results
The included 20-row sample plus one invalid row produced:

- **20 valid records processed**
- **1 invalid record logged**
- **10 Ready**
- **5 Needs follow-up**
- **5 Blocked**
- **4.58 hours saved for the batch**
- **76.4% reduction in modeled manual effort**

### Impact assumptions
These are planning assumptions, not observed production measurements:

1. Each valid onboarding record manually takes 18 minutes.
2. A Ready record takes 1.5 minutes of automated-review time.
3. An exception record takes 7 minutes to review the dashboard and send follow-up.
4. The 20 valid mock records represent one monthly onboarding batch.
5. There are 4.33 weeks in a month for weekly extrapolation.
6. Invalid records are excluded from modeled savings because they require separate correction.

For this batch:

- Manual: `20 * 18 = 360 minutes = 6.00 hours`
- Automated: `(10 Ready * 1.5) + (10 exceptions * 7) = 85 minutes = 1.42 hours`
- Saved: `360 - 85 = 275 minutes = 4.58 hours`
- Reduction: `275 / 360 = 76.4%`

Monthly impact is **4.58 hours saved**, based on one 20-person batch. Using the same sample composition, estimated weekly impact is **1.06 hours saved** (`4.58 / 4.33`). The percentage remains **76.4%** because the formula scales with the modeled mix of Ready and exception records.

## Tech Used
Python 3, CSV/JSON, argparse, dataclasses, unittest, and Python logging. No paid APIs, database, credentials, or packages are required.

## Setup and Run
From the repository root:

```bash
python3 src/main.py --input data/employees.csv --output output --as-of 2026-11-02
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

Optional commands:

```bash
python3 src/main.py --help
python3 src/main.py --input my_employees.csv --output reports
```

Example output (key lines):

```text
Processed records: 20
Invalid records: 1
Ready:              10
Needs follow-up:     5
Blocked:             5
Manual time:         6.00 hours
Automated time:      1.42 hours
Time saved:          4.58 hours
Work reduction:     76.4%
```

The text dashboard is written to `output/onboarding_dashboard.txt`, the structured report to `output/onboarding_report.json`, and operational logs to `onboarding.log`.

## Future Improvements
- Add an email or spreadsheet connector after validating credentials and data ownership.
- Store run history in SQLite for trend and aging analysis.
- Add automated expiration and overdue-item calculations.
- Build a small web dashboard from the generated JSON report.
- Replace boolean CSV values with a controlled integration schema and audit trail.

## Interview Talking Points
- The project starts with a measurable operational problem and removes the repeated decision-making from a spreadsheet-heavy onboarding process.
- CSV validation is deliberate: bad data is reported by row instead of silently producing incorrect onboarding actions.
- The time-savings model is separate from classification logic and tested independently.
- The `Ready`/`Needs follow-up`/`Blocked` states create a useful exception queue rather than making employees trust a fully automated decision.
- The implementation is intentionally local and dependency-free, showing that process improvement can be demonstrated before introducing infrastructure or paid tools.

## Likely Follow-Up Questions

**How did you choose the time assumptions?**
They are explicit portfolio assumptions for a realistic manual workflow. A manager would replace them with observed timestamps from current work before treating them as a production forecast.

**How does this differ from a spreadsheet formula?**
The program validates input, handles bad rows, applies consistent priority and status rules, logs each run, and produces both an operational action queue and structured JSON. Those behaviors make it reusable and easier to integrate than a manually maintained formula set.

**How would this work with real data?**
First, control the source system, document access rules, and minimum fields. Then add a connector for the approved HRIS or secure file share, keep the processor and report interfaces unchanged, and add authorization and audit logging before production deployment.
