#!/usr/bin/env python

import nitrate, qe
import xmlrpclib
import random
import optparse
from os import system

TAGS = {0:"Apps", 1:"Tier 1", 2:"new", 3:"Tier 2", 4:"TIP"}

def addbug(id):
    return [id, random.randint(1,10000), 1, "Summary", "Description"]

if __name__ == "__main__":
    parser = optparse.OptionParser(
            usage = "./init_tcms [--plans #] [--runs #] [--cases #]")
    parser.add_option("--plans",
            dest = "plans",
            type = "int",
            action = "store",
            default = 1,
            help = "create specified number of plans")
    parser.add_option("--runs",
            dest = "runs",
            type = "int",
            action = "store",
            default = 1,
            help = "create specified number of runs")
    parser.add_option("--cases",
            dest = "cases",
            type = "int",
            action = "store",
            default = 1,
            help = "create specified number of cases")
    (options, arguments) = parser.parse_args()

    # Create master plan (root)
    master = nitrate.TestPlan(name="Master Test Plan 2", \
        product="RHEL Tests", version="unspecified", \
        type=nitrate.PlanType(26))
    master.update()

    for i in range(0, options.plans):
        # Create Plans
        tplan = nitrate.TestPlan(name="Test Plan {0}".format(i+1),\
            parent=master.id, product="RHEL Tests", version="unspecified",\
            type=nitrate.PlanType(26))
        tplan.update()
        for c in range(0, options.cases):
            # Create cases
            case = nitrate.TestCase(name="Test Case {0}".format(i+1),\
                    category=nitrate.Category(702), product="RHEL Tests",\
                    summary="Test Case {0}".format(i+1),\
                    status=nitrate.CaseStatus(2))
            case.update()
            # Link with TestPlan
            nitrate.TestCase(case.id).testplans._add([nitrate.TestPlan(tplan.id)])
            # Add a tag
            nitrate.TestCase(case.id).tags._add([TAGS[random.randint(0,4)]])
            # Add bug
            nitrate.TestCase(case.id).bugs.add(nitrate.Bug(1000))
        for r in range(0, options.runs):
            # Create runs
            run = nitrate.TestRun(name="Test Run {0}".format(i+1),\
                    testplan=nitrate.TestPlan(tplan.id), build=nitrate.Build(979),\
                    product="RHEL Tests", summary="Test Run",\
                    version=nitrate.Version(389).name)
