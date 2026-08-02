from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt5.QtGui import QIcon

from calculator.Calculator import Calculator


class CalculatorController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.group_anim = None
        self.window_anim = None
        self.panel_anim = None
        uic.loadUi("resource/ui/calculator.ui", self)
        self.setWindowIcon(QIcon("resource/ui/img/calculator.png"))
        self.calculator = Calculator()
        self.expressionInput.returnPressed.connect(self.on_equal_click)
        self.calculateButton.clicked.connect(self.on_equal_click)
        self.clearButton.clicked.connect(self.on_clear)
        for btn in self.mathGroup.findChildren(QtWidgets.QPushButton):
            btn.clicked.connect(self.on_button_click)
        for btn in self.trigGroup.findChildren(QtWidgets.QPushButton):
            btn.clicked.connect(self.on_button_click)
        for btn in self.constGroup.findChildren(QtWidgets.QPushButton):
            btn.clicked.connect(self.on_button_click)
        self.extraButtonsPanel.setMaximumHeight(0)
        self.panel_expanded = False
        self.togglePanelButton.clicked.connect(self.animate_extra_panel)
        self.saveVarButton.clicked.connect(self.add_expression_in_variable_click)
        self.delMyCreateExpression.clicked.connect(self.clear_my_expression)

    def on_button_click(self):
        """Вызывается при нажатии мышкой на кнопки операций и функций."""
        button = self.sender()
        if button:
            self.expressionInput.insert(button.text())
            self.expressionInput.setFocus()

    def on_equal_click(self):
        """Вызывается при нажатии на Enter или кнопкой 'Вычислить'."""
        current_text = self.expressionInput.text()
        self.calculator.set_expression(current_text)
        result, history_expression, opn_expression = self.calculator.evaluate()
        self.expressionInput.setText(result)
        self.resultDisplay.setText(result)
        self.opnDisplay.setText(opn_expression)
        self.insert_text_history_in_begin(history_expression)

    def insert_text_history_in_begin(self, history_expression):
        """Записать арифметическое выражение в начало истории вычислений"""
        cursor = self.historyEdit.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.historyEdit.setTextCursor(cursor)
        self.historyEdit.insertPlainText(history_expression + "\n")

    def on_clear(self):
        """Очистка выражения"""
        self.expressionInput.clear()

    def animate_extra_panel(self):
        """Синхронная анимация раскрытия панели и увеличения высоты окна"""
        panel_height = 100
        self.panel_anim = QPropertyAnimation(self.extraButtonsPanel, b"maximumHeight")
        self.panel_anim.setDuration(300)
        self.panel_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.window_anim = QPropertyAnimation(self, b"geometry")
        self.window_anim.setDuration(300)
        self.window_anim.setEasingCurve(QEasingCurve.InOutQuad)
        if self.panel_expanded:
            self.panel_anim.setStartValue(panel_height)
            self.panel_anim.setEndValue(0)
            self.window_anim.setStartValue(self.geometry())
            self.window_anim.setEndValue(self.geometry().adjusted(0, 0, 0, -panel_height))
            self.togglePanelButton.setText("Дополнительные функции [v]")
            self.panel_expanded = False
        else:
            self.panel_anim.setStartValue(0)
            self.panel_anim.setEndValue(panel_height)
            self.window_anim.setStartValue(self.geometry())
            self.window_anim.setEndValue(self.geometry().adjusted(0, 0, 0, panel_height))
            self.togglePanelButton.setText("Скрыть функции [^]")
            self.panel_expanded = True
        self.group_anim = QParallelAnimationGroup()
        self.group_anim.addAnimation(self.panel_anim)
        self.group_anim.addAnimation(self.window_anim)
        self.group_anim.start()

    def add_expression_in_variable_click(self):
        """Добавляет пользовательские переменные/выражения"""
        variable = self.variableInput.text()
        evaluation = self.evalInput.text()
        if not variable or not evaluation:
            self.statusbar.showMessage("Заполните оба поля!", 3000)
            return
        if variable in self.calculator.user_expression:
            self.insert_text_history_in_begin("Данная переменная уже создана")
            return
        if self.calculator.save_variable_opn(variable, evaluation):
            final_value = self.calculator.user_expression[variable]
            self.insert_text_history_in_begin(f"Переменная: {variable} = {final_value} (исх: {evaluation})")
            self.statusbar.showMessage(f"Переменная {variable} успешно сохранена!", 3000)
            self.variableInput.clear()
            self.evalInput.clear()
        else:
            self.insert_text_history_in_begin("Ошибка: недопустимое имя или ошибка в выражении")

    def clear_my_expression(self):
        """Очищает словарь с пользовательскими переменными/выражениями"""
        self.calculator.user_expression.clear()
        self.variableInput.clear()
        self.evalInput.clear()
        self.insert_text_history_in_begin("Созданные переменные удалены")
        self.statusbar.showMessage(f"Созданные переменные удалены", 3000)