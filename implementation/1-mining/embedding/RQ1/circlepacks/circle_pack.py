from pydriller import Repository
from dictdiffer import diff
import csv, math, json, sys, os
from parser.tools import *
from embedding.tools import *
from parser.ddiff import DDiff
from collections import defaultdict
import packcircles as pc
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap


class CirclePack:

    def __init__(self):
        self.weights = json.load(open('./scheme/weight_adjustments.json'))
        self.basePath = 'visualization/'

    def __make_dir(self, proj, commit):
        path = self.basePath + proj.replace("/", "_") + "/" + commit
        try:
            os.makedirs(path)
        except:
            pass
        return path + "/"

    def __circle_pack_plot_save(self, essence, path, filename):
        labels = list(essence[1].keys())
        radii = np.array(list(essence[1].values()))
        radii = list(((radii / min(radii)) * 3).astype(int))
        for i in range(len(radii)):
            radii[i] = int(math.log(radii[i]))
        if len(radii) < 3:
            return
        fig, ax = plt.subplots()
        cmap = get_cmap('coolwarm_r')
        circles = pc.pack(radii)
        lims = [-math.inf, -math.inf, math.inf, math.inf]
        for idx, (x, y, radius) in enumerate(circles):
            lims = [max(lims[0], y+radius), max(lims[1], x+radius),
                    min(lims[2], y-radius), min(lims[3], x-radius)]
            patch = plt.Circle(
                (x, y),
                radius,
                color=cmap(radius/max(radii)),
                alpha=0.65
            )
            fsize = math.sqrt(radius/max(radii))*16
            if len(labels[idx]) > int(fsize)-1:
                ax.annotate(labels[idx][:int(fsize)-1]+"...", xy=(x-radius/2, y),
                        fontsize=fsize)
            else:
                ax.annotate(labels[idx], xy=(x-radius/2, y),
                        fontsize=fsize)
            ax.add_patch(patch)
        fig.set_figheight(5)
        fig.set_figwidth(7)
        ax.set(xlim=(lims[3], lims[1]), ylim=(lims[2], lims[0]))
        plt.axis('off')
        plt.savefig(path + filename + "_" + essence[0]+".png")

    def visualize(self, ddiff, proj, commit, filename):
        essences = get_essences(ddiff)
        path = self.__make_dir(proj, commit)
        for essence in essences:
            self.__circle_pack_plot_save(essence, path, filename)


