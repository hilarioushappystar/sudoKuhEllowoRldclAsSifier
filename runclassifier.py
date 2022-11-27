# Binary Classification for solving 4x4 Sudokus: 

# Original source code = https://machinelearningmastery.com/binary-classification-tutorial-with-the-keras-deep-learning-library/ 
# Credits: Jason Brownlee (PhD) for the original code and good tutorial writing skills :-)

import time 
import configfilereader as cfr
from pandas import read_csv
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold

###############################################
#
#  start
#
###############################################


if __name__ == "__main__":

    start_time = time.time()
    
    c = cfr.ConfigFileReader()
    parameterdict = c.readfile('configparams.txt')
    RAWDATAFILE = parameterdict['RAWDATAFILE']
    NUMLAYERS = int(parameterdict['NUMLAYERS'])

# load dataset
    dataframe = read_csv(RAWDATAFILE, header=None)

    dataset = dataframe.values

    labelcolumn = dataset.shape[1] - 1
    print('labelcolumn = ', labelcolumn)

# split into input (X) and output (Y) variables
    X = dataset[:,0:labelcolumn].astype(float)
    Y = dataset[:,labelcolumn]
    print('sizes == ', X.shape, Y.shape)
# encode class values as integers
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
# baseline model
    def create_baseline():
        # create model
        model = Sequential()
        for foo in range(NUMLAYERS):
            model.add(Dense(labelcolumn, input_shape=(labelcolumn,), activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        # Compile model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model
    
# evaluate model with standardized dataset
    estimator = KerasClassifier(model=create_baseline, epochs=100, batch_size=5, verbose=0)
    kfold = StratifiedKFold(n_splits=10, shuffle=True)
    results = cross_val_score(estimator, X, encoded_Y, cv=kfold)
    print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

    end_time = time.time()

    print('time taken (seconds) = ', end_time-start_time)