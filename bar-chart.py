import numpy as np
import matplotlib.pyplot as plt
import sys, json

def show_diagram(labels, values):
    x_pos = np.arange(len(labels))
    # prepare barchart
    plt.bar(x_pos, values, align='center', alpha=0.5)
    plt.xticks(x_pos, labels, rotation=90)
    plt.ylabel('Count of Jobs')
    plt.title('Technology Used')
    # show barchart
    plt.show()

def getSummary(raw_data, data_filter = {}):
    summary = {}
    for job in raw_data:
        tags = job['tag']
        for tag in tags:
            if not (tag in summary):
                summary[tag] = 1
            else:
                summary[tag] += 1
    return summary

def get_label_and_value(summary, threshold):
    labels = []
    values = []
    for tag in summary:
        value = summary[tag]
        if value > threshold:
            labels.append(tag)
            values.append(value)
    return (labels, values)

if __name__ == '__main__':
    file_name = sys.argv[1]
    threshold = int(sys.argv[2]) if len(sys.argv)>2 else 0
    json_file = open(file_name, 'r')
    raw_data = json.loads(json_file.read())
    summary = getSummary(raw_data)
    labels, values = get_label_and_value(summary, threshold)
    show_diagram(labels, values)
