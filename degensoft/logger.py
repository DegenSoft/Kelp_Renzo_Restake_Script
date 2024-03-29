# -*- coding: utf-8 -*-
import re
import logging

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')


def setup_file_logging(logger, log_file: str, formatter: logging.Formatter = log_formatter) -> None:
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def convert_urls_to_links(string: str) -> str:
    # Regular expression pattern to match URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    def replace_url(match):
        url = match.group(0)
        return '<a href="{0}">{0}</a>'.format(url)

    # Replace URLs with clickable links
    result = re.sub(url_pattern, replace_url, string)
    return result


def mask_hex_in_string(string: str) -> str:
    # Split the input string into parts using "a href" tags
    pattern_link = re.compile(r'(<a href=".*?".*?>)', re.DOTALL)
    parts = pattern_link.split(string)
    pattern_hex = re.compile(r'(0x)([0-9a-fA-F]+)')
    # Process each part of the string
    for i in range(len(parts)):
        # If the part contains a link, leave it unchanged
        if pattern_link.fullmatch(parts[i]):
            continue
        # Replace hex values with asterisks, keeping the first and last 4 characters
        else:
            parts[i] = pattern_hex.sub(
                lambda m: m.group(1) + m.group(2)[:4] + '*' * (len(m.group(2)) - 8) + m.group(2)[-4:], parts[i])
    return ''.join(parts)
