from __future__ import division
import math
import numpy as np


class SimpleNet(object):
    def __init__(self):
        """Simple deep net object with no neurons"""
        self.resetLayers()

    def setInputLayer(self, size):
        """Set the size of the input layer"""
        self._input_layer.resizeLayer(size, 0)
        self._wired = False

    def setOutputLayer(self, size):
        """Set the size of the output layer"""
        self._output_layer.resizeLayer(size, 0)
        self._wired = False

    def addHiddenLayer(self, size):
        """Add a hidden layer just above the output layer"""
        hidden_layer = SimpleLayer(size, 0)
        self._layers.insert(-1,hidden_layer)
        self._wired = False

    def resetLayers(self):
        """Reset the neural net"""
        self._input_layer = InputLayer(0)
        self._output_layer = SimpleLayer(0,0)
        self._layers = [self._input_layer, self._output_layer]
        self._wired = False

    def addLayerSet(self,input_size, hidden_list, output_size):
        """Add an input layer, array of hidden layers, and an output layer"""
        self.resetLayers()
        self.setInputLayer(input_size)
        self.setOutputLayer(output_size)
        for hidden_size in hidden_list:
            self.addHiddenLayer(hidden_size)

    def _rewire(self):
        """Rewire the internal layers to point to correct places"""
        old_layer = self._input_layer
        for layer in self._layers[1:]:
            layer.above = old_layer
            layer.resizeLayer(layer.size,old_layer.size)
            old_layer = layer
        self._wired = True

    def evaluateOnce(self,inputs):
        """Evaluate the net with a single set of inputs"""
        if not self._wired:
            self._rewire()
        if len(inputs) != self._input_layer.size:
            raise IndexError("Expected input of size %d but instead got %d" % (self._input_layer.size,len(inputs)))
        values = np.array(inputs)
        self._input_layer.setValues(values)
        return self._output_layer.evaluate()


    def train(self, training_inputs, training_outputs, iterations):
        """Train the network with a set of sets of inputs and the corresponding outputs"""
        for i in xrange(iterations):
            for j,inputs in enumerate(training_inputs):
                output = self.evaluateOnce(inputs)
                error = training_outputs[j] - output
                self._output_layer.backPropogate(error)

    def trainOnce(self, input, correct):
        output = self.evaluateOnce(input)
        error = correct - output
        self._output_layer.backPropogate(error)

    def getWeights(self):
        """Get a Python list of numpy weight arrays"""
        return [layer.weights for layer in self._layers]

    def setWeights(self, weights):
        """Set internal weights using a Python list of numpy arrays"""
        if len(weights) != len(self._layers):
            raise IndexError("Expected array of weights of size %d but got %d" % (len(self._layers),len(weights)))
        for i,weight in enumerate(weights):
            self._layers[i].weights = weights

    def __repr__(self):
        rep = "SimpleNet with:"
        rep = rep + "\nInput: "+str(self._input_layer.size)
        for layer in self._layers[1:-1]:
            rep = rep + "\nHidden: "+str(layer.size)
        rep = rep + "\nOutput: "+str(self._output_layer.size)
        return rep

class SimpleLayer(object):
    def __init__(self, size, inputs):
        """A simple layer for a simple network with <size> neurons and <inputs> in the layer above.
            Should not be evaluated or created outside of the SimpleNet"""
        self.resizeLayer(size, inputs)
        self.above = None # Reference to the layer above this one
        self.last_output = None # Last output of this layer
        self.last_input = None # Last input from the layer above

    def resizeLayer(self, new_size, new_inputs):
        """Reset the weights and sizes"""
        self.size = new_size
        self.inputs = new_inputs
        self.weights = 2 * np.random.random((self.inputs,self.size)) - 1

    def _sigmoid(self, x):
        """Calculate the sigmoid function"""
        return 1 / (1 + np.exp(-x))

    def _sigmoidDerivative(self, x):
        """Calculate the derivative of a sigmoid"""
        return x * (1 - x)

    def evaluate(self):
        """Evaluate the layer"""
        self.last_input = self.above.evaluate()
        self.last_output = self._sigmoid(np.dot(self.last_input,self.weights))
        return self.last_output

    def backPropogate(self, error):
        """Use the last evaluation to adjust weights"""
        delta = error * self._sigmoidDerivative(self.last_output)
        error_above = delta.dot(self.weights.T)
        adjustment = self.last_input.T.dot(delta)
        self.weights += adjustment
        self.above.backPropogate(error_above)


class InputLayer(SimpleLayer):
    def __init__(self, size):
        """A special SimpleLayer that doesn't evaluate and only passes inputs"""
        SimpleLayer.__init__(self, size, 0)
        self.values = np.zeros((size,))

    def resizeLayer(self, new_size, input_size):
        """Reset the size of the layer"""
        self.size = new_size
        self.inputs = 0
        self.values = np.zeros((new_size,1))

    def setValues(self, values):
        """Set the list of inputs as numpy array"""
        self.values = values
        self.values.resize((1,self.size))

    def evaluate(self):
        """Get the set if inputs"""
        return self.values

    def backPropogate(self, error):
        return




def testNet():
    # Inspired by https://medium.com/technology-invention-and-more/how-to-build-a-simple-neural-network-in-9-lines-of-python-code-cc8f23647ca1
    NN = SimpleNet()
    NN.addLayerSet(3,[],1)
    print NN
    training_inputs = np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
    training_outputs = np.array([[0, 1, 1, 0]]).T
    NN.train(training_inputs,training_outputs,10000)
    print NN.evaluateOnce(np.array([1,0,0]))

    NN2 = SimpleNet()
    NN2.addLayerSet(3,[4],1)
    print NN2
    training_inputs2 = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1], [0, 0, 0]])
    training_outputs2 = np.array([[0, 1, 1, 1, 1, 0, 0]]).T
    NN2.train(training_inputs2,training_outputs2,60000)
    print NN2.evaluateOnce(np.array([1, 1, 0]))

if __name__=="__main__":
    testNet()
