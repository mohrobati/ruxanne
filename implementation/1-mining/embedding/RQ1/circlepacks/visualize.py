from pydriller import Repository
from dictdiffer import diff
from parser.tools import *
from embedding.tools import *
from parser.ddiff import DDiff
from visualization.circle_pack import CirclePack


samples_file = open("./samples_for_vis.txt")

for line in samples_file:
    parts = line.split(" ")
    target_repo = parts[0]
    target_commit = parts[1]
    target_file = parts[2]
    target_scope = parts[3].replace("\n", "")

    circlePack = CirclePack()

    repo = Repository('https://github.com/'+target_repo,
                        only_modifications_with_file_types=['.rs'],
                        num_workers=1, single=target_commit)
    for commit in repo.traverse_commits():
        for mod in commit.modified_files:
            if mod.filename == target_file:
                print(mod.filename)
                try:
                    before_parsedTree = convert_code_to_dict(
                        mod.source_code_before)
                    new_parsedTree = convert_code_to_dict(mod.source_code)
                    ddiff = DDiff(before_parsedTree,
                                    new_parsedTree).get_ddiff(target_scope)
                    circlePack.visualize(ddiff, target_repo, target_commit, target_file)
                except:
                    pass

