import numpy as np

class Queue:
    def __init__(self, max_length, channels=2, data=None):
        if data:
            self.data = np.array(data, dtype='int16')
        else:
            self.data = np.zeros((channels, max_length), dtype='int16')
        self.max_length = max_length
        self.channels = channels
    
    def length(self):
        return len(self.data)

    def append(self, value):
        self.data = np.concatenate((self.data, value), axis=1)
        # Trim the queue
        self.data = self.data[:, self.max_length * -1:]

    def read_last(self, length):
        return self.data[:, length * -1:]
    
    def pop_first(self, length):
        value = self.data[:, 0:length]
        self.data = self.data[:, length:]
        return value


def test_init():
    queue = Queue(5, channels=2)
    assert queue.data.shape == (2, 5)
    np.testing.assert_array_equal(queue.data, np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0 ,0]]))

def test_append():
    queue = Queue(10)
    data = np.array([
        np.ones(5, dtype='int16'),
        np.ones(5, dtype='int16')
    ])
    queue.append(data)
    assert queue.data.shape == (2, 10)
    expected_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    expected = np.array([np.array(expected_values), np.array(expected_values)])
    np.testing.assert_array_equal(queue.data, expected)


def test_pop_first():
    queue = Queue(5, data=[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
    data = queue.pop_first(2)
    np.testing.assert_array_equal(data, np.array([[1, 2], [1, 2]]))
    np.testing.assert_array_equal(queue.data, np.array([[3, 4, 5], [3, 4, 5]]))


def test_read_last():
    queue = Queue(5, data=[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
    data = queue.read_last(2)
    np.testing.assert_array_equal(data, np.array([[4, 5], [4, 5]]))
    np.testing.assert_array_equal(queue.data, np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]))
