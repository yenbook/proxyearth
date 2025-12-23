"""
Username Enumeration Module
============================
This module checks username availability across multiple social media platforms
and public repositories. It's designed to be modular and easily extensible.

Author: OsintAggregator
License: MIT
"""

import requests
import time
from typing import Dict, List, Optional
from urllib.parse import quote


class UsernameEnumerator:
    """
    A modular class for enumerating username availability across platforms.

    HOW TO ADD MORE SOURCES:
    1. Add the platform URL pattern to the PLATFORMS dictionary
    2. The {username} placeholder will be replaced with the actual username
    3. Define the expected HTTP status codes for "found" and "not found"
    4. Add any custom headers if needed in the check_username method
    """

    # Platform definitions - EASILY EXTENSIBLE
    # Format: "Platform Name": {"url": "url_pattern", "found_code": 200, "not_found_code": 404}
    PLATFORMS = {
        "GitHub": {
            "url": "https://github.com/{username}",
            "found_code": 200,
            "not_found_code": 404,
            "method": "GET"
        },
        "Instagram": {
            "url": "https://www.instagram.com/{username}/",
            "found_code": 200,
            "not_found_code": 404,
            "method": "GET"
        },
        "Twitter/X": {
            "url": "https://twitter.com/{username}",
            "found_code": 200,
            "not_found_code": 404,
            "method": "GET"
        },
        "Reddit": {
            "url": "https://www.reddit.com/user/{username}",
            "found_code": 200,
            "not_found_code": 404,
            "method": "GET"
        },
        "Medium": {
            "url": "https://medium.com/@{username}",
            "found_code": 200,
            "not_found_code": 404,
            "method": "GET"
        },
        # ADD MORE PLATFORMS HERE from Awesome OSINT repository
        # Example:
        # "LinkedIn": {
        #     "url": "https://www.linkedin.com/in/{username}",
        #     "found_code": 200,
        #     "not_found_code": 404,
        #     "method": "GET"
        # },
    }

    def __init__(self, timeout: int = 10, delay: float = 1.0):
        """
        Initialize the UsernameEnumerator.

        Args:
            timeout (int): Request timeout in seconds (default: 10)
            delay (float): Delay between requests in seconds to avoid rate limiting (default: 1.0)
        """
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()

        # Set a realistic User-Agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def check_username(self, username: str, platform_name: str) -> Dict[str, any]:
        """
        Check if a username exists on a specific platform.

        Args:
            username (str): The username to check
            platform_name (str): The platform name (must exist in PLATFORMS dict)

        Returns:
            dict: Result containing status, url, and any error information
        """
        if platform_name not in self.PLATFORMS:
            return {
                "platform": platform_name,
                "status": "error",
                "message": f"Platform '{platform_name}' not configured",
                "url": None,
                "exists": False
            }

        platform = self.PLATFORMS[platform_name]
        url = platform["url"].format(username=quote(username))

        try:
            # Make the request
            response = self.session.get(
                url,
                timeout=self.timeout,
                allow_redirects=True
            )

            # Check if username exists based on status code
            exists = response.status_code == platform["found_code"]

            result = {
                "platform": platform_name,
                "status": "success",
                "url": url,
                "exists": exists,
                "status_code": response.status_code
            }

            # Add delay to avoid rate limiting
            time.sleep(self.delay)

            return result

        except requests.exceptions.Timeout:
            return {
                "platform": platform_name,
                "status": "error",
                "message": "Request timed out",
                "url": url,
                "exists": False
            }

        except requests.exceptions.ConnectionError:
            return {
                "platform": platform_name,
                "status": "error",
                "message": "Connection failed - site may be blocking requests",
                "url": url,
                "exists": False
            }

        except requests.exceptions.TooManyRedirects:
            return {
                "platform": platform_name,
                "status": "error",
                "message": "Too many redirects",
                "url": url,
                "exists": False
            }

        except requests.exceptions.RequestException as e:
            return {
                "platform": platform_name,
                "status": "error",
                "message": f"Request failed: {str(e)}",
                "url": url,
                "exists": False
            }

        except Exception as e:
            return {
                "platform": platform_name,
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "url": url,
                "exists": False
            }

    def enumerate_all(self, username: str, platforms: Optional[List[str]] = None) -> List[Dict]:
        """
        Check username across all configured platforms or a subset.

        Args:
            username (str): The username to check
            platforms (list, optional): List of platform names to check. If None, checks all.

        Returns:
            list: List of result dictionaries for each platform
        """
        if platforms is None:
            platforms = list(self.PLATFORMS.keys())

        results = []

        print(f"\n🔍 Checking username '{username}' across {len(platforms)} platforms...\n")

        for i, platform_name in enumerate(platforms, 1):
            print(f"[{i}/{len(platforms)}] Checking {platform_name}...", end=" ")

            result = self.check_username(username, platform_name)
            results.append(result)

            # Print result
            if result["status"] == "success":
                if result["exists"]:
                    print(f"✅ FOUND - {result['url']}")
                else:
                    print(f"❌ Not found")
            else:
                print(f"⚠️  ERROR - {result['message']}")

        return results

    def get_summary(self, results: List[Dict]) -> Dict[str, any]:
        """
        Generate a summary of enumeration results.

        Args:
            results (list): List of result dictionaries from enumerate_all

        Returns:
            dict: Summary statistics
        """
        total = len(results)
        found = sum(1 for r in results if r.get("exists", False))
        errors = sum(1 for r in results if r.get("status") == "error")

        found_on = [r["platform"] for r in results if r.get("exists", False)]

        return {
            "total_checked": total,
            "found_on": found,
            "not_found": total - found - errors,
            "errors": errors,
            "platforms_found": found_on,
            "success_rate": round((total - errors) / total * 100, 2) if total > 0 else 0
        }

    def close(self):
        """Close the session."""
        self.session.close()


# Convenience function for quick checks
def quick_check(username: str, platforms: Optional[List[str]] = None) -> List[Dict]:
    """
    Quick function to check a username without instantiating the class.

    Args:
        username (str): Username to check
        platforms (list, optional): Platforms to check

    Returns:
        list: Results from enumeration
    """
    enumerator = UsernameEnumerator()
    try:
        results = enumerator.enumerate_all(username, platforms)
        return results
    finally:
        enumerator.close()


if __name__ == "__main__":
    # Example usage when run directly
    import sys

    if len(sys.argv) < 2:
        print("Usage: python username_enum.py <username>")
        print("Example: python username_enum.py johndoe")
        sys.exit(1)

    username = sys.argv[1]
    results = quick_check(username)

    # Print summary
    enumerator = UsernameEnumerator()
    summary = enumerator.get_summary(results)

    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"Total platforms checked: {summary['total_checked']}")
    print(f"Username found on: {summary['found_on']} platform(s)")
    print(f"Not found on: {summary['not_found']} platform(s)")
    print(f"Errors: {summary['errors']}")
    print(f"Success rate: {summary['success_rate']}%")

    if summary['platforms_found']:
        print(f"\n✅ Found on: {', '.join(summary['platforms_found'])}")

    enumerator.close()
