
import numpy as np

def removeOutliers(rats):
    values = []
    result = []
    to_correct = 0
    for tpl in rats:
        values.append(tpl[0])
    data = np.array(values)
    mean = np.mean(data, axis=0)
    sd = np.std(data, axis=0)
    for i in range(0, len(rats)):
        if (mean - (rats[i][0] + to_correct) > 5 * sd or (rats[i][0] < 3)):
            # print('filtering out: ', rats[i][0])
            to_correct += rats[i][0]
        else:
            to_append = (rats[i][0] + to_correct, rats[i][1])
            to_correct = 0
            result.append(to_append)

    return result