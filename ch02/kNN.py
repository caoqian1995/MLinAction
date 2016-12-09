# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 16:40:31 2016

@author: cq
"""

from numpy import *
import operator
from os import listdir


def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels
 
   
def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffmat = diffMat**2
    sqDistances = sqDiffmat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
  
  
def file2matrix(filename):
    love_dic = {"largeDoses":3,"smallDoses":2,"didntLike":1}
    fr = open(filename)
    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        if listFromLine[-1].isdigit():
            classLabelVector.append(int(listFromLine[-1]))
        else:
            classLabelVector.append(love_dic.get(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector
  
  
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals
  
  
def datingClassTest():
    horatio = 0.1
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*horatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with:%d,the real answer is:%d" %(classifierResult,datingLabels[i])
        if(classifierResult != datingLabels[i]):
            errorCount += 1.0
    print "the total error rate is:%f" %(errorCount/float(numTestVecs))
  
  
def classifyPerson():
    resultList = ['not at all','in small doses','in large doses']
    percentTat = float(raw_input("percentage of video games:"))
    ffmile = float(raw_input("fly miles:"))
    ice = float(raw_input("ice cream:"))
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    inArr = array([ffmile,percentTat,ice])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)   
    print "you will maybe like this one:",resultList[classifierResult-1]
  
  
def img2vector(filename):
    returnVector = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            returnVector[0,32*i+j] = int(line[j])
    return returnVector
  
  
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        classNumber = int(fileNameStr.split('_')[0])
        hwLabels.append(classNumber)
        trainingMat[i,:] = img2vector('trainingDigits/%s' %fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0.0
    testLength = len(testFileList)
    for i in range(testLength):
        fileNameStr = testFileList[i]
        classNumber = int(fileNameStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' %fileNameStr)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwLabels,3)
        #print "the classifier is:%d  the real number is:%d" % (classifierResult,classNumber)
        if classifierResult != classNumber:
            errorCount += 1
    print "the total error number is :%d" %errorCount
    print "the total number is :%d" %testLength
    print "the total error rate is :%f" % (errorCount/float(testLength))
