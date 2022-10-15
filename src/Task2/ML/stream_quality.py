import joblib
import pandas as pd


class QualityPredictor:
    _instance = None
    _scaler = None
    _predict = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QualityPredictor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._scaler is None:
            print(joblib.load('../../../assets/scaler.save'))
            self._scaler = joblib.load('../../../assets/scaler.save')
        if self._predict is None:
            self._predict = joblib.load('../../../assets/regression.save')

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


test = pd.DataFrame(data=[[-0.938268, -0.524444, 0.244128, -0.089892, -0.017157, -0.015607, 12]], columns=['fps_mean',
                                                                                                           'fps_std',
                                                                                                           'rtt_mean',
                                                                                                           'rtt_std',
                                                                                                           'dropped_frames_mean',
                                                                                                           'dropped_frames_std',
                                                                                                           'dropped_frames_max'])
quality = QualityPredictor()
print(quality.predict(test))
