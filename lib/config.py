#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2012, Rui Carmo
Description: Shared configuration data
License: MIT (see LICENSE.md for details)
"""

import os, sys, platform, logging.config
from utils import get_config, path_for, tb

try:
    settings
except NameError:
    for host in [platform.node(), 'default']:
        try:
            settings = get_config(path_for(os.path.join('etc','%s.json' % host)))
        except IOError:
            continue
        except Exception as e:
            tb = tb()
            print tb
            if sys.stderr.isatty():
                print >> sys.stderr, ("Error while loading %(host)s.json: %(tb)s" % locals())
            else:
                log.error("Error while loading %(host)s.json: %(tb)s" % locals())
            sys.exit(2)
        logging.config.dictConfig(dict(settings.logging))
        log = logging.getLogger()
        log.info("Configuration for %s loaded." % host)
        break
