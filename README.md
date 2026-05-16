# Week 3 – Python Automation Projects

This repository contains my Week 3 internship tasks completed during my Python Development Internship at Syntecxhub.

## Projects Included

### 1. CSV to Excel Converter
A Python automation script that converts CSV files into Excel format with data cleaning and validation.

#### Features
- Reads CSV files
- Cleans column names
- Handles missing values
- Detects date columns automatically
- Exports data to Excel format
- Error handling with logging

#### Technologies Used
- Python
- Pandas
- OpenPyXL
- Argparse
- Logging

#### Usage

```bash
python csv_to_excel.py -i input.csv -o output.xlsx
```

---

### 2. Automated Email Sender Bot
A Python script that sends personalized emails automatically to multiple recipients.

#### Features
- Personalized email messages
- Multiple recipients support
- Retry mechanism
- Activity logging
- Secure SMTP connection

#### Technologies Used
- Python
- smtplib
- MIME
- Logging

#### Usage

```bash
python Emailbot.py
```

---

### 3. News Headline Scraper
A terminal-based web scraper that collects latest headlines from multiple news sources using RSS feeds.

#### Features
- Fetches headlines from multiple sources
- Keyword filtering
- Save output as JSON or CSV
- Colored terminal output
- Command-line arguments support

#### Supported Sources
- BBC
- Reuters
- NDTV
- The Hindu
- Hindustan Times
- Times of India

#### Usage

Fetch headlines:

```bash
python headline_scraper.py
```

Search by keyword:

```bash
python headline_scraper.py --keyword tech
```

Save as JSON:

```bash
python headline_scraper.py --format json
```

Save as CSV:

```bash
python headline_scraper.py --format csv
```

---

## Repository Structure

```bash
week-3/
│
├── csv_to_excel.py
├── Emailbot.py
├── headline_scraper.py
├── anime_data.csv
├── anime_output.xlsx
└── README.md
```

---

## Learning Outcomes

In this week, I learned:

- File handling and data processing
- Email automation
- Web scraping using RSS feeds
- Command-line interface development
- Logging and exception handling
- Python project structuring

---

## Author

Sarthak Rahane  
Python Developer Intern – Syntecxhub
