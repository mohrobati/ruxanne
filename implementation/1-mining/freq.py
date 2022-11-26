from pydriller import Repository
from dictdiffer import diff
from parser.tools import *
from embedding.tools import *
from parser.ddiff import DDiff
from collections import defaultdict


# Find the occurence frequency of each nonterminal
# over last 20 bug fixing commits of 18 most starred
# Github Rust projects

buggyKeywords = ["bug", "fix", "wrong", "error", "issue", "fault", "fail", "crash", "defect"]
freq_dict = defaultdict(int)

def iterate_commits(repo, proj):
    count, threshold = 0, 20
    for commit in repo.traverse_commits():
        if any(word in commit.msg for word in buggyKeywords):
            for mod in commit.modified_files:
                if mod.filename.endswith(".rs") and mod.source_code_before and mod.source_code:
                    try:
                        before_parsedTree = convert_code_to_dict(mod.source_code_before)
                        new_parsedTree = convert_code_to_dict(mod.source_code)
                        ddiff = DDiff(before_parsedTree, new_parsedTree).get_ddiff()
                        for scope in ddiff:
                            for diff in scope[1]:
                                for nonTerminal in diff.split("-"):
                                    if nonTerminal:
                                        freq_dict[nonTerminal] += 1
                        print(proj)
                        print(commit.hash)
                        print(mod.filename + "\n")
                        count+=1
                        if count == threshold:
                            return
                    except SystemExit:
                        break
                    except Exception as ex:
                        pass

for proj in open("./projects.txt", "r"):
    proj = proj.replace("\n", "")
    repo = Repository('https://github.com/'+proj,
                            only_modifications_with_file_types=['.rs'],
                            num_workers=1, order="reverse")
    iterate_commits(repo, proj)

print(freq_dict)