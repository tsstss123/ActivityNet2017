import json, os, sys
import pickle
from pprint import pprint

def analysis(dataset, output = None):
    '''分析数据集
    '''
    with open(dataset, 'r') as datafile:
        data = json.load(datafile)
    fout = open(output, 'w')
    video_cnt = 0
    labeled_video_cnt = 0
    segment_cnt = 0
    resolution_statistics = {}
    length_sum = 0.0
    labeled_length = 0.0
    dataset_version = data['version']
    for one in data['database'].items():
        item = one[1]
        video_cnt += 1
        if len(item['annotations']) > 0:
            labeled_video_cnt += 1
            segment_cnt += len(item['annotations'])
            for _ in item['annotations']:
                labeled_length += _['segment'][1] - _['segment'][0]
        if resolution_statistics.get(item['resolution']) is None:
            resolution_statistics[item['resolution']] = 1
        else:
            resolution_statistics[item['resolution']] += 1
        length_sum += item['duration']
    fout.write('DATASET : ' + dataset_version + '\n')
    fout.write('all ' + str(video_cnt) + ' videos, ' + str(labeled_video_cnt) + ' Videos labeled\n')
    fout.write(str(segment_cnt) + ' labeled segments\n')
    fout.write(str(int(length_sum / 3600)) + ' hours  ')
    fout.write(str(int(labeled_length / 3600)) + ' hours are labeled\n')
    for res, number in resolution_statistics.items():
        fout.write(res + ' : ' + str(number) + '\n')
    fout.close()


if __name__ == '__main__':
    analysis('activity_net.v1-3.min.json', 'output.txt')
