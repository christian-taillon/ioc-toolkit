# IoC Parser

IoCParserPro is a Python script designed to extract Indicators of Compromise (IoCs) from text input. It interacts with the api.iocparser.com to parse various types of IoCs and includes additional functionality for guessing IPs and defanging IoCs.

### Installation

First, clone the repository or download the script to your local machine.

```bash
git clone https://your-repository-url.git
cd ioc-parser-pro
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Usage

#### Common Steps for All Operating Systems

1. Run the script using Python:

   ```bash
   python3 ioc_parser_pro.py
   ```

2. Follow the on-screen prompts to input text directly or use the `--input` flag to specify a file path for text input.

3. Optionally, use the `--output` flag to specify a file path for saving the output and `--format` to set the output format (`yaml`, `txt`, `csv`, `json`).

4. To opt out of defanging IoCs, use the `--nodefang` flag.

#### Linux & macOS

- Open your terminal.
- Navigate to the directory where the script is located.
- Follow the common steps outlined above.

#### Windows

- Open Command Prompt or PowerShell.
- Navigate to the directory where the script is located.
- Follow the common steps outlined above.
