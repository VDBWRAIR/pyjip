#!/usr/bin/env python
"""
This is the master and control command for jip. Use it to invoke supported
sub-command to launch, check, and modify jobs.

Usage:
    jip [--loglevel <level>] [-p] <command> [<args>...]
    jip [--version] [--help]

Options:
    -p, --pipeline      the file contains a pipeline (interpreter mode)
    -h --help           Show this help message
    --version           Show the version information
    --loglevel <level>  Set the JIP log level to one of error|warn|info|debug

The commands to execute jobs:

    run     Locally run a jip script
    submit  submit a jip script to a remote cluster
    bash    Run or submit a bash command

The following command can be used to show and filter a list of
jobs:

    jobs    list and update jobs from the job database

The jip jobs command output can be piped into one of the following
action command. Note that the commands also work standalone:

    delete   delete the selected jobs
    archive  archive the selected jobs
    cancel   cancel selected and running jobs
    hold     put selected jobs on hold
    restart  restart selected jobs
    logs     show log files of jobs

Miscellaneous other commands:

    tools     list all tools available through the search paths
    profiles  list all available profiles
    edit      edit job commands for a given job
    clean     remove job logs
    check     check job status
"""
import os
import sys
import jip
import jip.options
import jip.tools
import jip.cli
import jip.cluster
import jip.configuration

from jip.logger import getLogger, log_level
from jip.vendor.docopt import docopt

log = getLogger('jip.cli.jip_main')


def main():
    try:
        jip.configuration.install_path = os.path.abspath(
            os.path.dirname(sys.argv[0])
        )
    except:
        pass

    try:
        _main()
    except jip.options.ParserException as err:
        log.debug("parser error: %s", str(err), exc_info=True)
        sys.stderr.write(str(err))
        sys.exit(1)
    except jip.ValidationError as va:
        log.debug("validation error: %s", str(va), exc_info=True)
        sys.stderr.write(str(va))
        sys.stderr.write("\n")
        sys.exit(1)
    except jip.tools.ToolNotFoundException as notFound:
        log.debug("Tool not found: %s", str(notFound), exc_info=True)
        print >>sys.stderr, jip.cli.colorize(str(notFound), jip.cli.RED)
        print >>sys.stderr, """\

Check your search paths and your jip configuration to include and
find tool definitions that are not in any default paths.
"""
        sys.exit(1)
    except jip.cluster.ClusterImplementationError as notFound:
        log.debug("Cluster not found: %s", str(notFound), exc_info=True)
        print >>sys.stderr, jip.cli.colorize(str(notFound), jip.cli.RED)
        sys.exit(1)
    except jip.cluster.SubmissionError as notFound:
        log.debug("Submission error: %s", str(notFound), exc_info=True)
        print >>sys.stderr, jip.cli.colorize(str(notFound), jip.cli.RED)
        sys.exit(1)


def _main():
    args = docopt(__doc__, version=str(jip.__version__),
                  options_first=True, help=True)
    if args['--loglevel']:
        log_level(args['--loglevel'])
    cmd = args['<command>']
    if not cmd:
        docopt(__doc__, version='1.0', options_first=True, argv=['--help'],
               help=True)
        sys.exit(1)

    try:
        import runpy
        argv = ["jip-" + cmd] + args['<args>']
        sys.argv = argv  # reset options
        runpy.run_module("jip.cli.jip_%s" % cmd, run_name="__main__")
    except ImportError:
        log.debug("Import error, trying command. Here is the exception:",
                  exc_info=True)
        # check interpreter mode
        import os
        if os.path.exists(cmd):
            import runpy
            argv = ["jip-interpreter"] + \
                ([] if not args['--pipeline'] else ['--pipeline']) + \
                [cmd] + args['<args>']
            sys.argv = argv  # reset options
            runpy.run_module("jip.cli.jip_interpreter", run_name="__main__")
        else:
            sys.stderr.write("\nCommand %s not found\n\n" % (cmd))
            docopt(__doc__, version='1.0', options_first=True, argv=['--help'],
                   help=True)
            sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
