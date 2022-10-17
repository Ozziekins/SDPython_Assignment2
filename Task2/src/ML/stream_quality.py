from pathlib import Path

import joblib


class QualityPredictor:
    _instance = None
    _scaler = None
    _predict = None

    _scalerPath = (Path(__file__).parent / '../../../Task2/assets/scaler.save').resolve()
    _regressorPath = (Path(__file__).parent / '../../../Task2/assets/regression.save').resolve()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QualityPredictor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._scaler is None:
            self._scaler = joblib.load(self._scalerPath)
        if self._predict is None:
            self._predict = joblib.load(self._regressorPath)

    def predict(self, df):
        """
        Prediction method
        :param df: Pandas dataframe with the following columns 'fps_mean', 'fps_std', 'rtt_mean', 'rtt_std', 'dropped_frames_mean',
       'dropped_frames_std', 'dropped_frames_max'
        :return: The Prediction 0 (Good) or 1 (Bad)
        """
        self._scaler.transform(df)
        df_drop = df.drop(['dropped_frames_max'], axis=1)
        return self._predict.predict(df_drop)[0]

