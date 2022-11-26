import numpy as np
import matplotlib
import matplotlib.pyplot as plt
print('matplotlib: {}'.format(matplotlib.__version__))

indices = [[0, 0], [0, 1], [0, 2],
           [1, 0], [1, 1], [1, 2],
           [2, 0], [2, 1], [2, 2]]

labels1 = ['$G_{c}$', '$G_{n}$']
labels2 = ['$BC_{c}$', '$BC_{n}$']
BC_NUMBER = 27143
borrow_only_data = [(5, 0.01, 160, 18755), (5, 0.001, 102, 25909), (5, 0.0001, 61, 26711), (7, 0.01, 77, 19324), (7, 0.001, 47, 26212), (7, 0.0001, 23, 26910), (9, 0.01, 51, 19642), (9, 0.001, 26, 26381), (9, 0.0001, 11, 27001)] 

TOTAL_NUMBER = 60583
total_data = [(5, 0.01, 331, 19902), (5, 0.001, 556, 40944), (5, 0.0001, 577, 50441), (7, 0.01, 182, 20931), (7, 0.001, 312, 42379), (7, 0.0001, 330, 51852), (9, 0.01, 128, 21535), (9, 0.001, 226, 43189), (9, 0.0001, 226, 52705)] 

fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(12, 8))

cols = ['$\epsilon =${}\n'.format(col) for col in ['0.01', '0.001', '0.0001']]
rows = ['Z = {}\n'.format(row) for row in [5, 7, 9]]

for axis, col in zip(ax[0], cols):
    axis.set_title(col)

for axis, row in zip(ax[:,0], rows):
    axis.set_ylabel(row, rotation=90, size='large')

for index in indices:
    print(index)
    x = np.arange(len(labels1))
    data_index = 3*index[0] + index[1]
    width = 0.5
    rects1 = ax[index[0], index[1]].bar(labels1, [TOTAL_NUMBER - total_data[data_index][3], total_data[data_index][3]], width, label="$C_{g}$="+ str(total_data[data_index][2]))
    rects2 = ax[index[0], index[1]].bar(labels2, [BC_NUMBER - borrow_only_data[data_index][3],borrow_only_data[data_index][3]], width, label="$C_{b}$="+ str(borrow_only_data[data_index][2]))
    ax[index[0], index[1]].legend(loc='upper right')
    ax[index[0], index[1]].bar_label(rects1, padding=5)
    ax[index[0], index[1]].bar_label(rects2, padding=5)
    ax[index[0], index[1]].axis(ymax=60000)
    ax[index[0], index[1]].set_yticks([])


fig.tight_layout()
plt.savefig('plt.svg')