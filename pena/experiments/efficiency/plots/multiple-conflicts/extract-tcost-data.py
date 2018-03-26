#!/usr/bin/env python3
import re

import datetime

def is_day_passed(t_init, t_finish):
    return ('PM' in t_init and 'AM' in t_finish)

TIME_FORMAT = "%I:%M:%S %p"

def extract_from(input_file, name):
    with open(input_file) as pwlog:
        entries = []
        for line in pwlog:
            if "Run Started" in line \
                    or "Run Finished" in line \
                    or "CONFLICTS" in line:
                entries.append(line.strip())

        results = []
        for i in range(0, len(entries), 3):
            t_init = re.sub(":INFO.*", "", entries[i + 1])
            t_finish = re.sub(":INFO.*", "", entries[i + 2])
            print('started:', entries[i + 1], 'finished:', entries[i + 2])

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

            n_str = re.sub(".*CONFLICTS C=", "", entries[i])
            
            results.append("{},{},{}".format(int(delta.total_seconds()), n_str, name))

        return results


with open("tcost.csv", "w") as f:
    # [f.write("{}\n".format(line)) for line in extract_from("../data/multiple/SS-multiple.log", "SS")]
    # [f.write("{}\n".format(line)) for line in extract_from("../data/multiple/PW-multiple.log", "PW")]
    [f.write("{}\n".format(line)) for line in extract_from("../data/multiple/PW-2.log", "PW")]

