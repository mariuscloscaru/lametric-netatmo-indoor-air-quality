import json

class Setup(object):

    def __init__(self):
        self.data = {}
        self.data['frames'] = []
        self.index = 0

    def addTextFrame(self, icon, text):
        frame = {}
        frame['index'] = self.index
        frame['icon']  = icon
        frame['text']  = text
        self.data['frames'].append(frame)
        self.index += 1

    def addGoalFrame(self, icon, start, current, end, unit):
        frame = {}
        frame['index'] = self.index
        frame['icon']  = icon
        frame['goalData'] = {}
        frame['goalData']['start'] = start
        frame['goalData']['current'] = start
        frame['goalData']['end'] = start
        frame['goalData']['unit'] = unit
        self.data['frames'].append(frame)
        self.index += 1

    def addSparklineFrame(self, data):
        frame = {}
        frame['index'] = self.index
        frame['chartData'] = data
        self.data['frames'].append(frame)
        self.index += 1
        
    def getData(self):
        return self.data;