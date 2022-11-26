import os, glob

projs = list(map(lambda x: x.replace("\n",""), open("../projects.txt", "r").readlines()))
for proj in projs:
    name = proj.split("/")[1]
    os.system("git clone https://github.com/"+proj+".git")
    os.chdir('./'+name)
    os.system("find . -name '*.rs' | xargs wc -l | tail -n 1 >> ../counts.txt")
    os.chdir('..')
