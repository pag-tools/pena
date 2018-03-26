#!/usr/bin/env python3
import re

import datetime

TIME_FORMAT = "%I:%M:%S %p"

def is_day_passed(t_init, t_finish):
    return ('PM' in t_init and 'AM' in t_finish)

class Entry:
    def __init__(self):
        self.conflict = None
        self.started = None
        self.finished = None
        self.iterative_runs = 0

def extract_from(input_file, name):
    with open(input_file) as pwlog:
        entries = []
        entry = None
        for line in pwlog:
            if "CONFLICT" in line:
                entry = Entry()
                entry.conflict = line.strip()
            elif "Run Started" in line:
                entry.started = line.strip()
            elif "Iterative run" in line:
                entry.iterative_runs += 1
            elif "Run Finished" in line:
                entry.finished = line.strip()
                entries.append(entry)

        results = []
        for entry in entries:
            t_init = re.sub(":INFO.*", "", entry.started)
            t_finish = re.sub(":INFO.*", "", entry.finished)

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
            n_str = re.sub(".*CONFLICTS C=", "", entry.conflict)
            results.append("{},{},{},{}".format(int(delta.total_seconds()), n_str, name, entry.iterative_runs))

        [print(p) for p in results]
        return results


with open("tcost-xxx.csv", "w") as f:
    [f.write("{}\n".format(line)) for line in extract_from("../data/multiple/SS-multiple.log", "SS")]

