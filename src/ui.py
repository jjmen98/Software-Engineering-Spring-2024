import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFrame, QMenuBar, QMenu, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import supabase


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.supabase_client = supabase.create_client("https://blzwcpdxyfmqngexhskf.supabase.co",
                                                      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJsendjcGR4eWZtcW5nZXhoc2tmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDcyNTEyMTMsImV4cCI6MjAyMjgyNzIxM30.Y78DCDzwlRNW8MVQiVJ4itxl9NdjV99PPa7Q9hh_daI")

        self.setWindowTitle("Photon")
        self.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(340, 0, 131, 31)
        self.label.setText("Edit Current Game")

        # Red Team Label
        self.red_team_label = QLabel(self.centralwidget)
        self.red_team_label.setGeometry(60, 10, 331, 20)
        self.red_team_label.setAlignment(Qt.AlignCenter)
        self.red_team_label.setStyleSheet("color: white; background-color: transparent;")
        self.red_team_label.setText("Red Team")

        # Green Team Label
        self.green_team_label = QLabel(self.centralwidget)
        self.green_team_label.setGeometry(410, 10, 331, 20)
        self.green_team_label.setAlignment(Qt.AlignCenter)
        self.green_team_label.setStyleSheet("color: white; background-color: transparent;")
        self.green_team_label.setText("Green Team")

        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(60, 40, 331, 376)
        self.frame.setStyleSheet(
            "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(120, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(60, 40, 331, 376)
        self.frame.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(120, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.players_red = []
        for i in range(15):
            label = QLabel(self.frame)
            label.setGeometry(10, 25 * i, 20, 20)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; background-color: transparent;")
            label.setText(str(i+1))

            id_input = QLineEdit(self.frame)
            id_input.setGeometry(40, 25 * i, 50, 20)
            id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white;")

            codename_input = QLineEdit(self.frame)
            codename_input.setGeometry(100, 25 * i, 200, 20)
            codename_input.setStyleSheet("color: white; background-color: black; border: 1px solid white;")

            self.players_red.append((id_input, codename_input))

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setGeometry(410, 40, 331, 376)
        self.frame_2.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.495074, fy:0.494, stop:0 rgba(0, 107, 24, 255), stop:1 rgba(0, 0, 0, 255));")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.players_green = []
        for i in range(15):
            label = QLabel(self.frame_2)
            label.setGeometry(10, 25 * i, 20, 20)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; background-color: transparent;")
            label.setText(str(i+1))

            id_input = QLineEdit(self.frame_2)
            id_input.setGeometry(40, 25 * i, 50, 20)
            id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white;")

            codename_input = QLineEdit(self.frame_2)
            codename_input.setGeometry(100, 25 * i, 200, 20)
            codename_input.setStyleSheet("color: white; background-color: black; border: 1px solid white;")

            self.players_green.append((id_input, codename_input))

        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        self.menuPhoton = QMenu(self.menubar)
        self.menuPhoton.setTitle("Photon")

        self.menuTeam_16 = QMenu(self.menubar)
        self.menuTeam_16.setTitle("Team 16")

        self.menubar.addAction(self.menuPhoton.menuAction())
        self.menubar.addAction(self.menuTeam_16.menuAction())

        self.setStatusBar(None)
        self.save_button = QPushButton("Save", self.centralwidget)
        self.save_button.setGeometry(60, 440, 100, 30)
        self.save_button.setStyleSheet("border: 1px solid white;")
        self.save_button.clicked.connect(self.save_data_to_supabase)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateSizes()

    def updateSizes(self):
        window_width = self.centralwidget.width()

        # Update label position to center horizontally
        label_width = 131
        label_height = 31
        label_y = 0
        self.label.setGeometry(int((window_width - label_width) / 2), label_y, label_width, label_height)

        # Update frame sizes
        frame_width = (window_width - 120) / 2
        frame_height = self.centralwidget.height() - 50
        self.frame.setGeometry(60, 40, int(frame_width), int(frame_height))
        self.frame_2.setGeometry(int(window_width / 2) + 10, 40, int(frame_width), int(frame_height))

        # Update save button position
        save_button_width = 100
        save_button_height = 30
        self.save_button.setGeometry(int((window_width - save_button_width) / 2), 500, save_button_width,
                                     save_button_height)

        # Update teams labels position
        self.red_team_label.setGeometry(60, 10, int(frame_width), 20)
        self.green_team_label.setGeometry(int(window_width / 2) + 10, 10, int(frame_width), 20)

        # Update players positions
        for i in range(15):
            label_x = 20
            player_x = label_x + self.players_red[i][0].width() - 35
            self.players_red[i][0].setGeometry(player_x, 25 * i, 50, 20)
            self.players_red[i][1].setGeometry(player_x + 60, 25 * i, 200, 20)

            player_x = label_x + self.players_green[i][0].width() - 20
            self.players_green[i][0].setGeometry(player_x, 25 * i, 50, 20)
            self.players_green[i][1].setGeometry(player_x + 60, 25 * i, 200, 20)

    def save_data_to_supabase(self):
        try:
            for id_input, codename_input in self.players_red:
                player_id_text = id_input.text().strip()
                if player_id_text:
                    try:
                        player_id = int(player_id_text)
                        codename = codename_input.text()
                        # Example table name is 'players'
                        self.supabase_client.table('player').insert({'id': player_id, 'codename': codename}).execute()
                    except ValueError:
                        print("Player ID must be an integer.")
                else:
                    print("ID input is empty")

            for id_input, codename_input in self.players_green:
                player_id_text = id_input.text().strip()
                if player_id_text:
                    try:
                        player_id = int(player_id_text)
                        codename = codename_input.text()
                        # Example table name is 'players'
                        self.supabase_client.table('player').insert({'id': player_id, 'codename': codename}).execute()
                    except ValueError:
                        print("Player ID must be an integer.")
                else:
                    print("ID input is empty")
        except Exception as e:
            print("Error occurred while saving data to Supabase:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1000, 700)
    mainWindow.show()
    sys.exit(app.exec_())
