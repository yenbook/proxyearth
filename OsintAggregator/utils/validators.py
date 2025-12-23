"""
Input Validation Utilities
===========================

Functions for validating different types of user input.
"""

import re
from typing import Tuple


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username format.

    Args:
        username (str): Username to validate

    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not username:
        return False, "Username cannot be empty"

    if len(username) < 1:
        return False, "Username too short"

    if len(username) > 50:
        return False, "Username too long (max 50 characters)"

    # Allow alphanumeric, underscores, hyphens
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"

    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format.

    Args:
        email (str): Email to validate

    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not email:
        return False, "Email cannot be empty"

    # RFC 5322 simplified regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        return False, "Invalid email format"

    if len(email) > 254:  # RFC 5321
        return False, "Email too long"

    local, domain = email.rsplit('@', 1)

    if len(local) > 64:  # RFC 5321
        return False, "Email local part too long"

    return True, ""


def validate_ip(ip: str) -> Tuple[bool, str]:
    """
    Validate IPv4 address format.

    Args:
        ip (str): IP address to validate

    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not ip:
        return False, "IP address cannot be empty"

    # IPv4 pattern
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

    if not re.match(pattern, ip):
        return False, "Invalid IP address format"

    # Check each octet is 0-255
    parts = ip.split('.')

    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False, f"Invalid octet value: {num} (must be 0-255)"
        except ValueError:
            return False, f"Invalid octet: {part}"

    return True, ""


def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate URL format.

    Args:
        url (str): URL to validate

    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not url:
        return False, "URL cannot be empty"

    # Basic URL validation
    url_pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'

    if not re.match(url_pattern, url):
        return False, "Invalid URL format (must start with http:// or https://)"

    return True, ""


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input to prevent injection attacks.

    Args:
        user_input (str): Raw user input

    Returns:
        str: Sanitized input
    """
    # Remove control characters
    sanitized = ''.join(char for char in user_input if ord(char) >= 32 or char == '\n')

    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    return sanitized
