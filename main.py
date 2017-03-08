# coding=utf-8
__author__ = 'Jiacy'

import math
import os
import re
import matplotlib.pyplot as plt
import numpy as np

class DealWithRcData():

    def __init__(self):
        # self.XMax = [137.24, 74.2284, 124.404, 84.6277, 147.247, 74.9338, 132.293, 79.3712]
        # self.YMax = [1113.17, 1304.28, 1434.18, 1333.82, 1795.96, 1995.26, 754.034, 1973.59]
        # self.ZMax = [2078.91, 1426.89, 1108.82, 1637.64, 1232.18, 1227.47, 1629.87, 1963.13]
        self.XMax = [0] * 8
        self.YMax = [0] * 8
        self.ZMax = [0] * 8
        self.DataPath = ''
        self.WorkSpaceX = 0
        self.WorkSpaceY = 0
        self.WorkSpaceZ = 0
        self.DEALDATA = True

    def InputData(self):
        self.DataPath = raw_input('Please input your data path(For Example "D:/"):')
        # self.WorkSpaceX = raw_input('Please input Z positon:')
        # self.WorkSpaceY = raw_input('Please input Y positon:')
        # self.WorkSpaceZ = raw_input('Please input Z positon:')

    def find_data(self):
        if os.path.isdir(self.DataPath):
            if os.path.exists(self.DataPath):
                for path,dire,eachfile in os.walk(self.DataPath):
                    for each in eachfile:
                        if '.out' in each:
                            datafile = open(path+'/'+each,'r')
                            while datafile.readline():
                                if 'VALUES' in datafile.readline():
                                    for i in range(5):
                                        datafile.readline()
                                    pattern = re.compile('(\d.\d+)E(\+|\-)(\d\d)')
                                    for i in range(8):
                                        temp = re.findall(pattern,datafile.readline())
                                        tempX = self.sciennumToNum(temp[3])
                                        tempY = self.sciennumToNum(temp[4])
                                        tempZ = self.sciennumToNum(temp[5])
                                        if self.XMax[i] < tempX:
                                            self.XMax[i] = tempX
                                        if self.YMax[i] < tempY:
                                            self.YMax[i] = tempY
                                        if self.ZMax[i] < tempZ:
                                            self.ZMax[i] = tempZ
            else:
                print 'No path existed!'
                self.DEALDATA = False
        else:
            print 'Please input a path!'
            self.DEALDATA = False

    def DealWithData(self):
        for i in range(8):
            self.XMax[i] /= math.sqrt(0.02)
            self.YMax[i] /= math.sqrt(0.02)
            self.ZMax[i] /= math.sqrt(0.02)
        sumX = sum(self.XMax)
        meanX = sumX/8.0
        totalX = 0
        for each in self.XMax:
            totalX += (each - meanX)**2
        kesaiX = math.sqrt(totalX/7.0)
        result = 20 * math.log((kesaiX + meanX)/meanX,10)
        print 'x方向的标准差为'.decode('utf-8').encode('GBK') + str(result)

        sumY = sum(self.YMax)
        meanY = sumY/8.0
        totalY = 0
        for each in self.YMax:
            totalY += (each - meanY)**2
        kesaiY = math.sqrt(totalY/7.0)
        result = 20 * math.log((kesaiY + meanY) / meanY, 10)
        print 'y方向的标准差为'.decode('utf-8').encode('GBK') + str(result)

        sumZ = sum(self.ZMax)
        meanZ = sumZ/8.0
        totalZ = 0
        for each in self.ZMax:
            totalZ += (each - meanZ)**2
        kesaiZ = math.sqrt(totalZ/7.0)
        result = 20 * math.log((kesaiZ + meanZ) / meanZ, 10)
        print 'z方向的标准差为'.decode('utf-8').encode('GBK') + str(result)

    def sciennumToNum(self,tupledata):
        if tupledata[1] == '+':
            number = float(tupledata[0]) * 10 ** int(tupledata[2])
        else:
            number = float(tupledata[0]) * 10 ** (-int(tupledata[2]))
        return number

    def displayData(self):
        print 'Z series:' + str(self.XMax)
        print 'Y series:' + str(self.YMax)
        print 'Z series:' + str(self.ZMax)
        # point = ('1','2','3','4','5','6','7','8')
        # data = [np.array(self.XMax),np.array(self.YMax),np.array(self.ZMax)]
        # x = np.arange(len(point))
        # plt.figure()
        # ax = plt.axes([0.16,0.12,0.77,0.77])
        #
        # ax.barh(x,data[2],align='center',color='g',alpha=0.5)
        #
        # plt.ylim(-1,8)
        # plt.xlabel(u'归一化场强')
        # plt.ylabel('8 point of workspace')
        # ax.set_yticks(x)
        # ax.set_yticklabels(point)

        # plt.show()

    def main(self):
        self.InputData()
        self.find_data()
        if self.DEALDATA:
            self.DealWithData()
            self.displayData()

        y = [2.58,2.0071,2.1933]
        x = ['x','y','z']
        plt.bar(np.arange(len(y)),y)
        plt.xticks([0.5,1.5,2.5],x)
        plt.show()


def main():
    while True:
        test = DealWithRcData()
        test.main()

if __name__ == '__main__':
    main()

