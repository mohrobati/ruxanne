from pydriller import Repository
import csv
from embedding.tools import *
from parser.tools import *
from parser.ddiff import DDiff


output_file = open("./datapoints.csv", "w+")
write = csv.writer(output_file)
write.writerows([["proj", "commit", "file", "scope", "desc"] + NONTERMINALS])
buggyKeywords = ["bug", "fix", "wrong", "error", "issue", "fault", "fail", "crash", "defect"]

for proj in open("./projects.txt", "r"):
    proj = proj.replace("\n", "")
    repo = Repository('https://github.com/'+proj,
                      only_modifications_with_file_types=['.rs'],
                      num_workers=1, order="reverse")
    for commit in repo.traverse_commits():
        if any(word in commit.msg for word in buggyKeywords):
            for mod in commit.modified_files:
                if mod.filename.endswith(".rs") and mod.source_code_before and mod.source_code:
                    try:
                        before_parsedTree = convert_code_to_dict(
                            mod.source_code_before)
                        new_parsedTree = convert_code_to_dict(mod.source_code)
                        ddiff = DDiff(before_parsedTree,
                                      new_parsedTree).get_ddiff()
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
                    except Exception as ex:
                        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
            print('\033[92m' + "--{}/commit/{} mined successfully--".format(proj, commit.hash) + '\033[0m')
            print("======\n")
print('\n\033[94m' + "Mining Finished!" + '\033[0m\n\n')
output_file.close()
