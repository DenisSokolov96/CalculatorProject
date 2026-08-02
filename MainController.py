import sys

from PyQt5 import QtWidgets

from calculator.CalculatorController import CalculatorController


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setDesktopFileName("calculator")
    window = CalculatorController()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
