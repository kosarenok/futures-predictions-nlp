"""
Module: commit_lint.py
Check if commit message follows the Conventional Commits format.

Notes: Conventional Commits format: <type>[optional scope]: <description>
"""

import os
import re
import sys

COMMIT_MESSAGE_FORMAT = "<type>[optional scope]: <description>"


def format_text(text: str, format_type: str) -> str:
    """
    Format text with specified formatting for terminal output.

    Parameters
    ----------
    text : str
        The text to be formatted.
    format_type : str
        The type of formatting ('bold', 'yellow', or 'yellow_bold').

    Returns
    -------
    str
        The formatted text string.

    Notes
    -----
    If an unknown format type is provided, the function returns the original text
    with a warning message.
    """
    format_start = {"bold": "\033[1m", "yellow": "\033[33m", "yellow_bold": "\033[1;33m"}
    format_end = "\033[0m"

    if format_type not in format_start:
        return f"Unknown format type: {format_type}. Text without formatting: {text}"

    return f"{format_start[format_type]}{text}{format_end}"


def read_commit_message():
    """
    Read the commit message from various possible sources.

    Returns
    -------
    str or None
        The commit message if successfully read, None otherwise.

    Notes
    -----
    The function attempts to read the commit message in the following order:
    1. From the COMMIT_EDITMSG file in the .git directory
    2. From stdin if it's not a TTY
    3. From any file arguments passed to the script

    If all attempts fail, it returns None and prints an error message.
    """

    # Try to read from COMMIT_EDITMSG file
    commit_editmsg = os.path.join(os.getcwd(), ".git", "COMMIT_EDITMSG")
    if os.path.exists(commit_editmsg):
        print(f"Debug: Reading from COMMIT_EDITMSG - {commit_editmsg}")
        with open(commit_editmsg, "r", encoding="utf-8") as f:
            return f.read().strip()

    # If COMMIT_EDITMSG doesn't exist, try reading from stdin
    if not sys.stdin.isatty():
        print("Debug: Reading from stdin")
        return sys.stdin.read().strip()

    # If stdin is empty, check if we have any file arguments
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            print(f"Debug: Reading from file argument - {arg}")
            with open(arg, "r", encoding="utf-8") as f:
                return f.read().strip()

    print("Error: Unable to read commit message from any source.")
    return None


def log_error_message(specific_error: str) -> None:
    """
    Print a formatted error message.

    Parameters
    ----------
    specific_error : str
        The specific error message to be included.
    """
    commit_msg_format = format_text(COMMIT_MESSAGE_FORMAT, "yellow_bold")
    error_msg = (
        f"Error: {specific_error}\n"
        f"Commit message does not follow the Conventional Commits format.\n"
        f"...............................................................\n"
        f"Info: https://www.conventionalcommits.org/ru/v1.0.0/\n"
        f"Format should be: {commit_msg_format}\n"
        f"Examples:\n"
        f"   - feat: add login functionality\n"
        f"   - feat: implement new model\n"
        f"   - fix: resolve memory leak\n"
    )
    print(error_msg)


def check_commit_message(commit_msg: str) -> bool:
    """
    Check if commit message follows the Conventional Commits format with optional ticket numbers.

    Parameters
    ----------
    commit_msg : str
        Commit message to check.

    Returns
    -------
    bool
        True if commit message follows the Conventional Commits format, False otherwise.

    Notes
    -----
    Conventional Commits format: <type>[optional scope]: <description>

    Examples
    --------
    Valid commit messages:
        - feat: add login functionality
        - feat: implement new model
        - fix: resolve memory leak
    """
    if not commit_msg:
        log_error_message("Empty commit message received.")
        return False

    print(f"Debug: Received commit message - '{commit_msg}'")

    # Split the commit message into type (with optional scope) and the rest
    parts = commit_msg.split(": ", 1)
    if len(parts) != 2:
        log_error_message("Commit message does not follow the Conventional Commits format.")
        return False

    type_part, description_part = parts

    # Check the type part
    type_pattern = r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z ]+\))?$"
    if not re.match(type_pattern, type_part):
        log_error_message("Invalid commit type or scope.")
        return False

    print("Commit message follows the Conventional Commits format.")
    return True


def main() -> None:
    """
    Main function to run the commit message linting.
    """

    commit_message = read_commit_message()
    if commit_message is None:
        sys.exit(1)

    if not check_commit_message(commit_message):
        sys.exit(1)


if __name__ == "__main__":
    main()
