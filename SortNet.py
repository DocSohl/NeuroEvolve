from __future__ import division
import numpy as np
from SimpleNet import SimpleNet

def createNet(bins):
    NN = SimpleNet()
    NN.addLayerSet(bins,[bins*4 for i in range(5)],bins)
    return NN

def trainNet(NN, bins, iterations):
    print "Training",
    for i in xrange(iterations):
        input = np.random.randint(bins,size=bins) / bins
        correct = np.sort(input)
        NN.trainOnce(input,correct)
        if i / iterations * 100 % 10 == 0:
            print " .",
    print

def evaluateNet(NN, bins, iterations):
    num_correct = 0
    for i in xrange(iterations):
        input = np.random.randint(bins,size=bins) / bins
        correct = np.sort(input)
        output = NN.evaluateOnce(input)[0]
        print "Correct: " + str(correct * bins)
        print "Output: " + str(output * bins)
        for j in range(bins):
            accurate = True
            if correct[j] * bins != round(output[j] * bins):
                accurate = False
                break
        if accurate:
            num_correct += 1
    print "Accuracy: "+str(float(num_correct) / iterations * 100)

if __name__=="__main__":
    NN = createNet(5)
    trainNet(NN,5,10000000)
    evaluateNet(NN,5,100)