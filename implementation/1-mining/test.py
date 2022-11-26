from pydriller import Repository
import csv, json
from parser.tools import *
from embedding.tools import *
from parser.ddiff import DDiff
from circle_pack import CirclePack
from pathlib import Path

Path("./__logs__/").mkdir(exist_ok=True)
before_file = open("./__logs__/before.txt", "w+")
diff_file = open("./__logs__/diff.txt", "w+")
after_file = open("./__logs__/after.txt", "w+")
output_file = open("./datapoints.csv", "w+")
write = csv.writer(output_file)
write.writerows([["proj", "commit", "file", "scope"] + NONTERMINALS])
buggyKeywords = ["bug", "fix", "wrong", "error", "issue", "fault", "fail", "crash", "defect"]
proj = "alacritty/alacritty"
circle_pack = CirclePack()
repo = Repository('https://github.com/'+proj,
                        only_modifications_with_file_types=['.rs'],
                        num_workers=1, order="reverse"
                        , single="90552e3e7f8f085919a39435a8a68b3a2f633e54")
for commit in repo.traverse_commits():
    print("Mining...")
    if any(word in commit.msg for word in buggyKeywords):
        for mod in commit.modified_files:
            if mod.filename.endswith(".rs") and mod.source_code_before and mod.source_code:
                try:
                    before_parsedTree = convert_code_to_dict(mod.source_code_before)
                    before_file.write(json.dumps(before_parsedTree))
                    new_parsedTree = convert_code_to_dict(mod.source_code)
                    after_file.write(json.dumps(new_parsedTree))
                    ddiff = DDiff(before_parsedTree, new_parsedTree).get_ddiff()
                    diff_file.write(json.dumps(ddiff))
                    for essence in get_essences(ddiff):
                        check = is_borrow_checker_related(essence, mod.diff)
                        print("https://github.com/"+proj +
                                "/commit/"+commit.hash, mod.filename, essence[0])
                        datapoint_list = get_datapoint(essence[1])[1]
                        if check[0]: 
                            print("BC-related keywords:", "-".join(list(check[1])))
                            datapoint_list.insert(0, "-".join(list(check[1])))
                        else:
                            datapoint_list.insert(0, 'None')
                        datapoint_list.insert(0, essence[0])
                        datapoint_list.insert(0, mod.filename)
                        datapoint_list.insert(0, commit.hash)
                        datapoint_list.insert(
                            0, proj.replace("\n", ""))
                        write.writerows([datapoint_list])
                        circle_pack.visualize(ddiff, proj, commit.hash, mod.filename)
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
        print('\033[92m' + "--{}/commit/{} mined successfully--".format(proj, commit.hash) + '\033[0m')
        print("======\n")
print('\n\033[94m' + "Mining Finished!" + '\033[0m\n\n')
before_file.close()
diff_file.close()
after_file.close()
output_file.close()
