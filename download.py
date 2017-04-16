import json, os
import pickle
from pprint import pprint
from multiprocessing.dummy import Pool as ThreadPool
from pytube import YouTube

done_video = set()

def get_video():
    global done_video
    try:
        os.mkdir('dataset')
    except:
        pass
    with open('activity_net.v1-3.min.json', 'r') as f:
        data = json.load(f)
    tasks = []
    for x in data['database'].items():
        tasks.append((x[0], x[1]['url']))
    # pool = ThreadPool(4)
    # pool.starmap(download_video, tasks)
    # pool.close()
    if os.path.exists('done_video.txt'):
        with open('done_video.txt', 'r') as done_file:
            for line in done_file.readlines():
                done_video.add(line.strip())
                print(line.strip() + ' has been download')

    for x in tasks:
        if x[0] in done_video:
            print(x[0] + ' has been download')
            continue
        if os.path.exists('./dataset/' + x[0] + '.mp4'):
            os.remove('./dataset/' + x[0] + '.mp4')
        download_video(x[0], x[1])
        with open('done_video.txt', 'a') as done_file:
            done_file.write(x[0] + '\n')

def download_video(name, url):
    print(name, url)
    yt = YouTube(url)
    yt.set_filename(name)
    video = yt.filter('mp4')[-1]
    video.download('./dataset/')

if __name__ == '__main__':
    get_video()