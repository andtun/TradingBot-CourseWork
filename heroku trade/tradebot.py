import abc
import threading
import time
import pandas as pd
import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential, model_from_json, load_model, save_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from alpaca_trade_api import REST

class AlpacaPaperSocket(REST):
    def __init__(self):
        super().__init__(
            key_id='PKE4YFUPUJXT4RI2JT8O',
            secret_key='Tsmc105gRWmtboD3lR9N0ts11pH4lCl3ryFBntYS',
            base_url='https://paper-api.alpaca.markets'
        )


class TradingSystem(abc.ABC):

    def __init__(self, api, symbol, time_frame, system_id, system_label):
        # Connect to api
        # Connect to BrokenPipeError
        # Save fields to class
        self.api = api
        self.symbol = symbol
        self.time_frame = time_frame
        self.system_id = system_id
        self.system_label = system_label
        thread = threading.Thread(target=self.system_loop)
        thread.start()

    @abc.abstractmethod
    def place_buy_order(self):
        pass

    @abc.abstractmethod
    def place_sell_order(self):
        pass

    @abc.abstractmethod
    def system_loop(self):
        pass

class PortfolioManagementSystem(TradingSystem):

    def __init__(self):
        super().__init__(AlpacaPaperSocket(), 'IBM', 6048000, 1, 'AI_PM')

    def place_buy_order(self):
        pass

    def place_sell_order(self):
        pass

    def system_loop(self):
        pass

Activation ='tanh'

# Class to develop your AI portfolio manager
class AIPMDevelopment:

    def __init__(self):
        # Read your data in and split the dependent and independent
        data = pd.read_csv('IBM.csv')
        X = data['Delta Close']
        y = data.drop(['Delta Close'], axis=1)

        # Train test spit
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # Create the sequential
        network = Sequential()

        # Create the structure of the neural network
        network.add(Dense(1, input_shape=(1,), activation=Activation))
        network.add(Dense(3, activation=Activation))
        network.add(Dense(3, activation=Activation))
        network.add(Dense(3, activation=Activation))
        network.add(Dense(1, activation=Activation))

        # Compile the model
        network.compile(
                      optimizer='rmsprop',
                      loss='hinge',
                      metrics=['accuracy']
                      )
        # Train the model
        network.fit(X_train.values, y_train.values, epochs=100)

        # Evaluate the predictions of the model
        y_pred = network.predict(X_test.values)
        y_pred = np.around(y_pred, 0)
        print(classification_report(y_test, y_pred))

        # Save structure to json
        #model = network.to_json()
        #with open("model.json", "w") as json_file:
        #    json_file.write(model)

        # Save weights to HDF5
        save_model(network, "weights.h5")

AIPMDevelopment()


# AI Portfolio Manager
class PortfolioManagementModel:

    def __init__(self):
        # Data in to test that the saving of weights worked
        data = pd.read_csv('IBM.csv')
        X = data['Delta Close']
        y = data.drop(['Delta Close'], axis=1)

        # Read structure from json
        """json_file = open('model.json', 'r')
        json = json_file.read()
        json_file.close()
        self.network = model_from_json(json)"""

        # Read weights from HDF5
        self.network = load_model("weights.h5")

        # Verify weights and structure are loaded
        y_pred = self.network.predict(X.values)
        y_pred = np.around(y_pred, 0)
        print(classification_report(y, y_pred))
        print(self.network.evaluate(y, y_pred))

PortfolioManagementModel()

