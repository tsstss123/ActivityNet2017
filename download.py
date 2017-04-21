import json, os, sys
import pickle
from pprint import pprint
import threading
from multiprocessing.dummy import Pool as ThreadPool
from pytube import YouTube

done_video = set()
NUM_THREAD = 4

def get_video():
    global done_video
    try:
        os.mkdir('dataset')
    except:
        pass
    with open('activity_net.v1-3.min.json', 'r') as f:
        data = json.load(f)
    alltasks = []
    for x in data['database'].items():
        alltasks.append((x[0], x[1]['url']))
    
    num_tasks = len(alltasks)

    if os.path.exists('done_video.txt'):
        with open('done_video.txt', 'r') as done_file:
            for line in done_file.readlines():
                done_video.add(line.strip())
                print(line.strip() + ' has been download')
    
    num_done = 0
    tasks = []
    for x in alltasks:
        if x[0] in done_video:
            num_done += 1 
        else:
            tasks.append(x)
    print(str(num_done) + '/' + str(num_tasks))

    # multithreading

    lock = threading.Lock()
    def worker(i):
        x = tasks.pop(0)
        if x[0] in done_video:
            print(x[0] + ' has been download')
            return
        if os.path.exists('./dataset/' + x[0] + '.mp4'):
            os.remove('./dataset/' + x[0] + '.mp4')
        try:
            download_video(x[0], x[1])
            lock.acquire()
            try:
                with open('done_video.txt', 'a') as done_file:
                    done_file.write(x[0] + '\n')
            finally:
                lock.release()
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            sys.exit(0)
        finally:
            return
            
    try:
        from multiprocessing.pool import ThreadPool
        multi_available = True
    except ImportError:
        print('multiprocessing not available, fall back to single threaded encoding')
        multi_available = False

    if multi_available and NUM_THREAD > 0:
        p = ThreadPool(NUM_THREAD)
        p.map(worker, [i for i in range(len(tasks))])
    else:
        for _ in range(len(tasks)):
            worker(_)

def download_video(name, url):
    print(name, url)
    yt = YouTube(url)
    yt.set_filename(name)
    video = yt.filter('mp4')[-1]
    video.download('./dataset/')

if __name__ == '__main__':
    get_video()