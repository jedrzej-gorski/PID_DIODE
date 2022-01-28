from PyQt5.QtWidgets import QApplication, QMessageBox, QSplitter, QTableView, QMainWindow, QFrame, QGridLayout, \
    QLineEdit, QFormLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QFileInfo, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtGui import QDoubleValidator
import sys
import pid
import ast

class GUIApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("simulation_data.db")

        if not self.db.open():
            self.QMessageBox.critical(None, "Symulator Diody - Error!", "Database Error: %s" % self.db.lastError().databaseText(),)
            sys.exit(1)

        # Create the application's window
        self.win = QMainWindow()
        self.win.setWindowTitle("Symulator diody")
        self.splitter = QSplitter()
        self.sql_model_1 = QSqlTableModel()
        self.sql_model_1.setTable("diodes_tb")
        self.sql_model_1.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.sql_model_1.select()
        self.sql_model_2 = QSqlTableModel()
        self.sql_model_2.setTable("environments_tb")
        self.sql_model_2.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.sql_model_2.select()
        self.sql_model_3 = QSqlTableModel()
        self.sql_model_3.setTable("resistors_tb")
        self.sql_model_3.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.sql_model_3.select()
        self.table_model_1 = QTableView()
        self.table_model_1.setModel(self.sql_model_1)
        self.table_model_2 = QTableView()
        self.table_model_2.setModel(self.sql_model_2)
        self.table_model_1.setEditTriggers(QTableView.NoEditTriggers)
        self.table_model_2.setEditTriggers(QTableView.NoEditTriggers)
        self.table_model_3 = QTableView()
        self.table_model_3.setModel(self.sql_model_3)
        self.table_model_3.setEditTriggers(QTableView.NoEditTriggers)
        self.splitter.addWidget(self.table_model_1)
        self.splitter.addWidget(self.table_model_2)
        self.splitter.addWidget(self.table_model_3)

        self.ui_frame = QFrame()
        self.ui_frame.resize(150, 150)
        self.diode_textbox = QLineEdit()
        self.diode_textbox.setAlignment(Qt.AlignRight)
        self.env_textbox = QLineEdit()
        self.env_textbox.setAlignment(Qt.AlignRight)
        self.res_textbox = QLineEdit()
        self.res_textbox.setAlignment(Qt.AlignRight)
        self.time_textbox = QLineEdit()
        self.time_textbox.setAlignment(Qt.AlignRight)
        self.setpoint_textbox = QLineEdit()
        self.setpoint_textbox.setAlignment(Qt.AlignRight)
        self.simulation_button = QPushButton("Rozpocznij symulację")
        self.simulation_button.clicked.connect(self.start_simulation)
        self.main_layout = QFormLayout()
        self.main_layout.addRow("Wybrana dioda", self.diode_textbox)
        self.main_layout.addRow("Wybrane środowisko", self.env_textbox)
        self.main_layout.addRow("Wybrany rezystor", self.res_textbox)
        self.main_layout.addRow("Czas symulacji", self.time_textbox)
        self.main_layout.addRow("Docelowe natężenie oświetlenia", self.setpoint_textbox)
        self.main_layout.addRow(self.simulation_button)
        self.ui_frame.setLayout(self.main_layout)

        self.add_diode_frame = QFrame()
        self.add_diode_layout = QFormLayout()
        self.diode_name_textbox = QLineEdit()
        self.diode_name_textbox.setAlignment(Qt.AlignRight)
        self.diode_coeff_textbox = QLineEdit()
        self.diode_coeff_textbox.setAlignment(Qt.AlignRight)
        self.diode_coeff_textbox.setValidator(QDoubleValidator())
        self.diode_offset_textbox = QLineEdit()
        self.diode_offset_textbox.setAlignment(Qt.AlignRight)
        self.diode_offset_textbox.setValidator(QDoubleValidator())
        self.diode_l_textbox = QLineEdit()
        self.diode_l_textbox.setAlignment(Qt.AlignRight)
        self.diode_l_textbox.setValidator(QDoubleValidator())
        self.diode_h_textbox = QLineEdit()
        self.diode_h_textbox.setAlignment(Qt.AlignRight)
        self.diode_h_textbox.setValidator(QDoubleValidator())
        self.diode_current_textbox = QLineEdit()
        self.diode_current_textbox.setAlignment(Qt.AlignRight)
        self.diode_current_textbox.setValidator(QDoubleValidator())
        self.diode_button = QPushButton("Dodaj diodę")
        self.diode_button.clicked.connect(self.add_diode)
        self.add_diode_layout.addRow("Nazwa nowej diody", self.diode_name_textbox)
        self.add_diode_layout.addRow("Współczynnik liniowy nowej diody", self.diode_coeff_textbox)
        self.add_diode_layout.addRow("Stała b nowej diody", self.diode_offset_textbox)
        self.add_diode_layout.addRow("Początek przedziału liniowego", self.diode_l_textbox)
        self.add_diode_layout.addRow("Koniec przedziału liniowego", self.diode_h_textbox)
        self.add_diode_layout.addRow("Natężenie prądu diody", self.diode_current_textbox)
        self.add_diode_layout.addRow(self.diode_button)
        self.add_diode_frame.setLayout(self.add_diode_layout)

        self.add_env_frame = QFrame()
        self.add_env_layout = QFormLayout()
        self.env_name_textbox = QLineEdit()
        self.env_name_textbox.setAlignment(Qt.AlignRight)
        self.env_expr_textbox = QLineEdit()
        self.env_expr_textbox.setAlignment(Qt.AlignRight)
        self.env_button = QPushButton("Dodaj środowisko")
        self.env_button.clicked.connect(self.add_env)
        self.add_env_layout.addRow("Nazwa nowego środowiska", self.env_name_textbox)
        self.add_env_layout.addRow("Funkcja wyznaczająca natężenie oświetlenia środowiska", self.env_expr_textbox)
        self.add_env_layout.addRow(self.env_button)
        self.add_env_frame.setLayout(self.add_env_layout)

        self.add_res_frame = QFrame()
        self.add_res_layout = QFormLayout()
        self.res_name_textbox = QLineEdit()
        self.res_name_textbox.setAlignment(Qt.AlignRight)
        self.res_val_textbox = QLineEdit()
        self.res_val_textbox.setAlignment(Qt.AlignRight)
        self.res_val_textbox.setValidator(QDoubleValidator())
        self.res_button = QPushButton("Dodaj rezystor")
        self.res_button.clicked.connect(self.add_res)
        self.add_res_layout.addRow("Nazwa nowego rezystora", self.res_name_textbox)
        self.add_res_layout.addRow("Wartość rezystancji nowego rezystora", self.res_val_textbox)
        self.add_res_layout.addRow(self.res_button)
        self.add_res_frame.setLayout(self.add_res_layout)

        self.final_frame = QFrame()
        self.final_layout = QGridLayout()
        self.final_layout.addWidget(self.splitter, 0, 1, 1, 3)
        self.final_layout.addWidget(self.ui_frame, 0, 0, 2, 1)
        self.final_layout.addWidget(self.add_diode_frame, 1, 1, 1, 1)
        self.final_layout.addWidget(self.add_env_frame, 1, 2, 1, 1)
        self.final_layout.addWidget(self.add_res_frame, 1, 3, 1, 1)
        self.final_frame.setLayout(self.final_layout)

        self.win.setCentralWidget(self.final_frame)
        self.win.show()

        self.graph_splitter = QSplitter()
        self.graph_splitter.setWindowTitle("Wykresy")
        self.view0 = QWebEngineView()
        self.view1 = QWebEngineView()
        self.view2 = QWebEngineView()

        sys.exit(self.app.exec_())
    def start_simulation(self):
        if (self.diode_textbox.text() == "" or self.env_textbox.text() == "" or self.res_textbox.text() == "" or
                self.time_textbox.text() == "" or float(self.time_textbox.text()) == 0.0 or
                float(self.setpoint_textbox.text()) == 0.0 or self.setpoint_textbox.text() == ""):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Błąd! Puste wartości.")
            msg.setInformativeText("Upewnij się, że pola nie są puste.")
            msg.setWindowTitle("Komunikat o błędzie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        diodequery = QSqlQuery()
        diodequery.prepare("SELECT * FROM diodes_tb where diode_name=:declared_name")
        diodequery.bindValue(":declared_name", self.diode_textbox.text())
        if not diodequery.exec():
            print("SELECT FAIL!")
            return
        envquery = QSqlQuery()
        envquery.prepare("SELECT * FROM environments_tb where env_name=:declared_name")
        envquery.bindValue(":declared_name", self.env_textbox.text())
        if not envquery.exec():
            print("SELECT FAIL!")
            return
        resquery = QSqlQuery()
        resquery.prepare("SELECT * FROM resistors_tb where res_name=:declared_name")
        resquery.bindValue(":declared_name", self.res_textbox.text())
        if not resquery.exec():
            print("SELECT FAIL!")
            return
        if not diodequery.next() or not envquery.next() or not resquery.next():
            print("REKORD NIEZNALEZIONY!")
            return
        diode_data = [diodequery.value(x) for x in range(2, 7)]
        env_data = envquery.value(2)
        res_data = resquery.value(2)
        controller = pid.PID(diode_data, env_data, res_data, float(self.time_textbox.text()), float(self.setpoint_textbox.text()))
        controller.run_pid()

        path0 = QFileInfo('linia.html').absoluteFilePath()
        path1 = QFileInfo('linia1.html').absoluteFilePath()
        path2 = QFileInfo('linia2.html').absoluteFilePath()

        self.graph_splitter = QSplitter()
        self.graph_splitter.setWindowTitle("Wykresy")
        self.view0 = QWebEngineView()
        self.view1 = QWebEngineView()
        self.view2 = QWebEngineView()
        self.view0.setUrl(QUrl.fromLocalFile(path0))
        self.view1.setUrl(QUrl.fromLocalFile(path1))
        self.view2.setUrl(QUrl.fromLocalFile(path2))
        self.graph_splitter.addWidget(self.view0)
        self.graph_splitter.addWidget(self.view1)
        self.graph_splitter.addWidget(self.view2)
        self.graph_splitter.show()


    def add_diode(self):
        if (self.diode_name_textbox.text() == "" or self.diode_coeff_textbox.text() == "" or
                self.diode_offset_textbox.text() == "" or self.diode_l_textbox.text() == "" or
                self.diode_h_textbox.text() == "" or self.diode_current_textbox.text() == ""):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Błąd! Puste wartości.")
            msg.setInformativeText("Upewnij się, że pola nie są puste.")
            msg.setWindowTitle("Komunikat o błędzie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if float(self.diode_l_textbox.text()) >= float(self.diode_h_textbox.text()):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Błąd! Lewy koniec przedziału napięcia liniowego ma wartość większą od prawego.")
            msg.setInformativeText("Upewnij się, że poprawnie wpisałeś/aś wartości.")
            msg.setWindowTitle("Komunikat o błędzie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if float(self.diode_l_textbox.text()) * float(self.diode_coeff_textbox.text()) + float(self.diode_offset_textbox.text()) != 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Błąd! Wartość natężenia dla początku przedziału liniowego nie jest równa 0!")
            msg.setInformativeText("Upewnij się, że współczynnik a * początek przedziału = -współczynnik b.")
            msg.setWindowTitle("Komunikat o błędzie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if float(self.diode_l_textbox.text()) < 0 or float(self.diode_h_textbox.text()) < 0 or float(self.diode_current_textbox()) <= 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Błąd! Wartości napięć nie mogą być ujemne i wartość natężenia musi być dodatnia!")
            msg.setInformativeText("Upewnij się, że poprawnie wpisałeś/aś wartości.")
            msg.setWindowTitle("Komunikat o błędzie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        exists = QSqlQuery()
        exists.prepare("SELECT * FROM diodes_tb WHERE diode_name=:new_name")
        exists.bindValue(":new_name", self.diode_name_textbox.text())
        if not exists.exec():
            print("SELECT FAILED!")
            return
        existsDiode = exists.next()
        if (existsDiode):
            print("Row already exists")
        else:
            new_record = self.sql_model_1.record()
            new_record.setValue("diode_name", self.diode_name_textbox.text())
            new_record.setValue("diode_coeff", self.diode_coeff_textbox.text())
            new_record.setValue("diode_low_voltage", self.diode_l_textbox.text())
            new_record.setValue("diode_high_voltage", self.diode_h_textbox.text())
            new_record.setValue("diode_coeff_offset", self.diode_offset_textbox.text())
            new_record.setValue("diode_forward_current", self.diode_current_textbox.text())
            if self.sql_model_1.insertRecord(-1, new_record):
                print("Rows inserted")
            self.sql_model_1.select()
    def add_env(self):
        if self.env_name_textbox.text() == "" or self.env_expr_textbox.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Błąd! Puste wartości.")
            msg.setInformativeText("Upewnij się, że pola nie są puste.")
            msg.setWindowTitle("Komunikat o błędzie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if not self.parse_expression():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Błąd! Niepoprawne wyrażenie.")
            msg.setInformativeText("Upewnij się, że jako zmiennej używasz x i, że wyrażenia są poprawnie sformułowane.")
            msg.setWindowTitle("Komunikat o błędzie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        exists = QSqlQuery()
        exists.prepare("SELECT * FROM environments_tb WHERE env_name=:new_name")
        exists.bindValue(":new_name", self.env_name_textbox.text())
        if not exists.exec():
            print("SELECT FAILED!")
            return
        existsEnv = exists.next()
        if (existsEnv):
            print("Row already exists")
        else:
            new_record = self.sql_model_2.record()
            new_record.setValue("env_name", self.env_name_textbox.text())
            new_record.setValue("env_func", self.env_expr_textbox.text())
            if self.sql_model_2.insertRecord(-1, new_record):
                print("Rows inserted")
            self.sql_model_2.select()


    def parse_expression(self):
        expr_iter = iter(self.env_expr_textbox.text())
        for character in expr_iter:
            if character.isalpha() and character != "x" and character != "(" and character != ")":
                if character == "s":
                    if next(expr_iter, None) == "i" and next(expr_iter, None) == "n" and next(expr_iter, None) == "(":
                        continue
                    else:
                        return False
                elif character == "c":
                    if next(expr_iter, None) == "o" and next(expr_iter, None) == "s" and next(expr_iter, None) == "(":
                        continue
                    else:
                        return False
                else:
                    return False
        try:
            ast.parse(self.env_expr_textbox.text())
        except SyntaxError:
            return False
        return True


    def add_res(self):
        if self.res_name_textbox.text() == "" or self.res_val_textbox.text() == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Błąd! Puste wartości.")
            msg.setInformativeText("Upewnij się, że pola nie są puste.")
            msg.setWindowTitle("Komunikat o błędzie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if float(self.res_val_textbox.text()) <= 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Błąd! Niedodatnia wartość rezystancji.")
            msg.setInformativeText("Upewnij się, że poprawnie wpisałeś/aś wartości.")
            msg.setWindowTitle("Komunikat o błędzie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        exists = QSqlQuery()
        exists.prepare("SELECT * FROM resistors_tb WHERE res_name=:new_name")
        exists.bindValue(":new_name", self.res_name_textbox.text())
        if not exists.exec():
            print("SELECT FAILED!")
            return
        existsRes = exists.next()
        if (existsRes):
            print("Row already exists")
        else:
            new_record = self.sql_model_3.record()
            new_record.setValue("res_name", self.res_name_textbox.text())
            new_record.setValue("res_value", self.res_val_textbox.text())
            if self.sql_model_3.insertRecord(-1, new_record):
                print("Rows inserted")
            self.sql_model_3.select()
