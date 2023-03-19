import re
import sys
import json
from itertools import zip_longest


def split_course_line(course):
    # need to match "ECSE 4490/6490)" but not "Fall 2021)"
    # so we use this horrifying backwards regex
    a = re.search(r"\)[0-9x][0-9][0-9][0-9](/[0-9x][0-9][0-9][0-9])? [A-Z]",course[::-1])
    if a:
        i = -a.start()
    else:
        a = re.search(r"[0-9x] ",course)
        i = a.start()+1

    return {"code":course[:i].strip(),"title":course[i:].strip()}


def main(filename):
    with open(filename) as file:
        lines = [
            line.strip()
            for line in file.readlines()
            # remove "Last updated: 2/22/2023"
            if line.strip() and not line.strip().startswith("Last updated:")
        ]

        concentration_indices = [
            i for i, line in enumerate(lines) if "Concentration Area:" in line
        ]

        areas = [
            lines[prev:next]
            for prev, next in zip_longest(
                concentration_indices, concentration_indices[1:]
            )
        ]
        
        areas = {
            area[0][area[0].index(":")+2:] : [
                split_course_line(course)
                for course in area[1:]
            ] for area in areas
        }

        json.dump(areas, sys.stdout, indent=2)


if __name__ == "__main__":
    main(sys.argv[-1])
