# multiprocessing_import_worker.py

import pickle

def worker(payload):
    """worker function"""
    answer_payload = pickle.loads(payload)
    sumPayload = 0
    for i in answer_payload[1]:
        sumPayload = sumPayload + i
        
    print('Worker', answer_payload[0], '----', sumPayload)
    return
