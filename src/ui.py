import sys
# pip install pygame
import pygame
import time
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QMenuBar, QMenu, QSplashScreen, QMessageBox, QInputDialog, QGridLayout, QDialog, QScrollArea, QTextEdit

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect, QMediaFormat
from PyQt6.QtCore import Qt, QSize, QTimer, QUrl
from PyQt6.QtGui import QPixmap, QFont, QKeyEvent, QTextCursor, QPalette


#include <QMediaContent>


app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        # allows calls Database from self.main.database & UDP Server calls from self.main.udp_server
        self.main = backend
        self.main.ui = self # sets file interconnect
        self.setWindowTitle("Photon | Team 16")
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.setupUI()
        self.setMinimumSize(800, 600)
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.red_player_labels = []
        self.green_player_labels = []
        self.killFeedText = QTextEdit()
        self.redTeamScoreLabel = QLabel()
        self.greenTeamScoreLabel = QLabel()
        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self.flash_label)
        self.flash_timer.setInterval(500)  # Flash duration in milliseconds
        self.flash_state = False
        self.media_status_connected = False
        self.scoresExist = False
        self.gameActive = False

    def update_position(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.player.setPosition(20000)
            self.player.play()

    def play_music(self):
        self.player.setAudioOutput(self.audioOutput)
        trackNo = random.randint(1, 8)
        if trackNo == 5:
            trackNo = 4
        track = "Track0" + str(trackNo) + ".wav"
        print("play_music")
        print("Playing " + track)
        filepath = "assets/tracks/" + track

        # Check if there's an existing connection before disconnecting
        if self.media_status_connected:
            self.player.mediaStatusChanged.disconnect(self.update_position)

        self.player.setSource(QUrl.fromLocalFile(filepath))
        self.player.mediaStatusChanged.connect(self.update_position)
        self.media_status_connected = True


    def setupUI(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Sets up outer layout... Superimposes the buttons on top of the player entry layout
        outerLayout = QVBoxLayout(self.centralwidget)

        # Sets up Player entry (inner) layout
        playerEntryLayout = QHBoxLayout()

        # Sets left background then superimposes Red Team's Layout
        self.frame = QFrame()  # frame is the leftmost red background picture
        self.frame.setStyleSheet(
            "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(120, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));")
        self.frame.setContentsMargins(20, 0, 100, 0)  # To compensate for the table margins (Left, Up, Right, Down)

        redTeamLayout = self.setupRedTeam()
        self.frame.setLayout(redTeamLayout)

        # Sets right background then superimposes Green Team's Layout
        self.frame_2 = QFrame()  # frame_2 is the rightmost green background picture
        self.frame_2.setStyleSheet(
            "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.495074, fy:0.494, stop:0 rgba(0, 107, 24, 255), stop:1 rgba(0, 0, 0, 255));")
        self.frame_2.setContentsMargins(100, 0, 20, 0)  # To compensate for the table margins (Left, Up, Right, Down)

        greenTeamLayout = self.setupGreenTeam()
        self.frame_2.setLayout(greenTeamLayout)

        # Add team layouts to player entry layout
        playerEntryLayout.addWidget(self.frame)
        playerEntryLayout.addWidget(self.frame_2)

        # Add player entry layout to outer layout
        outerLayout.addLayout(playerEntryLayout)

        # Create a layout for input boxes
        inputLayout = QHBoxLayout()

        # Create the QLineEdit widgets
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ENTER ID")
        self.id_input.setStyleSheet("background-color: black; color: white;")
        self.id_input.setFixedSize(100, 50)

        self.codename_input = QLineEdit()
        self.codename_input.setEnabled(False)
        self.codename_input.setPlaceholderText("ENTER CODENAME")
        self.codename_input.setStyleSheet("background-color: black; color: white;")
        self.codename_input.setFixedSize(100, 50)

        self.equipment_id_input = QLineEdit()
        self.equipment_id_input.setEnabled(False)
        self.equipment_id_input.setPlaceholderText("ENTER EQUIPMENT ID")
        self.equipment_id_input.setStyleSheet("background-color: black; color: white;")
        self.equipment_id_input.setFixedSize(100, 50)

        # Add input widgets to input layout
        inputLayout.addWidget(self.id_input)
        inputLayout.addWidget(self.codename_input)
        inputLayout.addWidget(self.equipment_id_input)

        # Add input layout to outer layout
        outerLayout.addLayout(inputLayout)  # Add input layout to outer layout before setting its margins

        # Set margins for inputLayout
        inputLayout.setContentsMargins(20, 0, 20, 20)

        # Create a layout for buttons
        buttonLayout = QHBoxLayout()

        # Add buttons to button layout
        self.addPlayerButton = QPushButton("Add Player")
        self.addPlayerButton.setStyleSheet("border: 1px solid white; border-radius: 15px; color: white;")
        self.addPlayerButton.setFixedSize(100, 20)
        buttonLayout.addWidget(self.addPlayerButton)
        self.addPlayerButton.clicked.connect(lambda: self.save_on_enter())

        # Add button layout to outer layout
        outerLayout.addLayout(buttonLayout, stretch=0)

        # Create a layout for buttons
        buttonLayout2 = QHBoxLayout()

        # Add buttons to button layout
        self.startGameButton = QPushButton("Start Game")
        self.startGameButton.setStyleSheet("border: 1px solid white; border-radius: 15px; color: white;")
        self.startGameButton.setFixedSize(100, 20)
        buttonLayout2.addWidget(self.startGameButton)
        self.startGameButton.clicked.connect(self.gameActionUI)

        self.deleteGameButton = QPushButton("Delete Game")
        self.deleteGameButton.setStyleSheet("border: 1px solid white; border-radius: 15px; color: white;")
        self.deleteGameButton.setFixedSize(100, 20)
        buttonLayout2.addWidget(self.deleteGameButton)
        self.deleteGameButton.clicked.connect(lambda: self.delete_all_players())

        # Add button layout to outer layout
        outerLayout.addLayout(buttonLayout2, stretch=0)

        # Set the outer layout to be the central widget's layout
        self.centralwidget.setLayout(outerLayout)

        # Set status bar
        self.setStatusBar(None)

        #fill with teams? assuming there are is already teams
        # Add the player to the appropriate layout based on equipment ID
        for player in self.main.red_team:
            self.add_player_to_red_team(player)
            player.score = 0
            player.hit_base = False
        for player in self.main.green_team:
            self.add_player_to_green_team(player)
            player.score = 0
            player.hit_base = False



    def codename_add_player(self):
        self.main.database.addPlayer(int(self.id_input.text()), self.codename_input.text())


    def alert_box(self, message):
        alert = QDialog(self)
        alert.setWindowTitle("ALERT")
        alert.layout = QVBoxLayout()
        alert.layout.addWidget(QLabel(message))
        alert.setStyleSheet("font-size: 30px; color: white;")
        alert.setLayout(alert.layout)
        alert.exec()

    def save_on_enter(self):
        # Get the input text from id_input and equipment_id_input widgets
        self.id_input.setEnabled(True)
        self.codename_input.setEnabled(False)
        self.equipment_id_input.setEnabled(False)

        id_text = self.id_input.text()
        equipment_id_text = self.equipment_id_input.text()

        # Check if the ID input text is not empty
        if id_text:
            try:
                # Convert the ID input text to an integer
                id_value = int(id_text)

                # Check if a player with the given ID exists in the database
                foundPlayer = self.main.database.getPlayer(id_value)


                if not foundPlayer["needsAdding"]:
                    self.codename_input.setText(foundPlayer["playerName"])
                    self.equipment_id_input.setEnabled(True)
                elif self.codename_input.text() == "":
                    self.alert_box("ID Not Found! Please Enter a Codename!")
                    self.codename_input.setEnabled(True)
                else:
                    self.codename_add_player()
                    self.equipment_id_input.setEnabled(True)
                    print("ENTER EQUIPMENT ID")


                # Check if equipment ID input text is not empty
                if equipment_id_text:
                    try:
                        # Convert the equipment ID input text to an integer
                        equipment_id_value = int(equipment_id_text)

                        #create Player Object
                        player = self.main.Player(id_text, self.codename_input.text(), equipment_id_value)
                        #self.main.udp_server.transmit_message(equipment_id_text)

                        # Add the player to the appropriate layout based on equipment ID
                        if equipment_id_value % 2 == 1:
                            # Add player to red team layout
                            self.main.add_team_player(player, "red")
                            self.add_player_to_red_team(player)

                            self.id_input.clear()
                            self.codename_input.clear()
                            self.equipment_id_input.clear()
                        else:
                            # Add player to green team layout
                            self.main.add_team_player(player, "green")
                            self.add_player_to_green_team(player)

                            self.id_input.clear()
                            self.codename_input.clear()
                            self.equipment_id_input.clear()
                    except ValueError:
                        # Handle the case where the equipment ID input text cannot be converted to an integer
                        print("Invalid equipment ID. Please enter a valid integer equipment ID.")
            except ValueError:
                # Handle the case where the ID input text cannot be converted to an integer
                print("Invalid input. Please enter a valid integer ID.")
        else:
            # Handle the case where the ID input text is empty
            print("ID input is empty.")

    def add_player_to_red_team(self, player_info):
        # Extract player information
        id = player_info.player_id
        codename = player_info.codename
        equipment_id = player_info.equipment_id

        # Find the next empty box in the red team layout
        player_layout = self.find_next_empty_box(self.frame.layout())  # Access the layout of self.frame

        if player_layout:
            # Get the QLabel widgets representing ID, codename, and equipment ID
            id_label, codename_label, equipment_id_label = player_layout

            # Update the QLabel widgets with player information
            id_label.setText(id)
            codename_label.setText(codename)
            equipment_id_label.setText(str(equipment_id))

    def add_player_to_green_team(self, player_info):
        # Extract player information
        id = player_info.player_id
        codename = player_info.codename
        equipment_id = player_info.equipment_id

        # Find the next empty box in the green team layout
        player_layout = self.find_next_empty_box(self.frame_2.layout())  # Access the layout of self.frame_2

        if player_layout:
            # Get the QLabel widgets representing ID, codename, and equipment ID
            id_label, codename_label, equipment_id_label = player_layout

            # Update the QLabel widgets with player information
            id_label.setText(id)
            codename_label.setText(codename)
            equipment_id_label.setText(str(equipment_id))

    def find_next_empty_box(self, team_layout):
        # Iterate through the children of the team layout to find the next empty box
        for i in range(team_layout.count()):
            player_layout_item = team_layout.itemAt(i)
            if player_layout_item and player_layout_item.layout():
                # Access the QHBoxLayout representing the player layout
                player_layout = player_layout_item.layout()

                # Check if the layout contains enough items
                if player_layout.count() >= 4:  # Assuming we need at least 4 items (including QLabel and QWidgets)
                    # Access the QLabel widgets representing ID, codename, and equipment ID
                    id_label = player_layout.itemAt(1).widget()  # Assuming the ID label is at index 1
                    codename_label = player_layout.itemAt(2).widget()  # Assuming the codename label is at index 2
                    equipment_id_label = player_layout.itemAt(3).widget()  # Assuming the equipment ID label is at index 3
                    if id_label and id_label.text() == "":
                        return id_label, codename_label, equipment_id_label
        return None



    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_F5:
            self.gameActionUI()
        elif event.key() == Qt.Key.Key_F12:
            self.delete_all_players()
        if event.key() == Qt.Key.Key_Return:
            self.save_on_enter()

    def delete_all_players(self):
        self.main.clear_teams()  # Clear the players_array
        self.clear_player_layout(self.frame.layout())
        self.clear_player_layout(self.frame_2.layout())

    def clear_player_layout(self, team_layout):
        # Iterate through the children of the team layout to find the next empty box
        for i in range(team_layout.count()):
            player_layout_item = team_layout.itemAt(i)
            if player_layout_item and player_layout_item.layout():
                # Access the QHBoxLayout representing the player layout
                player_layout = player_layout_item.layout()

                # Check if the layout contains enough items
                if player_layout.count() >= 4:  # Assuming we need at least 4 items (including QLabel and QWidgets)
                    # Access the QLabel widgets representing ID, codename, and equipment ID
                    id_label_item = player_layout.itemAt(1)  # Assuming the ID label is at index 1
                    codename_label_item = player_layout.itemAt(2)  # Assuming the codename label is at index 2
                    equipment_id_label_item = player_layout.itemAt(3)  # Assuming the equipment ID label is at index 3

                    # Check if layout items are not None before accessing widgets
                    if id_label_item and codename_label_item and equipment_id_label_item:
                        id_label = id_label_item.widget()
                        codename_label = codename_label_item.widget()
                        equipment_id_label = equipment_id_label_item.widget()

                        # Check if labels are not None before accessing text
                        if id_label and codename_label and equipment_id_label:
                            # Clear the text of the labels
                            id_label.setText("")
                            codename_label.setText("")
                            equipment_id_label.setText("")

    # Start of Timer Methods
    def update_timer_display(self):
        self.remaining_time = self.calculate_remaining_time()  # Implement this method to calculate remaining time
        self.timer_label.setText(f"{self.remaining_time}")

    def calculate_remaining_time(self):
        elapsed_seconds = self.elapsed_time()
        remaining_seconds = max(0,6*60 - elapsed_seconds)#FIXC
        minutes = int(remaining_seconds // 60)
        seconds = int(remaining_seconds % 60)
        self.update_scores()
        if int(remaining_seconds) <= 0:
            self.timerOut()
        return f"{minutes:01} : {seconds:02}"

    def update_scores(self):
        # red team
        redTeamScore = 0
        greenTeamScore = 0
        current_label = 0
        if len(self.red_player_labels) > 0:
            for player in self.main.red_team:
                self.red_player_labels[current_label][0].setText(player.codename)
                self.red_player_labels[current_label][1].setText(str(player.score))
                if player.hit_base:
                    self.red_player_labels[current_label][2].show()
                else:
                    self.red_player_labels[current_label][2].hide()
                current_label += 1
                redTeamScore += player.score
        if not hasattr(self, 'redTeamScoreLabel') or not isinstance(self.redTeamScoreLabel, QLabel):
            self.redTeamScoreLabel = QLabel()
            self.redTeamScoreLabel.setFont(QFont("Arial", 8))
            self.redTeamScoreLabel.setStyleSheet("color: red; background-color: transparent; font-size: 20px;")
            self.redTeamScoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.redTeamScoreLabel.setText(str(redTeamScore))
        else:
            self.redTeamScoreLabel.setText(str(redTeamScore))
        # green team
        current_label = 0
        if len(self.green_player_labels) > 0:
            for player in self.main.green_team:
                self.green_player_labels[current_label][0].setText(player.codename)
                self.green_player_labels[current_label][1].setText(str(player.score))
                if player.hit_base:
                    self.green_player_labels[current_label][2].show()
                else:
                    self.green_player_labels[current_label][2].hide()
                current_label += 1
                greenTeamScore += player.score
        self.greenTeamScoreLabel.setText(str(greenTeamScore))
        if not self.flash_timer.isActive():
            self.flash_timer.start()

    def flash_label(self):
        # Toggle the flash state
        self.flash_state = not self.flash_state

        # Determine which team's score label should flash white
        if self.scoresExist:
            redTeamScore = int(self.redTeamScoreLabel.text())
            greenTeamScore = int(self.greenTeamScoreLabel.text())
            if redTeamScore > greenTeamScore:
                if self.flash_state:
                    self.redTeamScoreLabel.setStyleSheet("color: white; background-color: transparent; font-size: 20px;")
                    self.greenTeamScoreLabel.setStyleSheet("color: green; background-color: transparent; font-size: 20px;")
                else:
                    self.redTeamScoreLabel.setStyleSheet("color: red; background-color: transparent; font-size: 20px;")
                    self.greenTeamScoreLabel.setStyleSheet("color: green; background-color: transparent; font-size: 20px;")
            elif greenTeamScore > redTeamScore:
                if self.flash_state:
                    self.greenTeamScoreLabel.setStyleSheet("color: white; background-color: transparent; font-size: 20px;")
                    self.redTeamScoreLabel.setStyleSheet("color: red; background-color: transparent; font-size: 20px;")
                else:
                    self.greenTeamScoreLabel.setStyleSheet("color: green; background-color: transparent; font-size: 20px;")
                    self.redTeamScoreLabel.setStyleSheet("color: red; background-color: transparent; font-size: 20px;")
            else:
                # Reset the style if scores are equal
                self.redTeamScoreLabel.setStyleSheet("color: red; background-color: transparent; font-size: 20px;")
                self.greenTeamScoreLabel.setStyleSheet("color: green; background-color: transparent; font-size: 20px;")


    def elapsed_time(self):
        current_time = time.time()
        elapsed_seconds = current_time - self.start_time
        return elapsed_seconds

    #End of Timer Method
    #Game End message after timer runs out, Call Jonathons button
    def timerOut(self):
        self.timer.stop()
        self.flash_timer.stop()
        self.scoresExist = False
        self.gameActive = False
        for i in range(3):
            self.main.udp_server.transmit_message("221")
         #button return declaration
        player_entry_button = QPushButton("Return to player entry screen", self.centralwidget)
        player_entry_button.clicked.connect(self.player_entry_button)
        player_entry_button.setStyleSheet("""color: white;background-color: black;border: 2px solid white;border-radius: 5px;padding: 5px;""")
        #layout
        self.gameActionLayout.addWidget(player_entry_button)


    def player_entry_button(self):
        self.red_player_labels.clear()
        self.green_player_labels.clear()
        self.player.stop()
        self.setupUI()



    def gameActionUI(self):
        for player in self.main.red_team:
            print("Transmitting Red Team Player")
            self.main.udp_server.transmit_message(str(player.equipment_id))
        for player in self.main.green_team:
            print("Transmitting Green Team Player")
            self.main.udp_server.transmit_message(str(player.equipment_id))
        #####REMOVE-LATER######
        self.main.sort_teams()
        self.setVisible(False)
        self.countdown()
        self.setVisible(True)
        # Clear the current central widget
        self.takeCentralWidget()
        #self.play_music()
        # Create a new central widget for the game action screen
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.gameActionLayout = QVBoxLayout(self.centralwidget)
        # Add Timer Layout
        self.gameActionLayout.addWidget(self.timerLayout())
        # Setup for score displays
        self.redScoreBackground = QFrame()
        self.redScoreBackground.setStyleSheet("background-color: black;")
        self.redScoreLayout = self.setupRedScoreLayout()
        self.redScoreBackground.setLayout(self.redScoreLayout)
        self.greenScoreBackground = QFrame()
        self.greenScoreBackground.setStyleSheet("background-color: black;")
        self.greenScoreLayout = self.setupGreenScoreLayout()
        self.greenScoreBackground.setLayout(self.greenScoreLayout)
        self.scoreLayout = QHBoxLayout()
        self.scoreLayout.addWidget(self.redScoreBackground)
        self.scoreLayout.addWidget(self.greenScoreBackground)
        self.gameActionLayout.addLayout(self.scoreLayout)
        '''
        if not hasattr(self, 'killFeedBackground') or not isinstance(self.killFeedBackground, QFrame):
            self.killFeedBackground = QFrame()
            self.killFeedBackground.setStyleSheet("background-color: black;")
            self.killFeedBackground.setContentsMargins(0, 20, 0, 20)
            killFeedLayout = QHBoxLayout(self.killFeedBackground)
            scrollArea = self.setupKillFeedLayout()
            killFeedLayout.addWidget(scrollArea)
            self.gameActionLayout.addWidget(self.killFeedBackground)
        '''


        self.killFeedBackground = QFrame()
        self.killFeedBackground.setStyleSheet("background-color: blue;")
        self.killFeedBackground.setContentsMargins(0, 20, 0, 20)
        killFeedLayout = QHBoxLayout(self.killFeedBackground)
        scrollArea = self.setupKillFeedLayout()
        killFeedLayout.addWidget(scrollArea)
        self.gameActionLayout.addWidget(self.killFeedBackground)
        self.scoresExist = True
        self.gameActive = True

    def timerLayout(self):
        # Timer, Can be moved to seperate method
        self.start_time = time.time()
        self.timer_label = QLabel("Timer")
        # Initialize the timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer_display)
        self.timer.start(1000)

        # Create and format the timer label
        self.timer_label = QLabel("Timer")
        self.timer_label.setStyleSheet("""color: white;background-color: black;font-size: 40px;""")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align center horizontally

        return self.timer_label



    def setupRedScoreLayout(self):
        redTeamLayout = QGridLayout()
        redTeamLayout.setSpacing(0)  # Eliminate spacing between cells
        redTeamLayout.setContentsMargins(0, 0, 0, 0)  # Eliminate margins within the layout
        # Fonts
        font = QFont("Arial", 10, QFont.Weight.Bold)
        userFont = QFont("Arial", 8)
        titleFont = QFont("Arial", 14, QFont.Weight.Bold)

        for i in range(1,15):
            for j in range(1,10):
                redTeamLayout.addWidget(QLabel(" "),i,j)

        # Red Team Title
        self.teamTitle = QLabel("RED TEAM")
        self.teamTitle.setFont(titleFont)
        self.teamTitle.setStyleSheet("color: red; background-color: transparent;")
        self.teamTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        redTeamLayout.addWidget(self.teamTitle, 1, 5)  # Span the title over 3 columns for better centering

        # Column Headers
        self.redUserID = QLabel("CODENAME:")
        self.redUserID.setFont(font)
        self.redUserID.setStyleSheet("color: red; background-color: transparent;")
        self.redUserID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        redTeamLayout.addWidget(self.redUserID, 2, 2)

        self.redScore = QLabel("SCORE:")
        self.redScore.setFont(font)
        self.redScore.setStyleSheet("color: red; background-color: transparent;")
        self.redScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        redTeamLayout.addWidget(self.redScore, 2, 8)

        i=0
        # Add players to the layout
        for player in self.main.red_team:
            playerNameLabel = QLabel(player.codename)
            playerNameLabel.setFont(userFont)
            playerNameLabel.setStyleSheet("color: red; background-color: transparent;")
            playerNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            redTeamLayout.addWidget(playerNameLabel, i+3, 2)

            playerScoreLabel = QLabel(str(player.score))  # Replace with actual score retrieval
            playerScoreLabel.setFont(userFont)
            playerScoreLabel.setStyleSheet("color: red; background-color: transparent;")
            playerScoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            redTeamLayout.addWidget(playerScoreLabel, i+3, 8)

            baseHitLabel = QLabel()  # Replace with actual score retrieval
            baseHitLabel.setFont(userFont)
            baseHitLabel.setStyleSheet("color: red; background-color: transparent;")
            baseHitLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
            baseHitLabel.setPixmap(QPixmap("assets/splashscreen_game_sounds/pictures/redb.png").scaled(12, 18))
            redTeamLayout.addWidget(baseHitLabel, i + 3, 1)
            baseHitLabel.hide()
            self.red_player_labels.append((playerNameLabel, playerScoreLabel, baseHitLabel))
            i+=1

        if not hasattr(self, 'redTeamScoreLabel') or not isinstance(self.redTeamScoreLabel, QLabel):
            self.redTeamScoreLabel = QLabel()
            self.redTeamScoreLabel.setFont(QFont("Arial", 8))
            self.redTeamScoreLabel.setStyleSheet("color: red; background-color: transparent; font-size: 20px;")
            self.redTeamScoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.redTeamLabel.setText("0")
            redTeamLayout.addWidget(self.redTeamScoreLabel, 20, 8)
            return redTeamLayout

        self.redTeamScoreLabel = QLabel()
        self.redTeamScoreLabel.setFont(QFont("Arial", 8))
        self.redTeamScoreLabel.setStyleSheet("color: red; background-color: transparent; font-size: 20px;")
        self.redTeamScoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        redTeamLayout.addWidget(self.redTeamScoreLabel, 20, 8)
        self.redTeamScoreLabel.setText("0")
        return redTeamLayout

    ######GREEN######
    def setupGreenScoreLayout(self):
        greenTeamLayout = QGridLayout()

        # Fonts
        font = QFont("Arial", 10, QFont.Weight.Bold)
        userFont = QFont("Arial", 8)
        titleFont = QFont("Arial", 14, QFont.Weight.Bold)

        for i in range(1,15):
            for j in range(1,10):
                greenTeamLayout.addWidget(QLabel(" "),i,j)


        # Green Team Title
        self.greenteamTitle = QLabel("GREEN TEAM")
        self.greenteamTitle.setFont(titleFont)
        self.greenteamTitle.setStyleSheet("color: green; background-color: transparent;")
        self.greenteamTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        greenTeamLayout.addWidget(self.greenteamTitle, 1, 5)  # Title at the top, spanning columns as needed

        # Column Headers
        self.greenUserID = QLabel("CODENAME:")
        self.greenUserID.setFont(font)
        self.greenUserID.setStyleSheet("color: green; background-color: transparent;")
        self.greenUserID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        greenTeamLayout.addWidget(self.greenUserID, 2, 2)  # UserID header in the second column

        self.greenScore = QLabel("SCORE:")
        self.greenScore.setFont(font)
        self.greenScore.setStyleSheet("color: green; background-color: transparent;")
        self.greenScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        greenTeamLayout.addWidget(self.greenScore, 2, 8)  # Score header in the eighth column

        # Add players to the layout
        i=0
        for player in self.main.green_team:
            playerNameLabel = QLabel(player.codename)  # Accessing the 'codename' key
            playerNameLabel.setFont(userFont)
            playerNameLabel.setStyleSheet("color: green; background-color: transparent;")
            playerNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            greenTeamLayout.addWidget(playerNameLabel, i+3, 2)  # Player names in the second column

            playerScoreLabel = QLabel(str(player.score))  # Placeholder for the score
            playerScoreLabel.setFont(userFont)
            playerScoreLabel.setStyleSheet("color: green; background-color: transparent;")
            playerScoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            greenTeamLayout.addWidget(playerScoreLabel, i+3, 8)  # Player scores in the eighth column

            baseHitLabel = QLabel()  # Replace with actual score retrieval
            baseHitLabel.setFont(userFont)
            baseHitLabel.setStyleSheet("color: green; background-color: transparent;")
            baseHitLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
            baseHitLabel.setPixmap(QPixmap("assets/splashscreen_game_sounds/pictures/greenb.png").scaled(10, 16))
            greenTeamLayout.addWidget(baseHitLabel, i + 3, 1)
            baseHitLabel.hide()
            self.green_player_labels.append((playerNameLabel, playerScoreLabel, baseHitLabel))
            i+=1

        self.greenTeamScoreLabel = QLabel()
        self.greenTeamScoreLabel.setFont(QFont("Arial", 8))
        self.greenTeamScoreLabel.setStyleSheet("color: green; background-color: transparent; font-size: 20px;")
        self.greenTeamScoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        greenTeamLayout.addWidget(self.greenTeamScoreLabel, 20, 8)
        self.greenTeamScoreLabel.setText("0")
        return greenTeamLayout

    def setupKillFeedLayout(self):
        scrollArea = QScrollArea(self.centralwidget)
        scrollArea.show()
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setStyleSheet("background: transparent;")

        killFeedLayout = QGridLayout()
        scrollAreaWidgetContents = QWidget()
        scrollAreaWidgetContents.setLayout(killFeedLayout)

        if not hasattr(self, 'killFeedText') or not isinstance(self.killFeedText, QTextEdit):
            print("Creating new QTextEdit")
            self.killFeedText = QTextEdit()
            self.killFeedText.setReadOnly(True)
            self.killFeedText.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
            self.killFeedText.setStyleSheet("color: white; background: blue; font-size: 30px; font-weight: bold;")
            scrollArea.setWidget(self.killFeedText)
            return scrollArea
        else:
            print("Using existing QTextEdit like the lying bitch I am")

        self.killFeedText = QTextEdit()
        self.killFeedText.setReadOnly(True)
        self.killFeedText.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.killFeedText.setStyleSheet("color: white; background: blue; font-size: 30px; font-weight: bold;")
        scrollArea.setWidget(self.killFeedText)
        return scrollArea

    def append_killFeed(self, text):
        if self.gameActive:
            self.killFeedText.append(text)
            self.killFeedText.ensureCursorVisible()

    def setupRedTeam(self):
        # Red Team Layout
        redTeamVerLayout = QVBoxLayout()
        redTeamHeaderLayout = QHBoxLayout()

        redTeamVerLayout.setContentsMargins(70, 0, 20, 0)  # Margin spacers: (Left, Up, Right, Down)
        redTeamVerLayout.addStretch(1)

        self.red_team_label = QLabel("RED TEAM")
        self.red_team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_team_label.setStyleSheet("color: white; background-color: transparent;")
        redTeamVerLayout.addWidget(self.red_team_label)

        # Red Team Headers
        self.red_id_header = QLabel("ID")
        self.red_id_header.setFixedWidth(50)
        self.red_id_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_id_header.setStyleSheet("color: white; background-color: transparent;")

        self.red_codename_header = QLabel("Codename")
        self.red_codename_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_codename_header.setStyleSheet("color: white; background-color: transparent;")

        self.red_eqid_header = QLabel("Eq. ID")
        self.red_eqid_header.setFixedWidth(50)
        self.red_eqid_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_eqid_header.setStyleSheet("color: white; background-color: transparent;")

        # Adds headers to the header layout
        redTeamHeaderLayout.addWidget(self.red_id_header)
        redTeamHeaderLayout.addStretch(1)
        redTeamHeaderLayout.addWidget(self.red_codename_header)
        redTeamHeaderLayout.addStretch(1)
        redTeamHeaderLayout.addWidget(self.red_eqid_header)

        # Add the header layout to the team layout
        redTeamVerLayout.addLayout(redTeamHeaderLayout)

        # this for loop creates the tables for red team
        for i in range(15):
            playerLayout = QHBoxLayout()
            # Create the player number label
            player_number = QLabel(str(i + 1))
            player_number.setStyleSheet("color: white; background-color: transparent;")
            player_number.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            player_number.setFixedWidth(
                30)  # This need to be here to ensure numbers past 10 don't push the boxes to the right

            id_input = QLabel()
            id_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            codename_input = QLabel()
            codename_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            equipment_id_input = QLabel()
            equipment_id_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            # Add input fields to the player layout. The 2nd parameters are the stretch factors to size the boxes properly.
            playerLayout.addWidget(player_number)
            playerLayout.addWidget(id_input, 1)
            playerLayout.addWidget(codename_input, 3)
            playerLayout.addWidget(equipment_id_input, 1)

            # Add the player layout to the team layout
            redTeamVerLayout.addLayout(playerLayout)

        redTeamVerLayout.addStretch(1)

        return redTeamVerLayout

    def setupGreenTeam(self):
        # Green Team Layout
        greenTeamVerLayout = QVBoxLayout()
        greenTeamHeaderLayout = QHBoxLayout()

        greenTeamVerLayout.setContentsMargins(20, 0, 70, 0)  # Margin spacers: (Left, Up, Right, Downn)
        greenTeamVerLayout.addStretch(1)

        self.green_team_label = QLabel("GREEN TEAM")
        self.green_team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_team_label.setStyleSheet("color: white; background-color: transparent;")
        greenTeamVerLayout.addWidget(self.green_team_label)

        # Green Team Headers
        self.green_id_header = QLabel("ID")
        self.green_id_header.setFixedWidth(50)
        self.green_id_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_id_header.setStyleSheet("color: white; background-color: transparent;")

        self.green_codename_header = QLabel("Codename")
        self.green_codename_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_codename_header.setStyleSheet("color: white; background-color: transparent;")

        self.green_eqid_header = QLabel("Eq. ID")
        self.green_eqid_header.setFixedWidth(50)
        self.green_eqid_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_eqid_header.setStyleSheet("color: white; background-color: transparent;")

        # Adds headers to the header layout
        greenTeamHeaderLayout.addWidget(self.green_id_header)
        greenTeamHeaderLayout.addStretch(1)
        greenTeamHeaderLayout.addWidget(self.green_codename_header)
        greenTeamHeaderLayout.addStretch(1)
        greenTeamHeaderLayout.addWidget(self.green_eqid_header)

        # Add the header layout to the team layout
        greenTeamVerLayout.addLayout(greenTeamHeaderLayout)

        # this for loop creates the tables for green team
        self.players_green = []
        for i in range(15):
            playerLayout = QHBoxLayout()

            # Create the player number label
            player_number = QLabel(str(i + 1))
            player_number.setStyleSheet("color: white; background-color: transparent;")
            player_number.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            player_number.setFixedWidth(
                30)  # This need to be here to ensure numbers past 10 don't push the boxes to the right

            id_input = QLabel()
            id_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            codename_input = QLabel()
            codename_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            equipment_id_input = QLabel()
            equipment_id_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            # Add input fields to the player layout. The 2nd parameters are the stretch factors to size the boxes properly.
            playerLayout.addWidget(player_number)
            playerLayout.addWidget(id_input, 1)
            playerLayout.addWidget(codename_input, 3)
            playerLayout.addWidget(equipment_id_input, 1)

            # Add the player layout to the team layout
            greenTeamVerLayout.addLayout(playerLayout)

            self.players_green.append((id_input, codename_input, equipment_id_input))

        greenTeamVerLayout.addStretch(1)

        return greenTeamVerLayout

    def prompt_player_id(self):
        player_id, ok = QLineEdit.getText("Player ID Prompt", "Enter Player ID:")
        if ok:
            # Logic to handle the player ID input
            try:
                player_id = int(player_id)
                # Continue with the logic after getting the player ID input
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid Player ID (integer).")

    def prompt_equipment_id(self):
        equipment_id, ok = QInputDialog.getText(self, "Equipment ID Prompt", "Enter Equipment ID:")
        if ok:
            try:
                equipment_id = int(equipment_id)
                return equipment_id
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid Equipment ID (integer).")
        return None

    def countdown(self):
        #Show countdown images
        pygame.init()
        # set pygame display size
        splash_display = pygame.display.set_mode((1000, 700))  # width height
        # set splashscreen image and scale to window
        pygame.display.set_caption('Photon Tag - Team 16')
        for i in range(30, -1, -1): #FIX
            filename = 'assets/splashscreen_game_sounds/countdown_images/{}.tif'.format(i)
            countdown_img = pygame.image.load(filename)
            countdown_img = pygame.transform.scale(countdown_img, (1000, 700))
            if i == 15:
                trackNo = random.randint(1, 8)
                if trackNo == 5:
                    trackNo = 4
                track = "Track0" + str(trackNo)
                pygame.mixer.init()
                pygame.mixer.music.load(f"assets/tracks/{track}.wav")
                original_frequency = pygame.mixer.Sound(f"assets/tracks/{track}.wav").get_length()
                new_frequency = int(original_frequency / 4)
                pygame.mixer.music.set_endevent(pygame.USEREVENT)
                pygame.mixer.music.play()  # Play the loaded file
                print("Playing track " + str(trackNo))

            # display splashscreen
            splash_display.blit(countdown_img, (0, 0))
            pygame.display.update()

            # Get the current time in milliseconds
            start_time = pygame.time.get_ticks()
            # Busy-wait loop for one second to try and convince OS that program is still responding
            while pygame.time.get_ticks() - start_time < 1000:
                pygame.event.get()
                pass  # Do nothing, just keep looping

        pygame.quit()
        # Transmit game Start Code
        self.main.udp_server.transmit_message("202")
        return 1



def ui_start(backend):
    # splash_pix = QPixmap('assets/splashscreen_game_sounds/logo.jpg').scaled(QSize(1000, 700), Qt.AspectRatioMode.KeepAspectRatio)
    # splash = QSplashScreen(splash_pix)
    # splash.show()
    # app.processEvents()
    # time.sleep(3)  # Display the splash screen for 3 seconds.
    # splash.close()

    # pygame for splashscreen
    pygame.init()
    # set pygame display size
    splash_display = pygame.display.set_mode((1000, 700))  # width height
    # set splashscreen image and scale to window
    splash_img = pygame.image.load('assets/splashscreen_game_sounds/logo.jpg')
    splash_img = pygame.transform.scale(splash_img, (1000, 700))
    # display splashscreen
    splash_display.blit(splash_img, (0, 0))
    pygame.display.set_caption('Photon Tag - Team 16')
    pygame.display.update()
    # show for 3 seconds then close splashscreen
    time.sleep(3)
    pygame.quit()

    mainWindow = MainWindow(backend)
    mainWindow.resize(1500, 1050)
    mainWindow.show()
    sys.exit(app.exec())