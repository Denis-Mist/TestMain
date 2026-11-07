"""Summarize a JMeter CSV results file."""

import csv
import sys
from collections import defaultdict
from pathlib import Path


def stats(rows):
    elapsed = [int(float(row["elapsed"])) for row in rows]
    stamps = [int(row["timeStamp"]) for row in rows]
    errors = sum(1 for row in rows if str(row["success"]).lower() != "true")
    span_ms = max(stamps) - min(stamps)
    throughput = len(rows) / (span_ms / 1000) if span_ms else float(len(rows))
    return {
        "samples": len(rows),
        "avg": round(sum(elapsed) / len(elapsed)),
        "min": min(elapsed),
        "max": max(elapsed),
        "error": round(100 * errors / len(rows), 2),
        "throughput": round(throughput, 2),
    }


def main():
    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    with source.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    groups = defaultdict(list)
    for row in rows:
        groups[row["label"]].append(row)
    lines = [
        "| Label | Samples | Avg ms | Min | Max | Error % | Throughput /s |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    ordered = list(groups.items())
    if rows:
        ordered.append(("TOTAL", rows))
    for label, items in ordered:
        item = stats(items)
        lines.append(
            f"| {label} | {item['samples']} | {item['avg']} | {item['min']} | {item['max']} | {item['error']} | {item['throughput']} |"
        )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
