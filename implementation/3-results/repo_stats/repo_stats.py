from pydriller.metrics.process.lines_count import LinesCount
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller import Repository
from datetime import datetime

def get_edited_files_count(added, removed):
    editted = {}
    for a_key in added:
        if a_key in removed:
            editted[a_key] = added[a_key] - removed[a_key]
    return sum(editted.values())

def get_avg_churn(avgs):
    sum = 0
    for key in avgs:
        if key and ".rs" in key:
            sum += avgs[key]
    return sum / len(avgs)

for proj in open("./projects.txt", "r"):
    proj = proj.replace("\n", "")
    print("in proj", proj)
    churn = CodeChurn(path_to_repo='https://github.com/'+proj,
                    since=datetime(2000, 1, 1),
                    to=datetime(2025, 12, 31))
    print("churn computed", churn.avg())
    avg_churn = get_avg_churn(churn.avg())
    print(proj)
    print('Churn: {}'.format(avg_churn))
    print("=========\n")
