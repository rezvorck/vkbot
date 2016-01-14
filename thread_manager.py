import threading
import time

    
class thread_manager:  # not thread-safe, should be used only from main thread
    def __init__(self):
        self.threads = {}
   
    def run(self, key, proc, pre_proc, instant_pre_proc, delay=0, pre_delay=0, pending_interval=0, pending_proc=None, min_delay=0):  # too many params
        if delay:
            if pending_proc:
                if min_delay <= delay + pre_delay:
                    instant_pre_proc()
                    pre_proc = lambda:None
                def _delay(proc, delay, pre_delay, pending_interval, pending_proc, min_delay):
                    def _f():
                        if min_delay > delay + pre_delay:
                            time.sleep(min_delay - delay - pre_delay)
                        pre_proc()
                        time.sleep(pre_delay)
                        st = time.time()
                        pending_proc()
                        while st + delay - time.time() > pending_interval:
                            time.sleep(pending_interval)
                            pending_proc()
                        time.sleep(max(st + delay - time.time(), 0))
                        proc()
                    return _f 
                proc = _delay(proc, delay, pre_delay, pending_interval, pending_proc, min_delay)
            else:
                if max(delay, min_delay) <= pre_delay:
                    instant_pre_proc()
                    pre_proc = lambda:None
                def _delay(proc, delay):
                    def _f():
                        time.sleep(max(0, delay - pre_delay))
                        pre_proc()
                        time.sleep(pre_delay)
                        proc()
                    return _f 
                proc = _delay(proc, max(delay, min_delay))
        t = threading.Thread(target=proc)
        self.threads[key] = t
        t.start()
        
    def isBusy(self, key):
        return key in self.threads and self.threads[key].is_alive()
    
    def gc(self):
        to_del = []
        for i in self.threads:
            if not self.threads[i].is_alive():
                to_del.append(i)
        for i in to_del:
            del self.threads[i]

class timeline:

    def __init__(self, duration=0):
        self.events = []
        self.duration = duration
        self.endtime = 0

    def do(self, func):
        self.events.append(func)
        return self

    def sleep(self, seconds):
        return self.do(lambda: time.sleep(seconds))

    def sleep_until(self, seconds=0):
        def _f():
            rem = self.endtime - time.time() - seconds
            if rem > 0:
                time.sleep(rem)
        return self.do(_f)

    def do_every_until(self, interval, func, seconds=0, do_at_start=True):
        if do_at_start:
            self.do(func)
        def _f():
            end = self.endtime - seconds
            while time.time() + interval < end:
                time.sleep(interval)
                func()
            time.sleep(max(0, end - time.time()))
        return self.do(_f)

    def __call__(self):
        self.endtime = time.time() + self.duration
        for func in self.events:
            func()
