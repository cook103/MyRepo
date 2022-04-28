import numpy as np
import pandas as pd
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


def Predict():
  url = "https://raw.githubusercontent.com/gheniabla/datasets/master/height-weight.csv"
  datatFrame = pd.read_csv(url, sep=',', index_col=False)

  X = datatFrame.Height
  Y = datatFrame.Weight

  TrainX = X.sample(frac=0.9, random_state=0)
  TestX = X.drop(TrainX.index)
  TrainY = Y.sample(frac=0.9, random_state=0)
  TestY = Y.drop(TrainY.index)

  model = tf.keras.Sequential()
  model.add(tf.keras.layers.Dense(8))
  model.add(tf.keras.layers.Dense(1))
  model.compile(optimizer=tf.train.AdamOptimizer(learning_rate=0.1), loss='mean_absolute_error')
  #build
  model.fit(np.array(X), np.array(Y), batch_size=32, epochs=10)

  height = 164;

  print("Prediction weight \n",model.predict([height]))   #prediction


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Predict();





