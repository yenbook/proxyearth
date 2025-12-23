#!/usr/bin/env python3
"""
OSINT Aggregator - Usage Examples
==================================

This file demonstrates various ways to use the OSINT Aggregator
both via the CLI and programmatically.

Run this file to see example outputs:
    python examples.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.username_enum import UsernameEnumerator, quick_check


def example_1_basic_username_check():
    """Example 1: Basic username check using quick_check function"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Username Check")
    print("="*70)

    username = "github"  # Replace with any username
    print(f"Checking username: {username}\n")

    results = quick_check(username)

    # Print summary
    found_count = sum(1 for r in results if r.get("exists"))
    print(f"\n✅ Username '{username}' found on {found_count} platforms")


def example_2_specific_platforms():
    """Example 2: Check specific platforms only"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Check Specific Platforms")
    print("="*70)

    username = "test"
    platforms = ["GitHub", "Reddit"]  # Only check these

    print(f"Checking username '{username}' on: {', '.join(platforms)}\n")

    enumerator = UsernameEnumerator()
    results = enumerator.enumerate_all(username, platforms)
    enumerator.close()

    for result in results:
        if result['exists']:
            print(f"✅ Found: {result['url']}")


def example_3_custom_settings():
    """Example 3: Using custom timeout and delay"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Custom Timeout and Delay Settings")
    print("="*70)

    username = "python"

    # Custom settings: 5 second timeout, 0.5 second delay
    enumerator = UsernameEnumerator(timeout=5, delay=0.5)

    print(f"Checking '{username}' with custom settings (timeout=5s, delay=0.5s)\n")

    results = enumerator.enumerate_all(username)
    summary = enumerator.get_summary(results)

    print(f"\nSummary:")
    print(f"  Total checked: {summary['total_checked']}")
    print(f"  Found: {summary['found_on']}")
    print(f"  Success rate: {summary['success_rate']}%")

    enumerator.close()


def example_4_programmatic_access():
    """Example 4: Programmatic access to results"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Programmatic Access to Results")
    print("="*70)

    username = "opensource"

    enumerator = UsernameEnumerator()
    results = enumerator.enumerate_all(username)

    # Filter only found accounts
    found_accounts = [r for r in results if r.get('exists')]

    print(f"\nFound {len(found_accounts)} accounts:")
    for account in found_accounts:
        print(f"  - {account['platform']}: {account['url']}")

    # Export to dictionary for further processing
    export_data = {
        "username": username,
        "accounts": [
            {
                "platform": r['platform'],
                "url": r['url'],
                "status_code": r.get('status_code')
            }
            for r in found_accounts
        ]
    }

    print(f"\nExport data structure:")
    import json
    print(json.dumps(export_data, indent=2))

    enumerator.close()


def example_5_error_handling():
    """Example 5: Handling errors gracefully"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Error Handling")
    print("="*70)

    username = "example_user"

    enumerator = UsernameEnumerator(timeout=2)  # Short timeout to demonstrate errors
    results = enumerator.enumerate_all(username)

    # Check for errors
    errors = [r for r in results if r.get('status') == 'error']

    if errors:
        print(f"\n⚠️  Encountered {len(errors)} errors:")
        for error in errors:
            print(f"  - {error['platform']}: {error['message']}")
    else:
        print("\n✅ No errors encountered")

    enumerator.close()


def main():
    """Run all examples"""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║         OSINT Aggregator - Usage Examples                     ║
    ║         Demonstrating programmatic usage                      ║
    ╚════════════════════════════════════════════════════════════════╝
    """)

    print("\nThese examples show how to use the OSINT Aggregator")
    print("programmatically in your own Python scripts.\n")

    # Run examples
    try:
        example_1_basic_username_check()
        example_2_specific_platforms()
        example_3_custom_settings()
        example_4_programmatic_access()
        example_5_error_handling()

        print("\n" + "="*70)
        print("All examples completed!")
        print("="*70)

        print("\n💡 TIP: You can also use the CLI for quick checks:")
        print("   python scanner.py --username <username>")

    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
