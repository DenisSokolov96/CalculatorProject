from PyQt6 import QtWidgets, uic, sip
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt6.QtGui import QIcon

from calculator.Calculator import Calculator, ENGINE_EVALUATION
from calculator.utils.CalculationUtils import generate_color
from calculator.utils.PlotWindow import PlotWindow


class CalculatorController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.group_anim = None
        self.window_anim = None
        self.panel_anim = None
        self.opened_plots = []
        uic.loadUi("resource/ui/calculator.ui", self)
        self.setWindowIcon(QIcon("resource/ui/img/calculator.png"))
        self.calculator = Calculator()
        self.engineComboBox.addItems(ENGINE_EVALUATION.values())
        self.engineComboBox.currentIndexChanged.connect(self.on_engine_change)
        self.on_engine_change()
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

        # Настройка боковой панели формул
        self.formulaPanel.setVisible(False)
        self.formulaPanel.setMaximumWidth(0)
        self.formula_panel_expanded = False
        self.toggleFormulaPanelBtn.clicked.connect(self.animate_side_panel)
        self.calcFormulaBtn.clicked.connect(self.on_calculate_formula)
        self.formulaSelectBox.currentIndexChanged.connect(self.update_formula_inputs)
        self.update_formula_inputs()
        self.buildPlotBtn.clicked.connect(self.on_build_plot_click)

    def on_engine_change(self):
        """Вызывается при смене метода решения в QComboBox"""
        engines = list(ENGINE_EVALUATION.keys())
        idx = self.engineComboBox.currentIndex()
        if 0 <= idx < len(engines):
            selected_engine = engines[idx]
            self.calculator.set_engine(selected_engine)
            if selected_engine == "opn":
                self.insert_text_history_in_begin("Выбран режим ОПН")
            else:
                self.insert_text_history_in_begin("Выбран режим вычисления через граф")

    def update_formula_inputs(self):
        """Динамически переключает подсказки полей ввода и видимость в зависимости от выбранной формулы"""
        formula = self.formulaSelectBox.currentText()
        self.paramInput1.clear()
        self.paramInput2.clear()
        self.paramInput3.clear()
        self.paramInput4.clear()
        self.formulaResultOutput.clear()
        if formula == "Формула Бернулли":
            self.paramInput1.setPlaceholderText("n — общее число испытаний")
            self.paramInput2.setPlaceholderText("k — количество успехов")
            self.paramInput3.setPlaceholderText("p — вероятность успеха (0-1)")
            self.paramInput4.setVisible(False)

        elif formula in ["Арифметическая прогрессия", "Геометрическая прогрессия"]:
            self.paramInput1.setPlaceholderText("a1 (или b1) — первый член")
            self.paramInput2.setPlaceholderText("d (или q) — шаг / знаменатель")
            self.paramInput3.setPlaceholderText("n — номер элемента / шагов")
            self.paramInput4.setToolTip("Режим расчета: 1 - найти n-й член, 2 - найти сумму n членов")
            self.paramInput4.setPlaceholderText("мод: 1 или 2")
            self.paramInput4.setVisible(True)

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
        result, history_expression, engine_log = self.calculator.evaluate()
        self.expressionInput.setText(result)
        self.insert_text_history_in_begin(engine_log)
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

    def animate_side_panel(self):
        """Плавное выдвижение боковой панели с принудительным расширением окна вправо"""
        panel_target_width = 300  # Ширина выезжающей панели
        self.side_panel_anim = QPropertyAnimation(self.formulaPanel, b"maximumWidth")
        self.side_panel_anim.setDuration(250)
        self.side_panel_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.side_window_anim = QPropertyAnimation(self, b"geometry")
        self.side_window_anim.setDuration(250)
        self.side_window_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        current_geo = self.geometry()
        if self.formula_panel_expanded:
            self.side_panel_anim.setStartValue(panel_target_width)
            self.side_panel_anim.setEndValue(0)
            self.side_window_anim.setStartValue(current_geo)
            self.side_window_anim.setEndValue(current_geo.adjusted(0, 0, -panel_target_width, 0))
            self.toggleFormulaPanelBtn.setText("»")
            self.formula_panel_expanded = False
            self.side_panel_anim.finished.connect(lambda: self.formulaPanel.setVisible(False))
        else:
            try:
                self.side_panel_anim.finished.disconnect()
            except TypeError:
                pass
            self.formulaPanel.setVisible(True)
            self.side_panel_anim.setStartValue(0)
            self.side_panel_anim.setEndValue(panel_target_width)
            self.side_window_anim.setStartValue(current_geo)
            self.side_window_anim.setEndValue(current_geo.adjusted(0, 0, panel_target_width, 0))
            self.toggleFormulaPanelBtn.setText("«")
            self.formula_panel_expanded = True
        self.side_group_anim = QParallelAnimationGroup()
        self.side_group_anim.addAnimation(self.side_panel_anim)
        self.side_group_anim.addAnimation(self.side_window_anim)
        self.side_group_anim.start()

    def animate_extra_panel(self):
        """Синхронная анимация раскрытия панели и увеличения высоты окна"""
        panel_height = 170
        self.panel_anim = QPropertyAnimation(self.extraButtonsPanel, b"maximumHeight")
        self.panel_anim.setDuration(300)
        self.panel_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.window_anim = QPropertyAnimation(self, b"geometry")
        self.window_anim.setDuration(300)
        self.window_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
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

    def on_calculate_formula(self):
        """Вызывается по нажатию кнопки 'Рассчитать' на панели формул"""
        formula = self.formulaSelectBox.currentText()
        res, history = self.calculator.calculate_formula(
            formula, self.paramInput1.text(), self.paramInput2.text(), self.paramInput3.text(), self.paramInput4.text()
        )
        self.formulaResultOutput.setText(res)
        self.insert_text_history_in_begin(history)

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
        if self.calculator.save_variable(variable, evaluation):
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

    def on_build_plot_click(self):
        """Вызывается при клике на 'Построить график'. Тонкий контроллер."""
        expr = self.expressionInput.text().strip()
        if not expr:
            self.statusbar.showMessage("Введите математическое выражение в главное поле ввода!", 4000)
            return
        try:
            min_x = float(self.plotMinXInput.text()) if self.plotMinXInput.text() else -10.0
            max_x = float(self.plotMaxXInput.text()) if self.plotMaxXInput.text() else 10.0
            if min_x >= max_x:
                self.statusbar.showMessage("Ошибка: Минимум X должен быть меньше Максимума X!", 4000)
                return

            if self.plotStepInput.text():
                step = float(self.plotStepInput.text().replace(",", "."))
                if step <= 0:
                    self.statusbar.showMessage("Ошибка: Шаг должен быть больше 0!", 4000)
                    return
            else:
                step = (max_x - min_x) / 500
        except ValueError:
            self.statusbar.showMessage("Заполняйте поля границ и шага только числами!", 4000)
            return
        try:
            x_array, y_masked = self.calculator.calculate_plot_data(expr, min_x, max_x, step)
        except Exception as e:
            self.statusbar.showMessage(f"Ошибка при расчете точек: {str(e)}", 5000)
            return
        new_plot = PlotWindow()
        new_plot.draw_plot(x_array, y_masked, expr, min_x, max_x, generate_color())
        self.opened_plots = [
            win for win in self.opened_plots
            if not sip.isdeleted(win) and win.isVisible()
        ]
        self.opened_plots.append(new_plot)
        new_plot.show()
        self.statusbar.showMessage("График успешно открыт в отдельном окне", 3000)
