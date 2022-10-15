from pathlib import Path
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from .NeuralNet import NeuralNet
import joblib
import os.path

_path = (Path(__file__).parent / '../../../assets/durationModel.pt').resolve()
_scalerPath = (Path(__file__).parent / '../../../assets/durationScale.save').resolve()


class DurationTrainer:
    """
    The singleton class handles the full training of the model for predicting session duration.
    It also has a predict method to predict the session duration of a user given past
    average information.
    """
    _instance = None
    _model = NeuralNet()
    _loss_fn = nn.MSELoss()
    _optimizer = torch.optim.Adam(_model.parameters(), lr=0.002)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DurationTrainer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        print("Initializing")
        if os.path.exists(_path):
            self._model.load_state_dict(torch.load(_path))
        if os.path.exists(_scalerPath):
            self._scaler = joblib.load(_scalerPath)
        else:
            self._scaler = StandardScaler()

    def train(self, data):
        """
        The method trains the neural network in 10000 epochs
        :param data: The pandas dataframe. It should contain the following columns:
                     dropped_frames_min, dropped_frames_mean, FPS_min, FPS_max, FPS_mean, FPS_std,
                     RTT_min, RTT_max, RTT_mean, RTT_std, bitrate_min, bitrate_max, bitrate_mean,
                     bitrate_std, duration
        :return: None
        """
        def preprocess():
            """
            Handles the preprocessing stage of the data.
            It scales the data and transforms to a usable tensor
            :return: Tensor dataset
            """
            x = data.drop(['duration'], axis=1)
            y = data['duration']
            if hasattr(self._scaler, "n_features_in_"):
                x = self._scaler.transform(x)
            else:
                x = self._scaler.fit_transform(x)
            return TensorDataset(torch.from_numpy(x.astype(np.float32)),
                                 torch.from_numpy(y.values.astype(np.float32)).unsqueeze(dim=1))

        def train_step(device):
            """
            Handles a single epoch of the training
            :param device: The device to be used in the training
            :return: None
            """
            train_loss, train_acc = 0, 0
            self._model.train()
            for batch, (X, y) in enumerate(data_loader):
                X, y = X.to(device), y.to(device)
                self._optimizer.zero_grad()
                y_pred = self._model(X)
                loss = self._loss_fn(y_pred, y)
                train_loss += loss
                loss.backward()
                self._optimizer.step()

        batch_size = 32
        dataset = preprocess()
        data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        epochs = 10000
        for epoch in range(epochs):
            train_step(
                device='cpu'
            )
        torch.save(self._model.state_dict(), _path)


def DurationPredict(data):
    """
    The function is used for predicting the session duration of a user given his metrics
    :param data: Pandas dataframe containing the following
             dropped_frames_min, dropped_frames_mean, FPS_min, FPS_max, FPS_mean, FPS_std,
             RTT_min, RTT_max, RTT_mean, RTT_std, bitrate_min, bitrate_max, bitrate_mean,
             bitrate_std
    :return: The predicted session duration.
    """
    _model = NeuralNet()
    if os.path.exists(_path):
        _model.load_state_dict(torch.load(_path))
        if os.path.exists(_scalerPath):
            _scaler = joblib.load(_scalerPath)
        else:
            _scaler = StandardScaler()
        if hasattr(_scaler, "n_features_in_"):
            data = _scaler.transform(data)
        data = torch.from_numpy(data.values.astype(np.float32))
        _model.eval()
        with torch.no_grad():
            return _model(data).item()
    else:
        return None
