import sys
import csv
from collections import Counter

from fingerprints.cleanup import clean_name_light
from fingerprints.types import remove_types


def main(file_name):
    counter = Counter()
    with open(file_name, "r") as fh:
        for idx, row in enumerate(csv.DictReader(fh)):
            if idx % 100_000 == 0:
                print(idx)
            if row["prop_type"] != "name":
                continue
            schema = row["schema"]
            # if schema not in ("Organization", "Company"):
            if schema != "Person":
                continue
            value = row["value"]
            clean = clean_name_light(value)
            if clean is None:
                continue
            # clean = remove_types(clean)
            # if clean is None:
            #     continue
            tokens = clean.split(" ")
            for token in tokens:
                if len(token) > 2:
                    counter[token] += 1
            # print((value, clean))

            # if idx > 1_000_000:
            #     break

    for token, count in counter.most_common(1000):
        print((token, count))


if __name__ == "__main__":
    main(sys.argv[1])
