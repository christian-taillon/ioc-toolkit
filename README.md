Python Script for Repository Scanning

## Description

This Python script authenticates to obtain a JWT token and uses it to create scans for repositories listed in a CSV file. It's designed to work with the Privya API.

## Prerequisites

Before running the script, ensure you have Python installed on your system. Python 3.6 or later is recommended. You can download Python from [python.org](https://www.python.org/downloads/).

## Installation

### Step 1: Clone the Repository

Clone this repository to your local machine using:

```bash
git clone [URL to the repository]
```

### Step 2: Install Required Packages

Navigate to the cloned directory and install the required Python packages using:

```bash
pip install -r requirements.txt
```

### `requirements.txt` Content

```
requests==2.25.1
```

## Setup

### Environment Variables

Set the following environment variables:

- `privya_client_id`: Your Privya client ID.
- `privya_client_secret`: Your Privya client secret.

#### Linux/macOS

Open your terminal and run:

```bash
export privya_client_id='your_client_id'
export privya_client_secret='your_client_secret'
```

#### Windows

Open Command Prompt and run:

```cmd
set privya_client_id=your_client_id
set privya_client_secret=your_client_secret
```

### CSV File

Ensure you have a CSV file named `repos.csv` in the same directory as the script. The CSV file should have a column named `repo` containing the repository clone paths.

## Usage

Run the script using the following command:

```bash
python3 script_name.py
```

Replace `script_name.py` with the actual name of the Python script.

### Operating System Specific Instructions

#### Linux/macOS

1. Open your terminal.
2. Navigate to the script's directory.
3. Run the script using the command above.

#### Windows

1. Open Command Prompt or PowerShell.
2. Navigate to the script's directory.
3. Run the script using the command above.
