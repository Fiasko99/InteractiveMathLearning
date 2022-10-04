import matplotlib
from PyQt5.QtWidgets import QSizePolicy

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

__all__ = ["MplCanvas"]


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=1):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        # self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        super(MplCanvas, self).__init__(fig)
