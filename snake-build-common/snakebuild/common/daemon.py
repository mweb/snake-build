# -*- coding: utf-8 -*-

"""
Copyright (c) 2006-2007 by:
    Blue Dynamics Alliance Klein & Partner KEG, Austria
    Squarewave Computing Robert Niederreiter, Austria

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted, provided that
the above copyright notice appear in all copies and that both that copyright
notice and this permission notice appear in supporting documentation, and that
the name of Stichting Mathematisch Centrum or CWI not be used in advertising
or publicity pertaining to distribution of the software without specific,
written prior permission.

STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.

References:
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012

History:
    2001/07/10 by Juergen Hermann
    2002/08/28 by Noah Spurrier
    2003/02/24 by Clark Evans
    2006/01/25 by Robert Niederreiter
    2008/06/06 by Mathias Weber

Class Daemon is used to run any routine in the background on unix environments
as daemon.

There are several things to consider:

*The instance object given to the constructor MUST provide a run method with
represents the main routine of the deamon

*The instance object MUST provide global file descriptors for (and named as):
    -stdin
    -stdout
    -stderr

*The instance object MUST provide a global (and named as) pidfile.
"""

__author__ = """Robert Niederreiter <office@squarewave.at>"""
__version__ = 0.2
__docformat__ = 'plaintext'

# python imports
import os
import sys
import time
import logging


from signal import SIGTERM

log = logging.getLogger('resourcehandler.common.Daemon')


class Daemon(object):
    START, STOP, RESTART, UNKNOWN = range(4)
    UMASK = 0
    WORKDIR = "."
    instance = None
    startmsg = 'started with pid %s'

    def __init__(self, instance, action):
        ''' Depending on the defined action the given instance of a class
            will be run as a daemonized process. This will happen if the action
            is set to START or RESTART. On STOP the former running instance
            should be stoped. This only works if the pid file is stored
            correctly.
            The instance needs to have a method run and and the following
            instance variables:
              * pidfile    holds the path to a file to store the proces
              * stdin      a file for the stdin channel
              * stdout     a file for the stdout channel
              * stderr     a file for the stderr channel

            @param instance: the class instance that offers the run method
            @param action: specifies if the application should be started/
                        restart or stoped
        '''
        self.instance = instance
        self.startstop(action)
        instance.run()

    def deamonize(self):
        """Fork the process into the background.
        """
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            log.error("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir(self.WORKDIR)
        os.umask(self.UMASK)
        os.setsid()

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            log.error("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        if not self.instance.stderr:
            self.instance.stderr = self.instance.stdout

        si = file(self.instance.stdin, 'r')
        so = file(self.instance.stdout, 'a+')
        se = file(self.instance.stderr, 'a+', 0)

        pid = str(os.getpid())

        log.info("\n%s\n" % self.startmsg % pid)
        sys.stderr.flush()

        if self.instance.pidfile:
            file(self.instance.pidfile, 'w+').write("%s\n" % pid)

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

    def startstop(self, action):
        """Start/stop/restart behaviour.

            @param action: this defines if the action for the application.
        """
        try:
            pf = file(self.instance.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if action == self.STOP or action == self.RESTART:
            if not pid:
                log.error("Could not stop, pid file '%s' missing.\n" %
                        self.instance.pidfile)
                sys.exit(1)
            try:
                while 1:
                    os.kill(pid, SIGTERM)
                    time.sleep(1)
            except OSError, err:
                err = str(err)
                if err.find("No such process") > 0:
                    os.remove(self.instance.pidfile)
                    if action == self.STOP:
                        sys.exit(0)
                    action = self.START
                    pid = None
                else:
                    print str(err)
                    sys.exit(1)
        if action == self.START:
            if pid:
                log.error("Start aborded since pid file '%s' exists.\n" % \
                        self.instance.pidfile)
                sys.exit(1)
            self.deamonize()
            return