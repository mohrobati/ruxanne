from .syn_compiler.lexer import Lexer
from .syn_compiler.parser import Parser
from dictdiffer import diff
import json, os
from collections import defaultdict
from pathlib import Path

BORROW_CHECKER_TOKENS = json.load(open("./scheme/borrow_checker.json", "r"))
WEIGHTS = json.load(open('./scheme/weight_adjustments.json'))
NONTERMINALS = sorted(list(WEIGHTS.keys()))

def convert_code_to_dict(code=None):
    path = os.path.abspath(os.getcwd())
    if code:
        f_code = open(path + "/parser/rust-parser/src/program.rs", "w+")
        f_code.write(code)
        f_code.close()
    os.chdir(path + "/parser/rust-parser")
    Path(path + "/__logs__/").mkdir(exist_ok=True)
    _ = os.system("cargo run --quiet --release ./src/program.rs")
    os.chdir(path)
    f_syn = open(path + "/__logs__/parsed.syn", "r")
    f_json = open(path + "/__logs__/parsed.json", "w+")
    tree = f_syn.read()
    lexer = Lexer().build()
    lexer.input(tree)
    parser = Parser()
    parser.build().parse(tree, lexer, False)
    f_json.write(parser.dictTree_string)
    f_syn.close()
    f_json.close()
    return parser.dictTree


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


def is_borrow_checker_related(essence, diff):
    seen_tokens = []
    seen_lexemes = set()
    for token in BORROW_CHECKER_TOKENS.keys():
        if token in essence[1]:
            seen_tokens.append(token)
    for token in seen_tokens:
        for line in list(filter(lambda x: x.startswith(('+', '-')), diff.split("\n"))): 
            if BORROW_CHECKER_TOKENS[token] in line:
                seen_lexemes.add(BORROW_CHECKER_TOKENS[token])
    return len(seen_lexemes) > 0, seen_lexemes
