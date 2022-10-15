from torch import nn


class NeuralNet(nn.Module):
    """
    Neural network model to be used for predicting session duration.
    """
    def __init__(self):
        super().__init__()
        self.layer_pred = nn.Sequential(
            nn.Linear(in_features=14, out_features=64, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=128, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=64, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=32, bias=True),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=1, bias=True),
        )

    def forward(self, X):
        return self.layer_pred(X)
