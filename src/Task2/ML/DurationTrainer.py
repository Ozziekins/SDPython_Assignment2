from pathlib import Path
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
import os.path

_modelPath = (Path(__file__).parent / '../../../assets/regressorModel.save').resolve()


class DurationTrainer:
    """
    The singleton class handles the full training of the model for predicting session duration.
    It also has a predict method to predict the session duration of a user given past
    average information.
    """
    _instance = None
    _model = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DurationTrainer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            if os.path.exists(_modelPath):
                self._model = joblib.load(_modelPath)
            else:
                self._model = Pipeline([
                    ('standardscaler', StandardScaler()),
                    ("linear_regression", SGDRegressor(max_iter=10000, tol=1e-3, warm_start=True))])

    def train(self, data):
        data = data.fillna(data.mean())
        x = data.drop(['duration'], axis=1)
        y = data['duration']
        self._model.fit(x, y)
        joblib.dump(self._model, _modelPath)

    def predict(self, data):
        try:
            return self._model.predict(data)[0]
        except NotFittedError as e:
            return None
