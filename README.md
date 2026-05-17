# Log Pattern Classifier

## Overview

Log Pattern Classifier is a Python-based log analysis system designed to process network switch logs, classify operational events, detect abnormal behavior, correlate related failures, and generate structured reports.

The project simulates a lightweight monitoring and troubleshooting pipeline similar to systems used in production networking environments. It supports parsing compressed and uncompressed logs, event classification, anomaly detection, event correlation, and incident reporting.

The system is modular and extensible, allowing additional classifiers and analysis modules to be integrated easily.

---

# Objectives

The project was built with the following objectives:

- Parse raw switch logs into structured events
- Detect important operational failures
- Identify unstable links and recurring issues
- Correlate multiple events to identify root causes
- Generate machine-readable and human-readable reports
- Support multi-file log analysis

---

# Features

## Log Parsing
- Supports `.log` and `.zst` files
- Parses timestamps, hostnames, and message content
- Multi-file aggregation support

## Event Classification
Supported classifiers include:

- SwitchD Crash
- VIP Failure
- Port Errors
- Link Flaps
- LACP Failures
- Mastership Events
- Switch Initialization
- Switch Health Events
- Admin Network Failures

## Analysis Engine
The analysis layer performs:

- Flap Detection
- Counter Anomaly Detection
- Event Correlation
- Severity Assignment
- Incident Narrative Generation

## Reporting
- JSON report generation
- Colored terminal summaries
- Severity filtering
- Category filtering

---

# System Architecture

```text
                    +-------------------+
                    |   Raw Log Files   |
                    | (.log / .zst)     |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |   Decompressor    |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |    Line Parser    |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |    Classifiers    |
                    |-------------------|
                    | SwitchD Crash     |
                    | VIP Failure       |
                    | Port Errors       |
                    | LACP              |
                    | Mastership        |
                    | Link Flaps        |
                    | Switch Health     |
                    | Admin Network     |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Normalized Events |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Analysis Engine   |
                    |-------------------|
                    | Flap Detection    |
                    | Anomaly Detection |
                    | Correlation       |
                    | Severity Mapping  |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Incident Reporter |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | report.json       |
                    +-------------------+
```

---

# Project Structure

```text
log_pattern_classifier/
│
├── analysis/
│   ├── anomaly_detector.py
│   ├── correlator.py
│   ├── flap_detector.py
│   ├── main_analysis.py
│   ├── narrator.py
│   ├── normalizer.py
│   ├── reporter.py
│   └── severity.py
│
├── classifiers/
│   ├── admin_net.py
│   ├── base.py
│   ├── lacp.py
│   ├── link_flap.py
│   ├── mastership.py
│   ├── port_errors.py
│   ├── switch_health.py
│   ├── switch_init.py
│   ├── switchd_crash.py
│   └── vip_failure.py
│
├── parser/
│   ├── decompressor.py
│   └── line_parser.py
│
├── tests/
│   ├── test_classifiers.py
│   └── test_parser.py
│
├── __main__.py
├── compress.py
├── README.md
└── .gitignore
```

---

# Processing Pipeline

The system follows a multi-stage pipeline for processing logs.

## Phase 1: Parsing

Raw log files are read line-by-line and converted into structured event dictionaries.

Example log:

```text
2026-03-05 18:16:10 Port Ethernet1 link DOWN
```

Structured event:

```json
{
    "timestamp": "2026-03-05 18:16:10",
    "message": "Port Ethernet1 link DOWN"
}
```

---

## Phase 2: Classification

Each parsed event is passed through multiple classifiers.

The classifiers determine:
- Event category
- Severity
- Port information
- Failure type

Example classified event:

```json
{
    "category": "Port Error",
    "severity": "error"
}
```

---

## Phase 3: Analysis

The analysis engine processes classified events and detects patterns.

### Flap Detection
Detects rapid DOWN → UP transitions on interfaces.

### Anomaly Detection
Detects sudden spikes in counter values.

### Correlation Engine
Combines related events occurring within a time window.

Example:
- Port Error
- Link DOWN
- Restart Event

These are combined into a single correlated incident.

### Narrative Generation
Converts incidents into human-readable summaries.

---

## Phase 4: Reporting

The reporting layer generates:
- JSON reports
- Console summaries
- Severity-filtered outputs
- Category-filtered outputs

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd log_pattern_classifier
```

## Install Dependencies

```bash
pip install colorama
```

---

# Usage

## Single File Processing

```bash
python __main__.py --input sample.log --output report.json
```

## Multiple File Processing

```bash
python __main__.py --input "*.log" --output report.json
```

## Severity Filtering

```bash
python __main__.py --input "*.log" --output report.json --severity critical
```

## Category Filtering

```bash
python __main__.py --input "*.log" --output report.json --filter-category "Port Error"
```

## Run Analysis Engine

```bash
python analysis/main_analysis.py
```

---

# Example Incident Summary

```text
1. Multiple ports went down simultaneously.
   This indicates a possible switch reset.

2. A port error was followed by link failure
   and system restart.

3. High packet loss caused link instability.
```

---

# Output Format

The generated report contains:

- Summary statistics
- Incident list
- Flap details
- Anomaly details
- Narrative summary

Example:

```json
{
    "summary": {
        "total_events": 35,
        "overall_severity": "CRITICAL"
    }
}
```

---

# Design Decisions

Several design decisions were made during development:

- Modular classifier architecture for extensibility
- Separate analysis layer for scalability
- JSON-based reporting for interoperability
- Rule-based correlation for explainability
- CLI workflow for easier automation

---

# Future Improvements

Possible future enhancements include:

- Real-time streaming analysis
- Machine learning based anomaly detection
- Interactive HTML timeline visualization
- Dashboard interface
- REST API support
- Database-backed event storage

---

# Technologies Used

- Python
- argparse
- glob
- JSON
- Regex
- colorama

---

# Author

Logithaa G

Computer Science Engineering  
GSSSIETW