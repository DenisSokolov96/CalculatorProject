from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotWindow(QDialog):
    """Отдельное всплывающее окно для полноэкранного отображения графика"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Визуализация графика функции")
        self.setWindowIcon(QIcon("resource/ui/img/calculator.png"))
        self.resize(750, 500)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("background-color: #f8f9fa; border: none; max-height: 30px;")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

    def draw_plot(self, x_array, y_masked, expr_title, min_x, max_x, line_color="#3498db"):
        """Метод для инкапсуляции отрисовки графика внутри самого окна"""
        self.ax.clear()
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.ax.plot(x_array, y_masked, color=line_color, linewidth=2, label=f"y = {expr_title}")
        self.ax.legend(loc="upper right")
        self.ax.set_xlim(min_x, max_x)
        self.ax.set_title(f"График функции {expr_title}", fontsize=11, weight='bold')
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
