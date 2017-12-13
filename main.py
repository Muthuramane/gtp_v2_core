#!/usr/bin/env python
# encoding: utf-8
'''
main -- shortdesc

main is a description

It defines classes_and_methods

@author:     Rosalia d'Alessandro

@copyright:  2017. All rights reserved.

@license:    license

@contact:    list_mailing@libero.it
'''

import sys
import os

from optparse import OptionParser
from utilities.configuration_parser import *

__all__ = []
__version__ = 0.1


DEBUG = 1
TESTRUN = 0
PROFILE = 0

GTP_PORT = 2123
DEFAULT_MSG_FREQ = 20
DEFAULT_SLEEPTIME = 1

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"

    program_version_string = '%%prog %s' % (program_version)

    program_license = "Copyright 2017 Rosalia d'Alessandro                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, description=program_license)
        parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
        parser.add_option("-s", "--server_mode", dest="server_mode", action="store_true", help="the software will act as server [default: %default]")
        parser.add_option("-c", "--config", dest="config_file", help="the configuration file")
        parser.add_option("-m", "--msg-freq", dest="msg_freq", type=int, help="determine the frequency of the messages. Set the sleep time between each message [default: %default]")
        parser.add_option("-d", "--delay", dest="delay", type=int, help="set the sleep time before start sending messages, it is the negotiation time [default: %default]")
        parser.add_option("-f", "--fuzzy", dest="is_fuzzy", action="store_true", help="set if is fuzzy [default: %default]")
        parser.add_option("-i", "--local_ip", dest="local_ip", help="local ip address")
        parser.add_option("-r", "--remote_ip", dest="remote_ip", help="remote ip address")        
        
        # set defaults
        parser.set_defaults(server_mode=False, config_file="", 
                            msg_freq=DEFAULT_SLEEPTIME, is_fuzzy=False,
                            delay=DEFAULT_SLEEPTIME)

        # process options
        (opts, args) = parser.parse_args(argv)

        if opts.verbose > 0:
            print("verbosity level = %d" % opts.verbose)
        server_mode = opts.server_mode
        is_fuzzy = opts.is_fuzzy
        config_file = opts.config_file
        msg_freq = opts.msg_freq
        delay = opts.delay
        local_ip = opts.local_ip
        remote_ip = opts.remote_ip
        
        # MAIN BODY #
        if opts.config_file != "" :
            config = parseConfigs(opts.config_file)
        else :
            config = None
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    sys.exit(main())