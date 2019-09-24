import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import os
from src.utils.dirs import *
from src.utils.parse import *
from matplotlib import dates
import datetime
from matplotlib.dates import HourLocator, MinuteLocator
from matplotlib.dates import DateFormatter


def makeRATDistributionForDevice(device, filename):
    def reject_outliers(data, m=2.):
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d / mdev if mdev else 0.
        return data[s < m]

    device_to_rat = parseDataSet(filename)
    sampling_rates = parseSamplingRates()
    key = device
    # print('self.sampling_rates', self.sampling_rates)
    sampling_rate = sampling_rates[key]
    path = (os.path.join(os.getcwd(), 'Distributions'))
    save_to = os.path.join(path, key.replace('/', '_'))
    createFolder(save_to)
    rats = device_to_rat[key]
    rats = list(map(lambda x: float(x[0]), rats))
    # comment out to reject outliers
    # rats = reject_outliers(np.array(rats))

    weights = np.ones_like(rats) / float(len(rats))
    n, bins, patches = plt.hist(x=rats, bins=20, color='#0504aa',
                                rwidth=0.7, weights=weights)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Relative Arrival Time (s)')
    plt.ylabel('Frequency')
    # plt.gca().yaxis.set_major_formatter(formatter)
    std = round(np.std(np.array(rats)), 2)
    mean = round(np.mean(np.array(rats)), 2)
    min = np.min(np.array(rats))
    max = np.max(np.array(rats))
    sample_size = len(rats)
    # print('std:', std)
    # print('mean:', mean)
    # print('min:', min)
    # print('max:', max)
    # plt.text(23, 45, r'$\mu=15, b=3$')
    #textstr = 'mean=' + to_str(mean) + ', ' + '\n' + 'std=' + self.to_str(std) + ', \n' + 'min=' + self.to_str(
    #    min) + ', \n' + 'max=' + to_str(max) + ', \n' + 'count=' + str(sample_size)
    #plt.text(0.8, 0.885, textstr, fontsize=8, transform=plt.gcf().transFigure)
    plt.title(device + ' SR=' + str(sampling_rate) + ')')
    maxfreq = n.max()
    # plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    # plt.ylim(ymax=105)
    plt.savefig(os.path.join(save_to, 'plot.png'))
    plt.close()


 # creates distribution of relative arrival times for each device
    def makeRATDistribution(filename):
        print('Plotting distributions...')
        def reject_outliers(data, m=5.):
            d = np.abs(data - np.median(data))
            mdev = np.median(d)
            s = d / mdev if mdev else 0.
            return data[s < m]

        device_to_rat = parseDataSet(filename)
        parsed_data_set = True
        sampling_rates = parseSamplingRates()
        for i in tqdm(range(len(list(device_to_rat.keys())))):
            key = list(device_to_rat.keys())[i]
            #print('self.sampling_rates', self.sampling_rates)
            sampling_rate = sampling_rates[key]
            path = (os.path.join(os.getcwd(), 'Distributions'))
            save_to = os.path.join(path, key.replace('/', '_'))
            createFolder(save_to)
            rats = device_to_rat[key]
            rats = list(map(lambda x: float(x[0]), rats))
            # comment out to reject outliers
            rats = reject_outliers(np.array(rats))

            weights = np.ones_like(rats) / float(len(rats))
            n, bins, patches = plt.hist(x=rats, bins=20, color='#0504aa',
                                    rwidth=0.7, weights=weights)
            plt.grid(axis='y', alpha=0.75)
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            #plt.gca().yaxis.set_major_formatter(formatter)
            std = round(np.std(np.array(rats)),2)
            mean = round(np.mean(np.array(rats)), 2)
            min = np.min(np.array(rats))
            max = np.max(np.array(rats))
            sample_size = len(rats)
            textstr = 'mean=' + to_str(mean) +', ' + '\n' + 'std=' + to_str(std) + ', \n' + 'min=' + to_str(min) + ', \n' + 'max=' + to_str(max) + ', \n' + 'count=' + str(sample_size)
            plt.text(0.8, 0.885, textstr, fontsize=8, transform=plt.gcf().transFigure)
            plt.title('Relative Arrival Time (SR=' + str(sampling_rate) + ')')
            maxfreq = n.max()
            #plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
            #plt.ylim(ymax=105)
            plt.savefig(os.path.join(save_to, 'distribution.png'))
            plt.close()


def parseDataPlot(lst):
    return (get_x(lst), get_y(lst))


def get_x(tup):
    result = list(map(lambda x: x[1], tup))
    return dates.date2num(list(map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f"), result)))

def get_y(tup):
    return list(map(lambda x: float(x[0]), tup))


def makeTimePlot(predictions, rats, names):
    fig, ax = plt.subplots()
    counter = 0
    while counter < len(predictions):
        x = []
        y = []
        for tup in predictions[counter]:
            y.append(tup[0])
            x.append(tup[1])
        print('x pred', x)
        x = dates.date2num(list(map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f"), x)))
        ax.plot(x, y, label = names[counter])
        counter +=1
    x = []
    y = []
    for tup in rats:
        y.append(tup[0])
        x.append(tup[1])
    print('x at', x)
    x = dates.date2num(list(map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f"), x)))
    ax.plot(x, y, label='Arrival Time')
    #plt.legend()
    ax.xaxis.set_major_locator(HourLocator(interval=4))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%dT%H:%M'))
    fig.autofmt_xdate()
    plt.show()


