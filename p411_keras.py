'''
Created on Jul 22, 2016

keras.py implements a neural network with the keras framework.

This example trains using the Handprint images 

from Python Machine Learning by Sebastian Raschka

@author: richard lyman
'''
 
import ocr_utils
import numpy as np



def do_keras(X_train,X_test, y_train_ohe, y_train,y_test):
    print('First 3 labels: ', y_train[:3])
    
    print('\nFirst 3 labels (one-hot):\n', y_train_ohe[:3])
    
    from keras.models import Sequential
    from keras.layers.core import Dense
    from keras.optimizers import SGD
    
    np.random.seed(1) 
    
    model = Sequential()
    model.add(Dense(input_dim=X_train.shape[1], 
                    output_dim=50, 
                    init='uniform', 
                    activation='tanh'))
    
    model.add(Dense(input_dim=50, 
                    output_dim=50, 
                    init='uniform', 
                    activation='tanh'))
    
    model.add(Dense(input_dim=50, 
                    output_dim=y_train_ohe.shape[1], 
                    init='uniform', 
                    activation='softmax'))
    
    sgd = SGD(lr=0.001, decay=1e-7, momentum=.9)
    model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=["accuracy"])
    
    model.fit(X_train, y_train_ohe, 
              nb_epoch=50, 
              batch_size=300, 
              verbose=1, 
              validation_split=0.1
              )
    y_train_pred = model.predict_classes(X_train, verbose=0)
    print('First 3 predictions: ', y_train_pred[:3])
    train_acc = np.sum(y_train == y_train_pred, axis=0) / X_train.shape[0]
    print('Training accuracy: %.2f%%' % (train_acc * 100))
    
    
    y_test_pred = model.predict_classes(X_test, verbose=0)
    test_acc = np.sum(y_test == y_test_pred, axis=0) / X_test.shape[0]
    print('Test accuracy: %.2f%%' % (test_acc * 100))

input_filters_dict = {'font': ('HANDPRINT',)}
output_feature_list = ['m_label_one_hot','image','m_label'] 
ds = ocr_utils.read_data(input_filters_dict = input_filters_dict, 
                         output_feature_list=output_feature_list, 
                         engine_type='keras',
                         test_size = .1,
                         dtype=np.float32,
                         random_state=0)

X_train = ds.train.features[1]
X_test = ds.test.features[1]
y_train_ohe = ds.train.features[0]
y_train = ds.train.features[2]-48
y_test = ds.test.features[2]-48    
do_keras(X_train,X_test, y_train_ohe, y_train, y_test)


print ('\n########################### No Errors ####################################')
