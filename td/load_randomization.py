import os

from unipath import Path

from td_list.models import RandomizationItem


def load_randomization():

    f = open(os.path.join(
             Path(os.path.dirname(os.path.realpath(__file__))).ancestor(2).child('etc'), 'randomization.csv'))
    for index, line in enumerate(f.readlines()):
        if index == 0:
            continue
        seq, drug_assignment = line.split(',')
        RandomizationItem.objects.get_or_create(name=seq, field_name=drug_assignment)
