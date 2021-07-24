"""
Maintains all the models
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import keras

from sklearn.model_selection import LeaveOneOut
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from sklearn import metrics
from sklearn.metrics import mean_absolute_percentage_error as mape

import pmdarima as pmd

class ModelFactory:
    def __init__(self, dataset, **options):
        self.dataset = dataset
        self.train_sets = {}
        self.test_sets = {}
        self.test_err = {}
        self.predict_sets = {}
        #self.pipeline = Pipeline([
        #    ('standardize', StandardScaler())
        #])
        self.model_specs = {}
        self.pipeline = None
        self.model = None
        self.trained_model = {}
        self.model_type = options['model']
        self.setup_model()
        self.cv_method = LeaveOneOut()
        self.reg_metric = 'neg_mean_absolute_error'

        # plotting
        self.plot_specs = {}
        self.plot_specs['color'] = 'red'
        self.plot_specs['label'] = 'Revenue'
    
        self.ss_fit = {}

    def setup_model(self):
        self.factory = {"SVR", "ARIMA", "DRNN"}
        if self.model_type in self.factory:
            self.model_call = getattr(self, "model_"+self.model_type)
        else:
            print("ERROR! Model N/A")

    def run_full(self):
        """Run full experiment"""
        self.prepare_data()
        self.train_model()
        self.test_model()
        if self.model_type == "SVR":
            self.forecast_model()

    def prepare_data(self):
        print("\nPreparing data for training...")
        for name, (data,labels) in self.dataset.items():
            shout_prepare = "\nTicker/Shape: {} --> {}".format(name, data.shape)
            print(shout_prepare)
            if np.any(np.isnan(labels)):
                print("Labels have NaN!")
                # Ignore this ticker for now!
                continue
            # Clean missing features
            self.replace_missing_mean(data)
            # Split into training/test sets -- pair with labels
            train_set, test_set, X_predict = self.split_data(data,labels)
            self.train_sets[name] = train_set
            self.test_sets[name] = test_set
            self.predict_sets[name] = X_predict

    def forecast_model(self):
        for name, Xp in self.predict_sets.items():
            # load trained model
            clf = self.trained_model[name]
            print("\nPredicting Next Year {} with {}".format(name, self.model_type))
            # single sample, reshape!
            prediction = clf.predict(Xp.reshape(1, -1))
            print("Preidction: {}".format(prediction[0]))

    def test_model(self):
        for name, (X_test,y_test) in self.test_sets.items():
            # load trained model
            clf = self.trained_model[name]
            print("\nTesting {} with {}".format(name, self.model_type))
            if self.model_type == "SVR":
                prediction = clf.predict(X_test)
                pred_err = mape(y_test, prediction)
            elif self.model_type == "ARIMA":
                prediction = clf.predict(1)
                # MAPE for one sample
                pred_e = abs(y_test[0] - prediction) / y_test[0]
                pred_err = pred_e.item(0)
            elif self.model_type == "DRNN":
                X_test = self.ss_fit[name].transform(X_test)
                X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
                prediction = clf.predict(X_test)
                print(prediction)
                pred_err = mape(y_test, prediction)
        
            self.test_err[name] = pred_err
            print('\nTest MAPE: {:.3}\n'.format(pred_err))

    def train_model(self):
        for name, (X,y) in self.train_sets.items():
            print("\nTraining {} with {}".format(name, self.model_type))
            if self.model_type == "SVR":
                clf = self.model_call()
                clf.fit(X,y.ravel())
                print("Best parameters from grid search: ")
                print(clf.named_steps['gridsearchcv'].best_params_)
            elif self.model_type == "ARIMA":
                clf = self.model_call()
                clf.fit(y.reshape(-1, 1))
            elif self.model_type == "DRNN":
                clf = self.model_DRNN(X.shape[1])
                self.ss_fit[name] = StandardScaler().fit(X)
                X = self.ss_fit[name].transform(X)
                X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
                clf.fit(X, y)
            self.trained_model[name] = clf

    def model_DRNN(self, dim):
        self.model_specs['units'] = 10
        self.model_specs['dim'] = dim
        def _last_time_step_mse(Yt, Yp):
            return keras.metrics.mean_squared_error(Yt[:,-1],Yp[:-1])
        
        m = keras.models.Sequential([
           keras.layers.SimpleRNN(self.model_specs['units'], return_sequences=True, input_shape=[None,self.model_specs['dim']]),
           keras.layers.SimpleRNN(self.model_specs['units']),
           keras.layers.Dense(1)
        ])
        m.compile(loss="mse",optimizer="adam",metrics=[_last_time_step_mse])
        return m

    def model_SVR(self):
        # Default values
        self.model_specs['kernel'] = 'rbf'
        #self.model_specs['gamma'] = '0.1'
        self.param_grid = {
            "C": np.logspace(-8, 10, 17),
            "gamma": np.logspace(-4, 4, 9)
        }
        self.model = SVR(**self.model_specs)

        gscv = GridSearchCV(estimator=self.model, param_grid=self.param_grid, cv=self.cv_method, scoring=self.reg_metric)
        clf = self.apply_pipeline(gscv)
        return clf

    def model_ARIMA(self):
        #clf = pmd.auto_arima(X,start_p=1,start_q=1,test="adf",trace=True)
        clf = pmd.AutoARIMA(trace=False)
        return clf

    def apply_pipeline(self, m):
        # Standardize the train set + m
        return make_pipeline(StandardScaler(), m)
    
    def split_data(self, data, labels):
        n = data.shape[0]
        # can't use last point!
        X_train, y_train = data[:n-3,:], labels[2:-2]
        X_test, y_test = data[-3:-1,:], labels[-2:]
        X_predict = data[-1,:]
        return ((X_train,y_train), (X_test, y_test), X_predict)
    
    def replace_missing_mean(self, data):
        col_mean = np.nanmean(data, axis=0)
        idxs = np.where(np.isnan(data))
        if idxs:
            # we have some missing features
            data[idxs] = np.take(col_mean, idxs[1])

    def plot_labels(self):
        for name, (_,labels) in self.dataset.items():
            self.plot_series(name, labels)

    def plot_series(self, name, y):
        """Plot y vector vs indices"""
        if np.any(np.isnan(y)):
            print("Label for {} has NaN!".format(name))
            return
        plot_label = "{} for {}".format(self.plot_specs['label'],name)
        x = np.arange(y.shape[0])
        y_bounds = [np.min(y),np.max(y)]
        exw = 0.1*y_bounds[0]
        plt.ylim(y_bounds[0]-exw, y_bounds[1]+exw)
        plt.plot(x, y, color=self.plot_specs['color'],label=plot_label)
        plt.legend()
        plt.show()

