import abc, typing
from metrics.util.timer import timer
import networkit as nk


class Metric(abc.ABC):
    """
    Abstract metric class to be inherited by all metrics.

    Args:
        abc (_type_): _description_
    """
    def __init__(self, name: str, graph: nk.Graph) -> None:
        super().__init__()

    @abc.abstractmethod
    def __call__(self, y_true, y_pred):
        pass

    def __str__(self):
        return self.__class__.__name__