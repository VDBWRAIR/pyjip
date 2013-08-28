#!/usr/bin/env python
"""
List all JIP tools/scripts that are available in the search paths.

Usage:
   jip-tools [--help|-h]

Other Options:
    -h --help             Show this help message
"""

from os import getcwd, getenv
import jip
from jip.utils import scan_modules, render_table, scan_scripts
from . import parse_args


def main():
    args = parse_args(__doc__, options_first=True)
    print "Tools scripts"
    print "-------------"
    print "Please note that there might be more. Here, we search only for"
    print "files with the .jip extension!"
    print ""
    print "Search paths:"
    print "Current directory: %s" % getcwd()
    print "Jip configuration: %s" % jip.configuration.get("jip_path", "")
    print "JIP_PATH variable: %s" % getenv("JIP_ENV", "")
    print ""
    rows = []
    for name, path in scan_scripts().iteritems():
        rows.append((name, path))
    print render_table(["Name", "Path"], rows)
    print ""

    print "Tools implemented in Python modules"
    print "-----------------------------------"
    print "The modules mus be available in PYTHONPATH and must be specified"
    print "in the jip configuration or in the JIP_MODULES environment"
    print "variable. Please note that pipeline scripts that contain"
    print "python blocks are allowed to load modules that contain tool"
    print "implementation. These tools might not be found by this scan!"
    print ""
    print "Jip configuration: %s" % jip.configuration.get("jip_modules", "")
    print "JIP_PATH variable: %s" % getenv("JIP_MODULES", "")
    print ""
    rows = []
    for name, cls in scan_modules().iteritems():
        help = cls.help()
        description = "-"
        if help is not None:
            description = help.split("\n")[0]
        if len(description) > 60:
            description = "%s ..." % description[46]
        rows.append((name, description))
    print render_table(["Tool", "Description"], rows)

if __name__ == "__main__":
    main()