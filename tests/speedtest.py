#!/usr/bin/python

import logging
import re
import sys
import time

sys.path.append('../napd/')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

log_format = "%(levelname)-8s %(message)s"
log_stream = logging.StreamHandler()
log_stream.setFormatter(logging.Formatter("%(asctime)s: " + log_format))
log_stream.setLevel(logging.WARNING)
logger.addHandler(log_stream)


import nap

class bonk:
    def __init__(self):
        self.n = nap.Nap()

        #self.n.remove_prefix({ 'name': 'test-schema' }, { 'prefix': '2.0.0.0/8' })
        #self.n.add_prefix({'name': 'test-schema' }, { 'authoritative_source': 'nap', 'prefix': '2.0.0.0/8', 'description': 'test' })



    def clear_db(self):
        """ Clear out everything in the database
        """
        self.nap._execute("TRUNCATE ip_net_plan CASCADE")



    def init_db(self):
        """ Initialise a few things we need in the db, a schema, a pool, a truck
        """



    def prefix_insert(self, argp):
        """ Insert a /16 into the DB
        """
        arg_prefix = argp.split("/")[0]
        arg_pl = argp.split("/")[1]
        if self.n._is_ipv4(arg_prefix):
            m = re.match("([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)", arg_prefix)
            os1 = int(m.group(1))
            os2 = int(m.group(2))
            os3 = int(m.group(3))
            os4 = int(m.group(4))
            count = 2**(32-int(arg_pl))
            i = 0
            t0 = time.time()
            try:
                for o1 in xrange(os1, 255):
                    for o2 in xrange(os2, 255):
                        for o3 in xrange(os3, 255):
                            t2 = time.time()
                            for o4 in xrange(os4, 255):
                                prefix = "%s.%s.%s.%s" % (o1, o2, o3, o4)
                                self.n.add_prefix({'name': 'test-schema' }, { 'authoritative_source': 'nap', 'prefix': prefix, 'description': 'test' })
                                i += 1
                                if i >= count:
                                    raise StopIteration()
                            t3 = time.time()
                            print o3, (t3-t2)/256
            except StopIteration:
                pass
            t1 = time.time()
            print count, "prefixes added in:", t1-t0


        elif self.n._is_ipv6(argp):
            print >> sys.stderr, "IPv6 is currently unsupported"




    def test1(self):

        t0 = time.time()
        res = self.n.find_free_prefix({ 'schema_name': 'test-schema', 'from-prefix': ['1.0.0.0/8'] }, 32, 1)
        t1 = time.time()
        res = self.n.find_free_prefix({ 'schema_name': 'test-schema', 'from-prefix': ['1.0.0.0/8'] }, 32, 500)
        t2 = time.time()
        for prefix in res:
            self.n.add_prefix({ 'authoritative_source': 'nap', 'schema_name': 'test-schema', 'prefix': prefix, 'description': 'test' })
        t3 = time.time()
        res = self.n.find_free_prefix({ 'schema_name': 'test-schema', 'from-prefix': ['1.0.0.0/8'] }, 32, 1)
        t4 = time.time()
        d1 = t1-t0
        d2 = t2-t1
        d3 = t3-t2
        d4 = t4-t3
        d5 = d4-d1
        print "First find free prefix:", d1
        print "First find of 500 prefixes:", d2
        print "Adding 500 prefixes", d3
        print "Find one prefix after", d4
        print "Diff", d5

    def test2(self):
        t0 = time.time()
        res = self.n.find_free_prefix({ 'schema_name': 'test-schema', 'from-prefix': ['2.0.0.0/8'] }, 32, 1)
        t1 = time.time()
        d1 = t1-t0
        print "Find free prefix:", d1

    def test3(self):
        self.n.find_free_prefix({ 'schema_name': 'test-schema', 'from-prefix': ['2.0.0.0/8'] }, 32, 1)



if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--prefix-insert', metavar = 'PREFIX', help='insert prefixes!')
    b = bonk()

    options, args = parser.parse_args()

    if options.prefix_insert is not None:
        if not b.n._get_afi(options.prefix_insert):
            print >> sys.stderr, "Please enter a valid prefix"
            sys.exit(1)
        b.prefix_insert(options.prefix_insert)

