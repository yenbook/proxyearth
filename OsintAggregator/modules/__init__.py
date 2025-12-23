"""
OSINT Aggregator Modules
=========================

This package contains modular OSINT reconnaissance components:
- username_enum: Username enumeration across platforms
- email_breach: Email data breach checking (coming soon)
- ip_lookup: IP geolocation and reputation (coming soon)
"""

from .username_enum import UsernameEnumerator, quick_check

__all__ = ["UsernameEnumerator", "quick_check"]
