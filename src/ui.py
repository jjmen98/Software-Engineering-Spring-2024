# main_window.py
import sys
import time
# pip install PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFrame, QLineEdit, QPushButton, QMenuBar, QMenu, QSplashScreen
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap


class MainWindow(QMainWindow):

    def __init__(self, backend):
        super().__init__()
        self.main = backend

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
        self.red_team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_team_label.setStyleSheet("color: white; background-color: transparent;")
        self.red_team_label.setText("Red Team")

        # Green Team Label
        self.green_team_label = QLabel(self.centralwidget)
        self.green_team_label.setGeometry(410, 10, 331, 20)
        self.green_team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_team_label.setStyleSheet("color: white; background-color: transparent;")
        self.green_team_label.setText("Green Team")

        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(60, 40, 331, 376)
        self.frame.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(120, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));")

        # Adjusted Column Labels for Red Team
        label_y_offset = 35  # Starting Y offset for column labels
        self.red_id_header = QLabel("ID", self.frame)
        self.red_id_header.setGeometry(40, label_y_offset, 50, 20)
        self.red_id_header.setStyleSheet("color: white; background-color: transparent;")

        self.red_codename_header = QLabel("Codename", self.frame)
        self.red_codename_header.setGeometry(100, label_y_offset, 150, 20)
        self.red_codename_header.setStyleSheet("color: white; background-color: transparent;")

        self.red_eqid_header = QLabel("Eq. ID", self.frame)
        self.red_eqid_header.setGeometry(260, label_y_offset, 50, 20)
        self.red_eqid_header.setStyleSheet("color: white; background-color: transparent;")

        input_boxes_start_y = label_y_offset - 35  # Y offset for input boxes, adding a gap
        self.players_red = []
        for i in range(15):
            # Positioning labels and input boxes with spacing
            label = QLabel(self.frame)
            label.setGeometry(10, input_boxes_start_y + (25 * i), 20, 20)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: white; background-color: transparent;")
            label.setText(str(i+1))

            id_input = QLineEdit(self.frame)
            id_input.setGeometry(40, input_boxes_start_y + (25 * i), 50, 20)
            id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            codename_input = QLineEdit(self.frame)
            codename_input.setGeometry(100, input_boxes_start_y + (25 * i), 150, 20)
            codename_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            equipment_id_input = QLineEdit(self.frame)
            equipment_id_input.setGeometry(260, input_boxes_start_y + (25 * i), 50, 20)
            equipment_id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            self.players_red.append((id_input, codename_input, equipment_id_input))

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setGeometry(410, 40, 331, 376)
        self.frame_2.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.495074, fy:0.494, stop:0 rgba(0, 107, 24, 255), stop:1 rgba(0, 0, 0, 255));")

        # Adjusted Column Labels for Green Team
        self.green_id_header = QLabel("ID", self.frame_2)
        self.green_id_header.setGeometry(40, label_y_offset, 50, 20)
        self.green_id_header.setStyleSheet("color: white; background-color: transparent;")

        self.green_codename_header = QLabel("Codename", self.frame_2)
        self.green_codename_header.setGeometry(100, label_y_offset, 150, 20)
        self.green_codename_header.setStyleSheet("color: white; background-color: transparent;")

        self.green_eqid_header = QLabel("Eq. ID", self.frame_2)
        self.green_eqid_header.setGeometry(260, label_y_offset, 50, 20)
        self.green_eqid_header.setStyleSheet("color: white; background-color: transparent;")

        self.players_green = []
        for i in range(15):
            # Positioning labels and input boxes with spacing for Green Team
            label = QLabel(self.frame_2)
            label.setGeometry(10, input_boxes_start_y + (25 * i), 20, 20)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: white; background-color: transparent;")
            label.setText(str(i+1))

            id_input = QLineEdit(self.frame_2)
            id_input.setGeometry(40, input_boxes_start_y + (25 * i), 50, 20)
            id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            codename_input = QLineEdit(self.frame_2)
            codename_input.setGeometry(100, input_boxes_start_y + (25 * i), 150, 20)
            codename_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            equipment_id_input = QLineEdit(self.frame_2)
            equipment_id_input.setGeometry(260, input_boxes_start_y + (25 * i), 50, 20)
            equipment_id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            self.players_green.append((id_input, codename_input, equipment_id_input))

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
        self.save_button.setStyleSheet("border: 1px solid white; border-radius: 15px;")
        self.save_button.clicked.connect(self.save_data_to_supabase)

        #self.setup_udp_sockets()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_sizes()

    def update_sizes(self):
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
        self.save_button.setGeometry(int((window_width - save_button_width) / 2), 500, save_button_width, save_button_height)

        # Update teams labels position
        self.red_team_label.setGeometry(60, 10, int(frame_width), 20)
        self.green_team_label.setGeometry(int(window_width / 2) + 10, 10, int(frame_width), 20)

        # Update players positions
        for i in range(15):
            label_x = 20
            player_x = label_x + self.players_red[i][0].width() - 35
            self.players_red[i][0].setGeometry(player_x, 25 * i, 50, 20)
            self.players_red[i][1].setGeometry(player_x + 60, 25 * i, 150, 20)
            self.players_red[i][2].setGeometry(player_x + 220, 25 * i, 50, 20)

            player_x = label_x + self.players_green[i][0].width() - 20
            self.players_green[i][0].setGeometry(player_x, 25 * i, 50, 20)
            self.players_green[i][1].setGeometry(player_x + 60, 25 * i, 150, 20)
            self.players_green[i][2].setGeometry(player_x + 220, 25 * i, 50, 20)

    def prompt_player_id(self):
        # Logic to prompt for player ID and handle database lookup
        pass

    def prompt_equipment_id(self):
        # Logic to prompt for equipment ID after player ID is entered
        pass

    def save_data_to_supabase(self):
        # Convert input data to Player objects and store them in lists
        self.players_red_objects = []
        self.players_green_objects = []

        try:
            # Handle red team players
            for id_input, codename_input, equipment_id_input in self.players_red:
                player_id_text = id_input.text().strip()
                codename_text = codename_input.text().strip()
                equipment_id_text = equipment_id_input.text().strip()
                if player_id_text and codename_text and equipment_id_text:
                    try:
                        player = self.main.Player(int(player_id_text), codename_text, int(equipment_id_text))
                        self.players_red_objects.append(player)
                        self.main.udp_server.transmit_message(str(player.equipment_id))
                    except ValueError:
                        print("Player ID and Equipment ID must be integers.")

            # Handle green team players
            for id_input, codename_input, equipment_id_input in self.players_green:
                player_id_text = id_input.text().strip()
                codename_text = codename_input.text().strip()
                equipment_id_text = equipment_id_input.text().strip()
                if player_id_text and codename_text and equipment_id_text:
                    try:
                        player = self.main.Player(int(player_id_text), codename_text, int(equipment_id_text))
                        self.players_green_objects.append(player)
                        #self.broadcast_equipment_id(player.equipment_id)
                    except ValueError:
                        print("Player ID and Equipment ID must be integers.")

            # Now send the player objects data to the database
            #self.send_players_to_database()

        except Exception as e:
            print("Error occurred while saving data to Supabase:", e)

def ui_start(backend):
    app = QApplication(sys.argv)
    splash_pix = QPixmap('assets\splashscreen_game_sounds\logo.jpg').scaled(QSize(1000, 700), Qt.AspectRatioMode.KeepAspectRatio)
    splash = QSplashScreen(splash_pix)
    splash.show()
    app.processEvents()
    time.sleep(3)  # Display the splash screen for 3 seconds.
    splash.close()

    main_window = MainWindow(backend)
    main_window.resize(1000, 700)
    main_window.show()
    sys.exit(app.exec())
