import json
from collections import defaultdict

BORROW_CHECKER_TOKENS = json.load(open("./scheme/borrow_checker.json", "r"))
WEIGHTS = json.load(open('./scheme/weight_adjustments.json'))
NONTERMINALS = sorted(list(WEIGHTS.keys()))

def get_essences(ddiff):
    essences = []
    for diff in ddiff:
        essence_dict = defaultdict(int)
        for change in diff[1]:
            for nonTerminal in change.split("-"):
                if nonTerminal in WEIGHTS:
                    essence_dict[nonTerminal] += WEIGHTS[nonTerminal]
        essences.append((diff[0], essence_dict))
    return json.loads(json.dumps(essences))


def get_datapoint(essence):
    datapoint = {}
    datapoint_list = []
    for nonTerminal in NONTERMINALS:
        datapoint[nonTerminal] = 0.0 if nonTerminal not in essence else essence[nonTerminal]
        datapoint_list += [0.0] if nonTerminal not in essence else [essence[nonTerminal]]
    return datapoint, datapoint_list
