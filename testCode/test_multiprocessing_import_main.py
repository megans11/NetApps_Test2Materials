# multiprocessing_import_main.py

import multiprocessing
import multiprocessing_import_worker
from random import randint
import pickle

if __name__ == '__main__':
   jobs = []
   for i in range(5):
      ints = (i*1,i*2,i*3,i*4)
      payload = (i,ints)
      p = multiprocessing.Process(target=multiprocessing_import_worker.worker,args=(pickle.dumps(payload),))
      jobs.append(p)
      p.start()