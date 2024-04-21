import sys
# pip install pygame
import pygame
import time
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QMenuBar, QMenu, QSplashScreen, QMessageBox, QInputDialog, QGridLayout, QDialog

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect, QMediaFormat
from PyQt6.QtCore import Qt, QSize, QUrl, QTimer
from PyQt6.QtGui import QPixmap, QFont, QKeyEvent


#include <QMediaContent>


app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        # allows calls Database from self.main.database & UDP Server calls from self.main.udp_server
        self.main = backend
        self.setWindowTitle("Photon | Team 16")
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.setupUI()
        self.setMinimumSize(800, 600)
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.players_array = []

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
        print("Playing " + track)
        filepath = "assets/tracks/" + track
        self.player.mediaStatusChanged.connect(self.update_position)
        self.player.setSource(QUrl.fromLocalFile(filepath))

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
        self.addPlayerButton.clicked.connect(lambda: self.save_on_enter(self.players_array))

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
        self.deleteGameButton.clicked.connect(lambda: self.delete_all_players(self.players_array))

        # Add button layout to outer layout
        outerLayout.addLayout(buttonLayout2, stretch=0)

        # Set the outer layout to be the central widget's layout
        self.centralwidget.setLayout(outerLayout)

        # Set status bar
        self.setStatusBar(None)

    def codename_add_player(self):
        self.main.database.addPlayer(int(self.id_input.text()), self.codename_input.text())

    def save_on_enter(self, players_array):
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

                
                if foundPlayer["playerName"] is not None:
                    self.codename_input.setText(foundPlayer["playerName"])
                    self.equipment_id_input.setEnabled(True)
                elif self.codename_input.text() == "":
                    print("INPUT CODENAME")
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

                        # Create player info dictionary
                        player_info = {
                            "id": id_text,
                            "codename": self.codename_input.text(),
                            "equipment_id": equipment_id_value
                        }

                        # Check if the player already exists in the players_array
                        if any(player["id"] == id_text for player in players_array):
                            print("Player already exists.")
                            self.id_input.clear()
                            self.codename_input.clear()
                            self.equipment_id_input.clear()
                        else:
                            # Add the player to the appropriate layout based on equipment ID
                            if equipment_id_value % 2 == 1:
                                # Add player to red team layout 
                                players_array.append(player_info)
                                self.add_player_to_red_team(player_info)

                                print(players_array)  # test

                                self.id_input.clear()
                                self.codename_input.clear()
                                self.equipment_id_input.clear()
                            else:
                                # Add player to green team layout
                                players_array.append(player_info)
                                self.add_player_to_green_team(player_info)

                                print(players_array) # test

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
        id = player_info["id"]
        codename = player_info["codename"]
        equipment_id = player_info["equipment_id"]

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
        id = player_info["id"]
        codename = player_info["codename"]
        equipment_id = player_info["equipment_id"]

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
            self.gameActionUI(self.players_array)
        elif event.key() == Qt.Key.Key_F12:
            self.delete_all_players(self.players_array)
        if event.key() == Qt.Key.Key_Return:
            self.save_on_enter(self.players_array)

    def delete_all_players(self, players_array):
        players_array.clear()  # Clear the players_array
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
                            return

    
    def gameActionUI(self):
        self.setVisible(False)
        self.countdown()
        self.setVisible(True)
        # Clear the current central widget
        self.takeCentralWidget()
        self.play_music()

        # Create a new central widget for the game action screen
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        gameActionLayout = QVBoxLayout(self.centralwidget)

        # Set up layouts
        redScoreLayout = self.setupRedScoreLayout(self.players_array)
        greenScoreLayout = self.setupGreenScoreLayout(self.players_array)
        killFeedLayout = self.setupKillFeedLayout()

        # Add backgrounds and layouts
        self.killFeedBackground = QFrame()  # frame is the leftmost red background picture
        self.killFeedBackground.setStyleSheet("background-color: blue;")
        self.killFeedBackground.setContentsMargins(0, 20, 0,
                                                   20)  # To compensate for the table margins (Left, Up, Right, Down)
        self.killFeedBackground.setLayout(killFeedLayout)

        self.redScoreBackground = QFrame()  # frame is the leftmost red background picture
        self.redScoreBackground.setStyleSheet("background-color: black;")
        self.redScoreBackground.setContentsMargins(0, 0, 0,
                                                   0)  # To compensate for the table margins (Left, Up, Right, Down)
        self.redScoreBackground.setLayout(redScoreLayout)

        self.greenScoreBackground = QFrame()  # frame is the leftmost red background picture
        self.greenScoreBackground.setStyleSheet("background-color: black;")
        self.greenScoreBackground.setContentsMargins(0, 0, 0,
                                                     0)  # To compensate for the table margins (Left, Up, Right, Down)
        self.greenScoreBackground.setLayout(greenScoreLayout)

        scoreLayout = QHBoxLayout()
        scoreLayout.addWidget(self.redScoreBackground)
        scoreLayout.addWidget(self.greenScoreBackground)

        gameActionLayout.addLayout(scoreLayout)
        gameActionLayout.addWidget(self.killFeedBackground)

    def setupRedScoreLayout(self, players_array):
        redTeamLayout = QGridLayout()

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
        redTeamLayout.addWidget(self.teamTitle, 0, 5)  # Span the title over 3 columns for better centering

        # Column Headers
        self.redUserID = QLabel("CODENAME:")
        self.redUserID.setFont(font)
        self.redUserID.setStyleSheet("color: red; background-color: transparent;")
        self.redUserID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        redTeamLayout.addWidget(self.redUserID, 1, 2)

        self.redScore = QLabel("Score:")
        self.redScore.setFont(font)
        self.redScore.setStyleSheet("color: red; background-color: transparent;")
        self.redScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        redTeamLayout.addWidget(self.redScore, 1, 8)

        
        # Add players to the layout
        for i, player in enumerate(players_array, start=2):
            if player["equipment_id"] % 2 == 1:
                playerNameLabel = QLabel(player["codename"])
                playerNameLabel.setFont(userFont)
                playerNameLabel.setStyleSheet("color: red; background-color: transparent;")
                playerNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                redTeamLayout.addWidget(playerNameLabel, i, 2)

                playerScoreLabel = QLabel("0")  # Replace with actual score retrieval
                playerScoreLabel.setFont(userFont)
                playerScoreLabel.setStyleSheet("color: red; background-color: transparent;")
                playerScoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                redTeamLayout.addWidget(playerScoreLabel, i, 8)
            else:
                continue
            
        return redTeamLayout

    ######GREEN######
    def setupGreenScoreLayout(self, players_array):
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
        greenTeamLayout.addWidget(self.greenteamTitle, 0, 5)  # Title at the top, spanning columns as needed

        # Column Headers
        self.greenUserID = QLabel("CODENAME:")
        self.greenUserID.setFont(font)
        self.greenUserID.setStyleSheet("color: green; background-color: transparent;")
        self.greenUserID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        greenTeamLayout.addWidget(self.greenUserID, 1, 2)  # UserID header in the second column

        self.greenScore = QLabel("Score:")
        self.greenScore.setFont(font)
        self.greenScore.setStyleSheet("color: green; background-color: transparent;")
        self.greenScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        greenTeamLayout.addWidget(self.greenScore, 1, 8)  # Score header in the eighth column

        # Add players to the layout
        for i, player in enumerate(players_array, start=2):
            if player["equipment_id"] % 2 == 1:
                continue
            else:
                playerNameLabel = QLabel(player["codename"])  # Accessing the 'codename' key
                playerNameLabel.setFont(userFont)
                playerNameLabel.setStyleSheet("color: green; background-color: transparent;")
                playerNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                greenTeamLayout.addWidget(playerNameLabel, i, 2)  # Player names in the second column

                playerScoreLabel = QLabel("0")  # Placeholder for the score
                playerScoreLabel.setFont(userFont)
                playerScoreLabel.setStyleSheet("color: green; background-color: transparent;")
                playerScoreLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                greenTeamLayout.addWidget(playerScoreLabel, i, 8)  # Player scores in the eighth column

        return greenTeamLayout

    def setupKillFeedLayout(self):
        killfeedVerLayout = QVBoxLayout()
        killfeedHorLayout = QHBoxLayout()

        killfeedHorLayout.setContentsMargins(20, 0, 70, 0)  # Margin spacers: (Left, Up, Right, Down)
        killfeedHorLayout.addStretch(1)

        killfeedVerLayout.addLayout(killfeedHorLayout)

        # print("HiFeed")
        return killfeedVerLayout

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
        for i in range(2, -1, -1):
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
            # show for 3 seconds then close splashscreen
            time.sleep(1)
        pygame.quit()
        # Transmit game Start Code
        self.main.udp_server.transmit_message("202")
        return 1

    def save_players_ui(self, team_color):
        try:
            if team_color == "red":
                for id_input, codename_input, equipment_id_input in self.players_red:
                    player_id_text = id_input.text().strip()
                    if player_id_text:
                        try:
                            db_search = self.main.database.getPlayer(int(player_id_text))
                            if not db_search['needsAdding']:
                                codename_input.setText(str(db_search['playerName']))
                                equipment_id_input.setFocus()  # Set focus to equipment ID input
                            else:
                                dialog = QInputDialog(self)
                                dialog.setInputMode(QInputDialog.InputMode.TextInput)
                                dialog.setLabelText("Enter Codename:")
                                dialog.setWindowTitle("Player Information")
                                dialog.setOkButtonText("Next")
                                dialog.setCancelButtonText("Cancel")
                                dialog.setStyleSheet("color: white;")
                                result = dialog.exec()
                                if result == QDialog.DialogCode.Accepted:
                                    codename = dialog.textValue()
                                    dialog.setLabelText("Enter Equipment ID:")
                                    result = dialog.exec()
                                    if result == QDialog.DialogCode.Accepted:
                                        equipment_id = dialog.textValue()
                                        codename_input.setText(codename)
                                        equipment_id_input.setText(equipment_id)
                                        # add player to database
                                        self.main.database.addPlayer(int(player_id_text), codename)
                            player = self.main.Player(int(id_input.text().strip()), codename_input.text().strip(),
                                                    int(equipment_id_input.text().strip()))
                            added = self.main.add_team_player(player, "red")
                            if not added:
                                print("save_players_ui: Player already added")
                            equipment_id = equipment_id_input.text().strip()
                            self.main.udp_server.transmit_message(equipment_id)
                        except ValueError:
                            print("Player ID must be an integer.")
            elif team_color == "green":
                for id_input, codename_input, equipment_id_input in self.players_green:
                    player_id_text = id_input.text().strip()
                    if player_id_text:
                        try:
                            db_search = self.main.database.getPlayer(int(player_id_text))
                            if not db_search['needsAdding']:
                                codename_input.setText(str(db_search['playerName']))
                                equipment_id_input.setFocus()  # Set focus to equipment ID input
                            else:
                                dialog = QInputDialog(self)
                                dialog.setInputMode(QInputDialog.InputMode.TextInput)
                                dialog.setLabelText("Enter Codename:")
                                dialog.setWindowTitle("Player Information")
                                dialog.setOkButtonText("Next")
                                dialog.setCancelButtonText("Cancel")
                                dialog.setStyleSheet("color: white;")
                                result = dialog.exec()
                                if result == QDialog.DialogCode.Accepted:
                                    codename = dialog.textValue()
                                    dialog.setLabelText("Enter Equipment ID:")
                                    result = dialog.exec()
                                    if result == QDialog.DialogCode.Accepted:
                                        equipment_id = dialog.textValue()
                                        codename_input.setText(codename)
                                        equipment_id_input.setText(equipment_id)
                                        # add player to database
                                        self.main.database.addPlayer(int(player_id_text), codename)
                            player = self.main.Player(int(id_input.text().strip()), codename_input.text().strip(),
                                                    int(equipment_id_input.text().strip()))
                            added = self.main.add_team_player(player, "green")
                            if not added:
                                print("save_players_ui: Player already added")
                            equipment_id = equipment_id_input.text().strip()
                            self.main.udp_server.transmit_message(equipment_id)
                        except ValueError:
                            print("Player ID must be an integer.")
        except Exception as e:
            print("Error occurred while saving data to Supabase:", e)


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

