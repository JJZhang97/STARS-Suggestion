#Load mods time schedule and store it.
def load_courses():
    #possible to have more than 1 timeslot for a single class, eg Comm fund 2
    return {"AC1101":[["1-tue-0830-1030","1-wed-1530-1730"],["2-wed-0830-1030","2-thu-1530-1730"],["3-thu-0830-1030","3-mon-1430-1630"]],
            "BC1101":[["1-thu-1430-1830"],["2-fri-0830-1230"],["3-mon-0830-1230"]]}


