# Log Pattern Classifier

A high-performance Python-based log analysis tool that parses FlashBlade system logs, classifies incidents into predefined categories, detects anomalies, correlates related events, and generates actionable incident reports.

Designed as part of the **Pure Storage Empower Me Mentorship Program**, the project processes compressed log files efficiently using a single-pass pipeline and produces structured JSON reports along with human-readable incident summaries.

---

## Features

### Log Parsing
- Supports compressed `.zst` FlashBlade log files
- Extracts
  - Timestamp
  - Host
  - Source
  - Log Level
  - Message
- Robust regex-based parser
- Handles malformed log entries gracefully

### Incident Classification

Automatically classifies logs into the following categories:

| Category | Description |
|-----------|-------------|
| Process Initialization | Detects startup and initialization events |
| Process Crash | Detects unexpected process termination |
| Admin Network Issue | Network connectivity/configuration issues |
| Timeout | RPC, Request and operation timeout events |
| Port Error | Port failures and hardware interface errors |
| Link Flap | Link up/down oscillations |
| Switch Health Transition | Switch health state changes |
| Assert Failure | Assertion failures |
| SIGABRT Events | SIGABRT crashes |
| Stacktrace Events | Stack traces indicating software failures |

---

## Event Severity

The tool categorizes events into four severity levels.

### Critical
- Assert Failure
- SIGABRT Events
- Stacktrace Events

### Error
- Process Crash
- Port Error
- Admin Network Issue

### Warning
- Timeout
- Link Flap
- Switch Health Transition

### Info
- Process Initialization

---

# Project Architecture

```
               FlashBlade Logs (.zst)
                        │
                        ▼
                Decompression Module
                        │
                        ▼
                  Log Line Parser
                        │
                        ▼
            Single Pass Classification Engine
                        │
                        ▼
      ┌──────────────────────────────────┐
      │ Classifier Pipeline              │
      │                                  │
      │ Process Initialization           │
      │ Process Crash                    │
      │ Admin Network Issue              │
      │ Timeout                          │
      │ Port Error                       │
      │ Link Flap                        │
      │ Switch Health Transition         │
      │ Assert Failure                   │
      │ SIGABRT Events                   │
      │ Stacktrace Events                │
      └──────────────────────────────────┘
                        │
                        ▼
               Analysis Pipeline
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
Flap Detector   Anomaly Detector   Event Correlator
      │                 │                 │
      └─────────────────┼─────────────────┘
                        ▼
               Incident Narrator
                        │
                        ▼
                 Report Generator
                        │
                        ▼
          JSON Reports + Dashboard Output
```

---

# Project Structure

```
log-classifier/
│
├── app.py
├── requirements.txt
├── README.md
│
├── log_classifier/
│   ├── parser/
│   │   └── line_parser.py
│   │
│   ├── classifiers/
│   │   ├── process_initialization.py
│   │   ├── process_crash.py
│   │   ├── admin_network_issue.py
│   │   ├── timeout.py
│   │   ├── port_error.py
│   │   ├── link_flap.py
│   │   ├── switch_health_transition.py
│   │   ├── assert_failure.py
│   │   ├── sigabrt.py
│   │   └── stacktrace.py
│   │
│   ├── analysis/
│   │   ├── flap_detector.py
│   │   ├── anomaly_detector.py
│   │   ├── correlator.py
│   │   ├── narrator.py
│   │   └── reporter.py
│   │
│   └── main.py
│
├── templates/
│   ├── index.html
│   └── results.html
│
├── static/
│
├── Tests/
│
└── sample_logs/
```

---

# Technologies Used

### Programming Language

- Python 3.10+

### Libraries

- zstandard
- re
- json
- collections
- argparse
- Flask
- Bootstrap 5
- Chart.js

### Deployment

- Docker
- Amazon ECR
- AWS Elastic Beanstalk

---

# Installation

Clone the repository

```bash
git clone https://github.com/logithaa-g/log-classifier.git
```

Move into the project directory

```bash
cd log-classifier
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

Run using the command line

```bash
python -m log_classifier \
--input platform.log.zst \
--output report.json
```

Or launch the Flask dashboard

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

Upload one or multiple log files to generate reports.

---

# Generated Outputs

## report.json

Contains

- Event counts
- Severity distribution
- Classified events
- Summary statistics

---

## analysis_output.json

Contains

- Correlated incidents
- Detected anomalies
- Link flap analysis
- Timeline
- Root cause summary

---

## Dashboard

Displays

- Total events
- Severity distribution
- Incident categories
- Charts
- Timeline
- Event summary

---

# Sample Output

```
Total Events : 156

Critical : 6
Error    : 18
Warning  : 35
Info     : 97

Top Incident

Link Flap : 24
Timeout : 19
Port Error : 11
```

---

# Analysis Modules

## Flap Detector

Detects repeated link state transitions occurring within short time intervals.

---

## Anomaly Detector

Identifies unusual spikes in log frequency and abnormal system behavior.

---

## Event Correlator

Groups related log events occurring within the same incident window.

---

## Incident Narrator

Generates human-readable summaries explaining the sequence of system events.

Example

```
The switch experienced repeated link flaps followed by multiple timeout events.
This eventually triggered an assertion failure resulting in a SIGABRT crash.
```

---

## Report Generator

Produces structured JSON reports suitable for dashboards and future integrations.

---

# Performance

- Single-pass processing
- Low memory usage
- Scalable for large log files
- Efficient regex parsing
- Modular classifier architecture
- Easily extensible with new classifiers

---

# Future Improvements

- Machine Learning–based anomaly detection
- Elasticsearch integration
- Kibana dashboard support
- PDF incident reports
- Email alert generation
- Real-time log streaming
- Grafana visualization
- Docker Compose deployment
- REST API support

---

# Testing

Run all tests

```bash
pytest Tests/
```

---

# Screenshots

## Upload Dashboard

```
(Add Screenshot)
```

## Results Dashboard

```
(Add Screenshot)
```

## Incident Timeline

```
(Add Screenshot)
```

---

# Contributing

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Added new classifier"
```

4. Push

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# License

This project is licensed under the MIT License.

---

# Author

**Logithaa G**

Computer Science Engineering

GSSS Institute of Engineering and Technology for Women, Mysuru

GitHub:
https://github.com/logithaa-g

---

# Acknowledgements

- Pure Storage
- Empower Me Mentorship Program
- Python Open Source Community
- Flask Community