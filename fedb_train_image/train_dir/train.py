#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

# from fespark.sql import SparkSession

import numpy as np
import pandas as pd
import lightgbm as lgb
import os

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV

print('train file')

# bucket='feoutput'

# data_path = 'ins'
# data_location = 's3://{}/{}'.format(bucket, data_path)
# model_path = 'model'
# model_location = 's3://{}/{}'.format(bucket, model_path)
prefix = '/opt/ml/'

input_path = prefix + 'input/data'
output_path = os.path.join(prefix, 'output')
model_path = os.path.join(prefix, 'model')

# print(data_location)

# # bucket='feoutput'
# f1 = data_location+'/part-00043-d4365180-5aa4-4139-b62f-f658e6071763-c000.csv'
# f2 = data_location+'/part-00174-d4365180-5aa4-4139-b62f-f658e6071763-c000.csv'
# # data_location = 's3://{}/{}'.format(bucket, data_path)

# File mode, the input files are copied to the directory specified here.
channel_name='training'
training_path = os.path.join(input_path, channel_name)

f1 = training_path+'/part-00043-d4365180-5aa4-4139-b62f-f658e6071763-c000.csv'
f2 = training_path+'/part-00174-d4365180-5aa4-4139-b62f-f658e6071763-c000.csv'

train_set = pd.read_csv(f1, header=None, index_col=False)
predict_set = pd.read_csv(f2, header=None, index_col=False)

# train_set contains features
y_train = train_set.loc[:,0]
# print(type(y_train))
x_train = train_set.drop(columns=0)
# print(x_train.loc[0])

y_predict = predict_set.loc[:,0]
x_predict = predict_set.drop(columns=0)


lgb_train = lgb.Dataset(x_train, y_train)
lgb_eval = lgb.Dataset(x_predict, y_predict, reference=lgb_train)


# specify your configurations as a dict
params = {
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': {'l2', 'l1'},
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0
}

print('LGB Starting training...')
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=20,
                valid_sets=lgb_eval,
                early_stopping_rounds=5)

gbm.save_model(model_path+'/model.txt')

