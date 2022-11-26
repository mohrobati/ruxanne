import csv, sys, json

nonTerminals = json.load(open('./nonTerminals.json'))
freq_true = json.load(open('./freq.json'))

for nonTerminal in nonTerminals:
    if nonTerminal not in freq_true:
        freq_true[nonTerminal] = 1
    else:
        freq_true[nonTerminal] = 1 / freq_true[nonTerminal]

output_file = open("./weight_adjustments.json", "w+")
output_file.write(json.dumps(freq_true))




