#!/usr/bin/env python3
#
#
# Copyright (C) 2015  Glen Pitt-Pladdy
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#
# See: https://www.pitt-pladdy.com/blog/_20150707-214047_0100_Bayesian_Classifier_Classes_for_Python/
# Previously: https://www.pitt-pladdy.com/blog/_20111229-214727_0000_Bayesian_Classifier_Classes_for_Perl_and_PHP/
#

from __future__ import print_function
import sys
import os
import re
import sqlite3
import classifier


# load & apply stoplist if available
def stopwordlist(classifier):
    stopwordpath = os.path.join(os.path.dirname(sys.argv[0]), 'stopwords.txt')
    with open(stopwordpath, 'rt') as f_stopowrds:
        stopwords = [w.strip() for w in f_stopowrds]
        classifier.removestopwords(stopwords)


if len(sys.argv) >= 5 and sys.argv[2] == 'classify' and sys.argv[3].isdigit() and sys.argv[4].isdigit():
    db = sqlite3.connect(sys.argv[1])
    classifier = classifier.Classifier(db, sys.stdin.read())
    stopwordlist(classifier)
    classifier.unbiased = True
    clases = [int(x) for x in sys.argv[3:]]
    prob = classifier.classify(clases)
    for clas in clases:
        print("class{:d}: {:f}".format(clas, prob[clas]))
elif len(sys.argv) >= 4 and len(sys.argv) <= 5 and sys.argv[2] == 'teach' and sys.argv[3].isdigit():
    db = sqlite3.connect(sys.argv[1])
    classifier = classifier.Classifier(db, sys.stdin.read())
    stopwordlist(classifier)
    if len(sys.argv) >= 4:
        classifier.teach(int(sys.argv[3]))
    else:
        classifier.teach(int(sys.argv[3]), float(sys.argv[4]))
elif len(sys.argv) == 3 and sys.argv[2] == 'updatequality':
    db = sqlite3.connect(sys.argv[1])
    classifier = classifier.Classifier(db, '')
    classifier.unbiased = True
    classifier.updatequality()
elif len(sys.argv) == 4 and sys.argv[2] == 'degrade' and re.match(r'^\d+(\.\d+)?$', sys.argv[3]):
    db = sqlite3.connect(sys.argv[1])
    classifier = classifier.Classifier(db, '')
    classifier.degrade(sys.argv[3])
elif len(sys.argv) == 4 and sys.argv[2] == 'cleanfrequency' and re.match(r'^\d+(\.\d+)?$', sys.argv[3]):
    db = sqlite3.connect(sys.argv[1])
    classifier = classifier.Classifier(db, '')
    classifier.cleanfrequency(sys.argv[3])
else:
    sys.exit("Usage: %s <sqlite file> [teach <clasid> [weighting]|clasify <clasid> <clasid> [clasid] [...]|updatequality|degrade <factor>|cleanfrequency <threshold>]\n\ttext on STDIN\n\tIf \"stopwords.txt\" (one per line) exists it will be used\n" % sys.argv[0])


