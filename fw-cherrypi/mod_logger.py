#!/usr/bin/python3
"""
This module provides logging functions, including colourisation.
"""
import os

class ClassANSIColourCodes:
    RESET = u"\u001b[0m"
    BOLD = u"\u001b[1m"
    BOLD2 = "\033[1m"
    UNDERLINE = u"\u001b[4m"
    UNDERLINE2 = "\033[4m"
    REVERSED = u"\u001b[7m"
    NEGATIVE = "\033[7m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    BLINK = "\033[5m"
    CROSSED = "\033[9m"

    blue = u"\u001b[34m"
    red = u"\u001b[31m"
    black = u"\u001b[30m"
    green = u"\u001b[32m"
    yellow = u"\u001b[33m"
    magenta = u"\u001b[35m"
    cyan = u"\u001b[36m"
    white = u"\u001b[37m"

    bright_black = u"\u001b[30;1m"
    bright_red = u"\u001b[31;1m"
    bright_green = u"\u001b[32;1m"
    bright_yellow = u"\u001b[33;1m"
    bright_blue = u"\u001b[34;1m"
    bright_magenta = u"\u001b[35;1m"
    bright_cyan = u"\u001b[36;1m"
    bright_white = u"\u001b[37;1m"

    bg_black = u"\u001b[40m"
    bg_red = u"\u001b[41m"
    bg_green = u"\u001b[42m"
    bg_yellow = u"\u001b[43m"
    bg_blue = u"\u001b[44m"
    bg_magenta = u"\u001b[45m"
    bg_cyan = u"\u001b[46m"
    bg_white = u"\u001b[47m"

    bg_bright_black = u"\u001b[40;1m"
    bg_bright_red = u"\u001b[41;1m"
    bg_bright_green = u"\u001b[42;1m"
    bg_bright_yellow = u"\u001b[43;1m"
    bg_bright_blue = u"\u001b[44;1m"
    bg_bright_magenta = u"\u001b[45;1m"
    bg_bright_cyan = u"\u001b[46;1m"
    bg_bright_white = u"\u001b[47;1m"

    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""

class ClassLog:
    debug_level=0
    error_to_file = False
    error_to_syslog = False
    debug_to_file = False
    debug_to_syslog = False
    log_levels = {0: "",
                  1: " - ",
                  2: "  * ",
                  3: "   o ",
                  10: "# ",
                  11: "! ",
                  12: "> ",
                  13: ">> ",
                  -10: "ERROR: ",
                  -900: "DEBUG: ",
                  -901: "DEBUG 01-: ",
                  -902: "DEBUG 02: ",
                  -903: "DEBUG 03: ",
                  -904: "DEBUG 04: ",
                  -905: "DEBUG 05: ",
                  -906: "DEBUG 06: ",
                  -907: "DEBUG 07: ",
                  -908: "DEBUG 08: ",
                  -909: "DEBUG 09: ",
                  -999: "DEBUG 99: "}

    acc = ClassANSIColourCodes()

    def log(self, log_level, log_text, *args, **kwargs):
        custom_prefix = kwargs.get("custom_prefix", False)
        custom_colour = kwargs.get("custom_colour", False)
        custom_bg_colour = kwargs.get("custom_bg_colour", False)
        log_prefix = self.log_levels.get(log_level, "")
        colour_code = ""
        colour_reset = self.acc.RESET

        if custom_prefix == False:
            if log_level == 999:  # Center Text
                log_text = self.acc.bg_white + self.acc.blue + center_text(log_text, "#") + self.acc.RESET
                log_level = 0
            if log_level >= 0:
                log_prefix = self.log_levels.get(log_level, str(log_level))
            elif log_level < 0 and log_level >= -10:
                log_prefix = "ERROR " + str(abs(log_level - 100))[1:] + ": "  # In the ERROR range
                colour_code = self.acc.red
            elif log_level <= 900 and log_level >= -999:
                log_prefix = "DEBUG " + str(abs(log_level))[1:] + ": "  # In the DEBUG range
                colour_code = self.acc.yellow
        else:
            log_prefix = custom_prefix

        if custom_colour:
            colour_code = custom_colour
            # print("Set FG: ")
            # print("   ", repr(colour_code))
            # print("Set FG")

        if custom_bg_colour:
            colour_code = colour_code + custom_bg_colour
            # print("Set BG: ")
            # print("   ", repr(custom_bg_colour))
            # print("   ", repr(colour_code))

        if log_level >= (self.debug_level * -1):
            fprint(colour_code + log_prefix + colour_reset + log_text + ''.join(args))
            # print(repr(colour_code + log_prefix + colour_reset + log_text + ''.join(args)))

def get_terminal_size():
    stty = "25 80"
    try:
        stty = os.popen('stty size', 'r').read()
        stty =  "25 80" if stty == "" else stty
    except Exception as error:
        print("STTY Error:", error)
    return stty.split()

def center_text(text_to_center, pad_character, *args):
    rows, columns = get_terminal_size()

    args = args + ("", "", "", "","")
    pre_string = args[0] if len(args) >= 0 else None
    post_string = args[1] if len(args) > 0 else None
    pad_character += " "
    space_left = int((int(columns) - len(text_to_center)) / 2)
    pad_left = pad_character[0] * space_left
    return (pre_string + pad_left + text_to_center + pad_left + post_string)

def fprint(text_to_print, *args, **kwargs):
    print(text_to_print, ''.join(args))
