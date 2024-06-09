#
import time
from enum import Enum
from typing import Optional

from colour import Colour, Formatting
from constants import *

"""
The Logger class. You have one logger per project, and do all logging through that.

Parameters:
ignored_subjects (optional) : a list of strings, representing subjects to ignore. If you try to print a message with one of these
subjects, it will not appear in the shell.

ignored_severities (optional) : a list of strings (although the default severities are in an enum, as NORMAL, WARNING and ERROR.) of
severities that are ignored.If you try to print a message with one of these severities, it will not appear in the shell.
"""
class Logger():
    def __init__(self, ignored_subjects:list[str] | None = None, ignored_severities: list[str] | None = None) -> None:
        if ignored_subjects is None:
            ignored_subjects = []
        if ignored_severities is None:
            ignored_severities = []
        self.init_time = time.time()
        self.ignored_subjects = ignored_subjects
        self.ignored_severities = ignored_severities

    """Logs a message with the severity WARNING. Takes a message, and optionally a subject."""
    def warning(self, message:str, subject: str | None =None) -> None:
        self.log(message, severity=WARNING, subject=subject)

    """Logs a message with the severity ERROR. Takes a message, and optionally a subject."""
    def error(self, message:str, subject: str | None = None) -> None:
        self.log(message, severity=ERROR, subject=subject)

    """
    Allows you to log something.
    
    Parameters:
    message: The message
    severity (optional) : The severity of the message. Expressed as enums, these are NORMAL, WARNING and ERROR.
    subject: a string, showing a subject. Allows certain messages to be automatically ignored.
    """
    def log(self, message: str, severity: str=NORMAL, subject: str | None = None) -> None:
        if severity not in [NORMAL, WARNING, ERROR]:
            raise ValueError(f" Severity {severity} is not valid. Use NORMAL, WARNING or ERROR.")
        if not (subject in self.ignored_subjects or self.ignored_subjects == ALL or severity in self.ignored_severities):
            if subject is None: subject = ""
            else: subject = subject + " "
            self._log(message, severity, subject)

    def _log(self, message: str, severity: str=NORMAL, subject: str | None = None) -> None:
        # ============== TIME ============== #
        # Find the time since the initialisation of logger
        message_time = time.time() - self.init_time
        # Convert to h, m, s
        hours, minutes = divmod(message_time, 60*60)
        minutes, seconds = divmod(minutes, 60)
        # Compile to string, strip any that is zero
        message_time_str = ""
        for timesegment in [f"{int(hours)}h", f"{int(minutes)}m", f"{int(seconds)}s"]:
            if not timesegment[0] == "0":
                message_time_str = message_time_str + timesegment

        # ============= COLOURS ============ #
        prefix_background = None
        prefix_text_colour = Colour.F_Black
        message_text_colour = None
        if severity == NORMAL:
            prefix_background = Colour.B_Blue
            message_text_colour = Colour.F_Blue
        elif severity == WARNING:
            prefix_background = Colour.B_Yellow
            message_text_colour = Colour.F_Yellow
        elif severity == ERROR:
            prefix_background = Colour.B_Red
            message_text_colour = Colour.F_Red

        # ============ PRINT ============== #
        prefix = f"{prefix_background}{prefix_text_colour}{subject}{severity} @ {message_time_str}{Formatting.Reset}"
        message_formatted = f"{message_text_colour}{message}{Formatting.Reset}"
        print(prefix, message_formatted)

if __name__ == "__main__":
    l = Logger()
    time.sleep(1)
    l.log("Portal opened on Level 2", subject="portals")
    l.log("hi", severity=WARNING, subject="hi's")
    time.sleep(1)
    l.log("Will stupid artists stop putting terrain over the cutoff height we've all agreed upon?", severity=ERROR)