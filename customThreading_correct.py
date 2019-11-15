# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 13:30:39 2019

@author: GELab
"""

#!/usr/bin/python

import queue
import threading
import time

exitFlag = 0

class Worker(threading.Thread):
    
    def __init__(self,  name, workQ, resultQ,task,Lock):
        threading.Thread.__init__(self)
      
        self.name = name
        
        ##global items
        self.workQ = workQ
        self.resultQ = resultQ
        self.task = task
        self.Lock = Lock
        self.keepActive = True
        self.daemon = True
    
    def _getWork(self):
        ##throws exception
        
        
        with self.Lock:
            priority,args = self.workQ.get(False)
            self.workQ.task_done()
            return priority,args
  
       
    def _performTask(self,args):
        
        return self.task(args)
    
    
    def _fillResultQueue(self, priority,result):
        
        with self.Lock:
            self.resultQ.put((priority,result))
            

    def workContinously(self):
        
        while self.keepActive:
            
            time.sleep(1) ## halt for self.keepActive to changed
            
            try:
                
                priority,args = self._getWork()
                result = self._performTask(args)
                self._fillResultQueue(priority,result)
                
                
#                print ("processed  taskID: ",  priority, 'by thread : ', self.name)
                
            except queue.Empty:
                
                ##most probably empty 
#                print(e)
                pass
                
            
    
    def run(self):
        print ("Starting " + self.name)
        self.workContinously()
        print ("Exiting " + self.name)
        
    def stop(self):
        
        self.keepActive = False



class ThreadPool():
    
    
    def __init__(self,threadTaskMapping):
        
        
        """
        threadTaskMapping = {Threadname: (task,args)}
        """
        self.Lock = threading.Lock()
        self.threadNames = threadTaskMapping.keys()
        self.workQueue = queue.PriorityQueue()
        self.resultQueue = queue.PriorityQueue()
#        self.keepActive = True
        
        self.threadQueueMapping = {}
        self.threads = []
        
        
    def launchWorkers(self):
        
        for tName in self.threadNames:
            workQueue = queue.PriorityQueue()
            thread = Worker(tName, self.workQueue, self.resultQueue,self.task,self.Lock)
            thread.deamon = True
            thread.start()
            self.threads.append(thread)
            
            
    def addWork(self,args):
        
        with self.Lock:
           
            epoch_time = time.time()
   
            self.workQueue.put((epoch_time,args))
            
            
    def getResults(self):
        
        
        try:
            with self.Lock:
                priority,result = self.resultQueue.get(False)
                
                return result
        
        except Exception as e:
            
            return None, e
            
            
            
            
    def completeAndExitWork(self):
        
#        self.workQueue.join()
        for thread in self.threads:
            thread.stop()
        
#        for thread in self.threads:
#            
#            thread.join()
        
        


if __name__ == '__main__':
    def task(*data):
        
        return data
    
    
    threadPool = ThreadPool(5,task)
    argsList = ["One", "Two", "Three", "Four", "Five"]
    
    for args in argsList:
       threadPool.addWork(args)
    
    
    threadPool.launchWorkers()

    print('result ',  threadPool.getResults())
    threadPool.completeAndExitWork()

   

