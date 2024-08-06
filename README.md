# Check-In Automation

Automate the check-in process for a web application using Selenium.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)

## Prerequisites

- Python 3.11

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NAMUS09/CheckInAutomation.git
   cd CheckInAutomation
   ```

2. Install dependencies:

   ```bash
   pip install selenium pillow pyinstaller requests cryptography pyinstaller-versionfile
   ```

### Usage

Run the application:

```bash
python main_app.py
```

Build the application exe:

```bash
python release/build.py
```

Build the uninstall exe:

```bash
pyinstaller --noconsole --onefile --clean --icon=assets\uninstall.ico --add-data "assets;assets" --name=UnInstaller uninstall\main.py
```
