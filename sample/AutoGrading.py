from sample.web.app import flaskRun
from multiprocessing import Pool
from sample.FileMonitor import Monitor
import  os
from sample.grading.main  import grading
import requests
import time
import platform
import atexit


class AutoGrading(object):

    def __init__(self):
        self.x = 1
        self.uploadedFileAdress = os.path.dirname(os.path.realpath(__file__)) + "/web/static/upload/unclassify/"

    def run(self):
        # app = Monitor("server")
        p = Pool(2)
        p.apply_async(self.moniter, args=(1,))
        p.apply_async(flaskRun())

    def moniter(self,number):
        app = Monitor("server")
        app.monitor()

    def grading(self,imageAddress, recogFlag):
        imageAddress = self.uploadedFileAdress + imageAddress
        return grading(imageAddress,"",recogFlag)
