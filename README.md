# Check-In Automation

Automate the check-in process for a web application using Selenium.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.11
- Selenium library
- Pillow library
- Pyinstaller library
- Requests library
- Cryptography library

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/check-in-automation.git
   cd check-in-automation
   ```

2. Install dependencies:

   ```bash
   pip install selenium pillow pyinstaller requests cryptography
   ```

### Usage

Run the application:

```bash
python main_app.py
```

Build the application exe:

```bash
pyinstaller --noconsole --onefile --clean --icon=assets\clock.ico --add-data assets;assets --name=CheckInAutomation main.py
```

Build the uninstall exe:

```bash
pyinstaller --noconsole --onefile --clean --icon=assets\uninstall.ico --add-data assets;assets --name=UnInstaller uninstall\main.py
```
