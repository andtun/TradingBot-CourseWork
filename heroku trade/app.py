from bottle import *

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



run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug=False)
