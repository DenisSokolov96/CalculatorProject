import sys

from PyQt6 import QtWidgets

from calculator.CalculatorController import CalculatorController


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setDesktopFileName("calculator")
    window = CalculatorController()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
