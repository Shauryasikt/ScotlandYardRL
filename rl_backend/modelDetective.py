import numpy as np
import tensorflow as tf
class Model(object):

    def __init__(self):
        tf.reset_default_graph
        self.learning_rate = 0.001
        self.columns = 1432
        self.X = tf.placeholder(shape=[None, self.columns], dtype=tf.float32, name="X")
    # The TD target value
        self.Y = tf.placeholder(shape=[None, 1], dtype=tf.float32, name="Y")

        self.hidden1 = int(self.columns/2)
        self.hidden2 = int(self.columns/2)
        self.hidden3 = int(self.columns/2)
        self.hidden4 = int(self.columns/2)
        self.hidden5 = int(self.columns/4)
        self.hidden6 = int(self.columns/4)
        self.hidden7 = int(self.columns/8)
        self.hidden8 = int(self.columns/8)
        self.out = 1

        self.weights = {
            'w1' : tf.Variable(tf.random_normal([self.columns, self.hidden1])),
            'w2' : tf.Variable(tf.random_normal([self.hidden1, self.hidden2])),
            'w3' : tf.Variable(tf.random_normal([self.hidden2, self.hidden3])),
            'w4' : tf.Variable(tf.random_normal([self.hidden3, self.hidden4])),
            'w5' : tf.Variable(tf.random_normal([self.hidden4, self.hidden5])),
            'w6' : tf.Variable(tf.random_normal([self.hidden5, self.hidden6])),
            'w7' : tf.Variable(tf.random_normal([self.hidden6, self.hidden7])),
            'w8' : tf.Variable(tf.random_normal([self.hidden7, self.hidden8])),
            'out' : tf.Variable(tf.random_normal([self.hidden8, self.out]))
        }

        self.biases = {
            'b1': tf.Variable(tf.random_normal([self.hidden1])),
            'b2': tf.Variable(tf.random_normal([self.hidden2])),
            'b3': tf.Variable(tf.random_normal([self.hidden3])),
            'b4': tf.Variable(tf.random_normal([self.hidden4])),
            'b5': tf.Variable(tf.random_normal([self.hidden5])),
            'b6': tf.Variable(tf.random_normal([self.hidden6])),
            'b7': tf.Variable(tf.random_normal([self.hidden7])),
            'b8': tf.Variable(tf.random_normal([self.hidden8])),
            'out': tf.Variable(tf.random_normal([self.out]))
            }


        self.layer1 = tf.nn.relu(tf.matmul(self.X, self.weights['w1']) + self.biases['b1'])
        self.layer2 = tf.nn.relu(tf.matmul(self.layer1, self.weights['w2']) + self.biases['b2'])
        self.layer3 = tf.nn.relu(tf.matmul(self.layer2, self.weights['w3']) + self.biases['b3'])
        self.layer4 = tf.nn.relu(tf.matmul(self.layer3, self.weights['w4']) + self.biases['b4'])
        self.layer5 = tf.nn.relu(tf.matmul(self.layer4, self.weights['w5']) + self.biases['b5'])
        self.layer6 = tf.nn.relu(tf.matmul(self.layer5, self.weights['w6']) + self.biases['b6'])
        self.layer7 = tf.nn.relu(tf.matmul(self.layer6, self.weights['w7']) + self.biases['b7'])
        self.layer8 = tf.nn.relu(tf.matmul(self.layer7, self.weights['w8']) + self.biases['b8'])


        self.pred = tf.nn.relu(tf.matmul(self.layer8, self.weights['out']) + self.biases['out'])

        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.pred, labels=self.Y))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
        self.init = tf.initialize_all_variables() # Do not change this. The line you used is deprecated.
        self.save_path = None
        # Creating a saver object with a maximum of 5 latest models to be saved. The oldest one is automatically deleted.
        self.saver = tf.train.Saver(max_to_keep = 5)

        global sess
        sess = tf.Session()
        sess.run(self.init)


    def predict(self,x):
        y = sess.run(self.pred, feed_dict={self.X:x})
        return y


    def optimize(self,x, y):
        sess.run([self.optimizer, self.cost], feed_dict={self.X: x, self.Y: y})

    def save(self, episode):
        # Saving the file path and storing the file path. The episode which it saves is appended to the file name.
        # Will make this more organized.
        self.save_path = self.saver.save(sess, 'models/detective_models/', global_step = episode)

    def restore(self):
        # Restoring the file from a previous save path.
        self.saver.restore(sess, self.save_path)
