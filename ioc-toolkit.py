#!/usr/bin/env python3
"""
Created: Early 2024
Last Modified: 2024-01-22

Description:
    This script is designed to extract Indicators of Compromise (IoCs) from text input.
    It interacts with the api.iocparser.com to parse various types of IoCs from the provided text.
    Users can input text directly or via a file, and the script supports multiple output formats
    including YAML, TXT, CSV, and JSON. The script also enhances readability by colorizing the output
    in the terminal.

Dependencies:
    - requests: For making HTTP requests to the API.
    - yaml: For YAML output formatting.
    - csv: For CSV output formatting.
    - json: For JSON output formatting.
    - termcolor: For colorizing terminal output.
    - prompt_toolkit: For handling multi-line text input in the terminal.
"""

import argparse
import io
import os
import platform
import requests
import yaml
import csv
import json
import re
from termcolor import colored
from prompt_toolkit import PromptSession
from prompt_toolkit.input.defaults import create_input
from prompt_toolkit.output.defaults import create_output

# Define the supported IoC keys
SUPPORTED_KEYS = ["ASN", "BITCOIN_ADDRESS", "CVE", "DOMAIN", "EMAIL", "FILE_HASH_MD5", "FILE_HASH_SHA1", "FILE_HASH_SHA256", "IPv4", "IPv6", "MAC_ADDRESS", "MITRE_ATT&CK", "URL", "YARA_RULE"]

def parse_arguments():
    parser = argparse.ArgumentParser(description='IoC Extractor Helper. Once prompted, copy and paste text into console. Press \'Esc\' followed by \'Enter\' to submit.')
    parser.add_argument('--input', '-i', help='Input file path', type=str)
    parser.add_argument('--output', '-o', help='Output file path', type=str)
    parser.add_argument('--nodefang', action='store_true', help='Opt out of defanging IoCs')
    parser.add_argument('--format', choices=['yaml', 'txt', 'csv', 'json'], default='yaml', help='Output format')
    return parser.parse_args()

def extract_guessed_ips(data):
    guessed_ip_patterns = re.findall(r'\b(?:\d{1,3}-){3}\d{1,3}\b', data)
    return [ip.replace('-', '.') for ip in guessed_ip_patterns]

def defang_ioc(ioc, ioc_type):
    defanged_ioc = ioc
    if ioc_type.lower() in ["ipv4", "ipv6", "domain", "hosts", "url", "guessed_ip", "guessed_ipv4"]:
        defanged_ioc = defanged_ioc.replace('.', '[.]')
        defanged_ioc = defanged_ioc.replace('http', 'hxxp')
    return defanged_ioc

def read_input(args):
    if args.input:
        with open(args.input, 'r') as file:
            return file.read()
    else:
        # Create a prompt session with support for multi-line input
        session = PromptSession(input=create_input(), output=create_output())

        print("Enter or paste your text here. Press 'Esc' followed by 'Enter' to submit.")
        try:
            # Capture multi-line input
            text = session.prompt(multiline=True)
            return text
        except KeyboardInterrupt:
            # Handle the interrupt gracefully
            return ""

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def send_request(data):
    url = "https://api.iocparser.com/raw"
    headers = {'Content-Type': 'text/plain'}
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_data = response.json()

        # Extract and filter the 'data' field
        ioc_data = response_data.get('data', {})
        filtered_data = {key: value for key, value in ioc_data.items() if value}

        return filtered_data
    except requests.exceptions.HTTPError as http_err:
        print(colored(f"HTTP error occurred: {http_err}", 'red'))
    except requests.exceptions.RequestException as req_err:
        print(colored(f"Error sending request: {req_err}", 'red'))
    except requests.exceptions.JSONDecodeError:
        print(colored("Failed to parse JSON response. The server might have returned an unexpected response.", 'red'))
    return None

def format_output(data, output_format):
    if output_format == 'csv':
        # CSV formatting
        if not data:
            return ""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ioc_type', 'ioc'])
        for ioc_type, iocs in data.items():
            for ioc in iocs:
                writer.writerow([ioc_type, ioc])
        return output.getvalue()

    elif output_format in ['yaml', 'txt']:
        # Custom colored output for YAML and TXT formats
        colored_output = ""
        for ioc_type, iocs in data.items():
            colored_output += colored(ioc_type + ":\n", 'red')
            for ioc in iocs:
                colored_output += "  - " + ioc + "\n"
        return colored_output

    elif output_format == 'json':
        # JSON formatting
        return json.dumps(data, indent=4)

    else:
        # Custom colored output for text
        colored_output = ""
        for ioc_type, iocs in data.items():
            colored_output += colored(ioc_type + ":\n", 'blue')
            for ioc in iocs:
                colored_output += "  - " + colored(ioc, 'green') + "\n"
        return colored_output

def save_output(data, file_path):
    with open(file_path, 'w') as file:
        file.write(data)

def main():
    args = parse_arguments()
    input_data = read_input(args)
    response_data = send_request(input_data)
    formatted_output = format_output(response_data, args.format)

    # Extract and add guessed IPs
    guessed_ips = extract_guessed_ips(input_data)
    if guessed_ips:
        response_data['GUESSED_IPv4'] = guessed_ips

    # Defang IoCs if the user hasn't opted out
    if not args.nodefang:
        for ioc_type, iocs in response_data.items():
            response_data[ioc_type] = [defang_ioc(ioc, ioc_type) for ioc in iocs]

    clear_screen()  # Clear the screen before printing output
    formatted_output = format_output(response_data, args.format)

    if args.output:
        save_output(formatted_output, args.output)
    else:
        print(formatted_output)

if __name__ == "__main__":
    main()
