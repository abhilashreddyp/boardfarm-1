# Copyright (c) 2015
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
import lib

# Import from every file
import os
import glob
import unittest2
import inspect

test_files = glob.glob(os.path.dirname(__file__)+"/*.py")
test_mappings = { }
for x in sorted([os.path.basename(f)[:-3] for f in test_files if not "__" in f]):
    try:
        exec("import %s as test_file" % x)
        test_mappings[test_file] = []
        for obj in dir(test_file):
            ref = getattr(test_file, obj)
            if inspect.isclass(ref) and issubclass(ref, unittest2.TestCase):
                test_mappings[test_file].append(ref)
                exec("from %s import %s" % (x, obj))
    except Exception as e:
        print(e)
        print("Warning: could not import from file %s." % x)

def init(config):
    try:
        for test_file, tests in test_mappings.iteritems():
            for test in tests:
                #print('checking %s in %s' % (test, test_file))
                if hasattr(test, "parse"):
                    #print("calling parse on %s" % test)
                    new_tests = test.parse(config) or []
                    for new_test in new_tests:
                        globals()[new_test] = getattr(test_file, new_test)
    except:
        print("Failed to run all tests parse function!")
        pass
