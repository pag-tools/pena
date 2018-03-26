#!/usr/bin/env python3
import re

import datetime

TIME_FORMAT = "%I:%M:%S %p"

PATTERNS = [
    "Run Started",
    "dimensionality reduction started",
    "dimensionality reduction finished",
    "fetching pages started",
    "fetching pages finished",
    "Started search",
    "Finished search"
    "Cleansing start",
    "Cleansing finished",
    "Checking visual conflicts started",
    "Checking visual conflicts finished",
    "Run Finished",
]

def is_day_passed(t_init, t_finish):
    return ('PM' in t_init and 'AM' in t_finish)

def list_to_chunks(lista, chunks=3):
    res = []
    for i in range(0, len(lista), chunks):
        chunk = lista[i:i+chunks]
        res.append(chunk)
    return res


def extract_from(input_file, name):
    with open(input_file) as pwlog:
        entries = []
        for line in pwlog:
            if [p for p in PATTERNS if p in line]:
                entries.append(line.strip())

        entries = list_to_chunks(entries, chunks=3)
        results = []

        print(entries[0])
        raise Exception('0')

        for i in range(0, len(entries), 3):
            t_init = re.sub(":INFO.*", "", entries[i])
            t_finish = re.sub(":INFO.*", "", entries[i + 2])

            t_regex = re.compile('.+\s(AM|PM)', re.IGNORECASE)
            t_init = re.search(t_regex, t_init).group()
            t_finish = re.search(t_regex, t_finish).group()

            # need to convert to plus one day if pass a day
            if is_day_passed(t_init, t_finish):
                t_finish = datetime.datetime.strptime(t_finish, TIME_FORMAT) + datetime.timedelta(days=1)
            else:
                t_finish = datetime.datetime.strptime(t_finish, TIME_FORMAT)

            t_init = datetime.datetime.strptime(t_init, TIME_FORMAT)

            delta = abs(t_finish - t_init)
            N_str = re.sub(", .*", "", re.sub(".*Input: ", "", entries[i + 1]))
            results.append("{},{},{}".format(int(delta.total_seconds()), N_str, name))

        return results


with open("tcost_steps.csv", "w") as f:
    [f.write("{}\n".format(line)) for line in extract_from("../data/single/TESTE-100.log", "PW")]
    # [f.write("{}\n".format(line)) for line in extract_from("../data/single/PW-single.log", "PW")]
    # [f.write("{}\n".format(line)) for line in extract_from("../data/single/SS-single.log", "SS")]