import sys
# pip install pygame
import pygame
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QMenuBar, QMenu, QSplashScreen, QMessageBox, QInputDialog, QGridLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont

app = QApplication(sys.argv)
class MainWindow(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        # allows calls Database from self.main.database & UDP_Server calls from self.main.udp_server
        self.main = backend
        self.setWindowTitle("Photon | Team 16")
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.setupUI()
        self.setMinimumSize(800, 600)

    def setupUI(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Sets up outer layout... Superimposes the buttons ontop of the player entry layout
        # mainLayout = QVBoxLayout(self.centralwidget)

        # Sets up Player entry (inner) layout
        playerEntryLayout = QHBoxLayout(self.centralwidget)

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

        # Adds Background + Team Layouts
        playerEntryLayout.addWidget(self.frame, 1)
        playerEntryLayout.addWidget(self.frame_2, 1)

        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        self.menuPhoton = QMenu(self.menubar)
        self.menuPhoton.setTitle("Photon")

        self.menuTeam_16 = QMenu(self.menubar)
        self.menuTeam_16.setTitle("Team 16")

        self.menubar.addAction(self.menuPhoton.menuAction())
        self.menubar.addAction(self.menuTeam_16.menuAction())

        self.startGameButton = QPushButton("Start Game")
        self.startGameButton.setStyleSheet("border: 1px solid white; border-radius: 15px; color: white;")
        self.startGameButton.setFixedSize(50, 20)
        playerEntryLayout.addWidget(self.startGameButton)
        self.startGameButton.clicked.connect(self.gameActionUI)
        self.setStatusBar(None)

        self.deleteGameButton = QPushButton("Delete Game")
        self.deleteGameButton.setStyleSheet("border: 1px solid white; border-radius: 15px; color: white;")
        self.deleteGameButton.setFixedSize(50, 20)
        playerEntryLayout.addWidget(self.deleteGameButton)
        self.deleteGameButton.clicked.connect(self.delete_all_players)
        self.setStatusBar(None)

    def delete_all_players(self):
       self.clear_player_entries() 

    def clear_player_entries(self):
        # Implement logic to clear player entries from the UI
        # For example:
        for id_input, codename_input, equipment_id_input in self.players_red:
            id_input.clear()
            codename_input.clear()
            equipment_id_input.clear()

        for id_input, codename_input, equipment_id_input in self.players_green:
            id_input.clear()
            codename_input.clear()
            equipment_id_input.clear() 
       
           
    def gameActionUI(self):
        self.setVisible(False)
        #self.countdown()
        self.setVisible(True)
         # Clear the current central widget
        self.takeCentralWidget()
        
        # Create a new central widget for the game action screen
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        gameActionLayout = QVBoxLayout(self.centralwidget)
        killFeedLayout = QHBoxLayout(self.centralwidget)
        scoreLayout = QHBoxLayout()
        
        self.killFeedBackground = QFrame()   #frame is the leftmost red background picture
        self.killFeedBackground.setStyleSheet("background-color: blue;")
        self.killFeedBackground.setContentsMargins(0, 20, 0, 20) # To compensate for the table margins (Left, Up, Right, Down)
        
        self.redScoreBackground = QFrame()   #frame is the leftmost red background picture
        self.redScoreBackground.setStyleSheet("background-color: black;")
        self.redScoreBackground.setContentsMargins(0, 0, 0, 0) # To compensate for the table margins (Left, Up, Right, Down)
        
        self.greenScoreBackground = QFrame()   #frame is the leftmost red background picture
        self.greenScoreBackground.setStyleSheet("background-color: black;")
        self.greenScoreBackground.setContentsMargins(0, 0, 0, 0) # To compensate for the table margins (Left, Up, Right, Down)
        
        redScoreLayout = self.setupRedScoreLayout()
        greenScoreLayout = self.setupGreenScoreLayout()
        killFeedLayout = self.setupKillFeedLayout()

        self.killFeedBackground.setLayout(killFeedLayout)
        self.redScoreBackground.setLayout(redScoreLayout)
        self.greenScoreBackground.setLayout(greenScoreLayout)

        scoreLayout.addWidget(self.redScoreBackground)
        scoreLayout.addWidget(self.greenScoreBackground)

        gameActionLayout.addLayout(scoreLayout)
        gameActionLayout.addWidget(self.killFeedBackground)



    def setupRedScoreLayout(self):
        #####RED#####
        redTeamLayout = QGridLayout()

        font = QFont("Arial", 10, QFont.Weight.Bold)
        userFont = QFont("Arial", 8)
        titleFont = QFont("Arial", 14, QFont.Weight.Bold)
        # Red Team User IDs
        self.redUserID = QLabel("UserID")
        self.redUserID.setFont(font)
        self.redUserID.setStyleSheet("color: red; background-color: transparent;")
        self.teamTitle = QLabel("RED TEAM")
        self.teamTitle.setFont(titleFont)
        self.teamTitle.setStyleSheet("color: red; background-color: transparent;")

        # Red Team Score
        self.redScore = QLabel("Score")
        self.redScore.setFont(font)
        self.redScore.setStyleSheet("color: red; background-color: transparent;") 

        self.testUser = QLabel("Test User")
        self.testUser.setFont(userFont)
        self.testUser.setStyleSheet("color: red; background-color: transparent;")

        self.testScore = QLabel("Test Score")
        self.testScore.setFont(userFont)
        self.testScore.setStyleSheet("color: red; background-color: transparent;")

        for i in range(1,10):
            for j in range(1,10):
                redTeamLayout.addWidget(QLabel(" "),i,j)

        self.redUserID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.teamTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.redScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.testUser.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.testScore.setAlignment(Qt.AlignmentFlag.AlignCenter)

        redTeamLayout.addWidget(self.redUserID, 1, 2)
        redTeamLayout.addWidget(self.teamTitle, 0, 5)
        redTeamLayout.addWidget(self.redScore, 1, 8)
        redTeamLayout.addWidget(self.testUser, 2, 2)
        redTeamLayout.addWidget(self.testScore, 2, 8)
        #redTeamLayout.addWidget(self.initializeGrid, 9, 14)
        #redTeamVerLayout.addWidget(self.teamTitle)

        return redTeamLayout

    ######GREEN######
    def setupGreenScoreLayout(self):
        #####green#####
        greenTeamLayout = QGridLayout()

        font = QFont("Arial", 10, QFont.Weight.Bold)
        userFont = QFont("Arial", 8)
        titleFont = QFont("Arial", 14, QFont.Weight.Bold)
        # green Team User IDs
        self.greenUserID = QLabel("UserID")
        self.greenUserID.setFont(font)
        self.greenUserID.setStyleSheet("color: green; background-color: transparent;")
        self.greenteamTitle = QLabel("GREEN TEAM")
        self.greenteamTitle.setFont(titleFont)
        self.greenteamTitle.setStyleSheet("color: green; background-color: transparent;")

        # green Team Score
        self.greenScore = QLabel("Score")
        self.greenScore.setFont(font)
        self.greenScore.setStyleSheet("color: green; background-color: transparent;") 

        self.greentestUser = QLabel("Test User")
        self.greentestUser.setFont(userFont)
        self.greentestUser.setStyleSheet("color: green; background-color: transparent;")

        self.greentestScore = QLabel("Test Score")
        self.greentestScore.setFont(userFont)
        self.greentestScore.setStyleSheet("color: green; background-color: transparent;")

        for i in range(1,10):
            for j in range(1,10):
                greenTeamLayout.addWidget(QLabel(" "),i,j)

        self.greenUserID.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.greenteamTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.greenScore.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.greentestUser.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.greentestScore.setAlignment(Qt.AlignmentFlag.AlignCenter)

        greenTeamLayout.addWidget(self.greenUserID, 1, 2)
        greenTeamLayout.addWidget(self.greenteamTitle, 0, 5)
        greenTeamLayout.addWidget(self.greenScore, 1, 8)
        greenTeamLayout.addWidget(self.greentestUser, 2, 2)
        greenTeamLayout.addWidget(self.greentestScore, 2, 8)
        #greenTeamLayout.addWidget(self.initializeGrid, 9, 14)
        #greenTeamVerLayout.addWidget(self.teamTitle)
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
        # self.red_id_header.setSizePolicy(QSizePolicy.expandingDirections, 0)

        self.red_codename_header = QLabel("Codename")
        self.red_codename_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_codename_header.setStyleSheet("color: white; background-color: transparent;")
        # self.red_codename_header.setSizePolicy(QSizePolicy.expandingDirections, 0)

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

        self.players_red = []

        # this for loop creates the tables for red team
        for i in range(15):
            playerLayout = QHBoxLayout()

            # Create the player number label
            player_number = QLabel(str(i + 1))
            player_number.setStyleSheet("color: white; background-color: transparent;")
            player_number.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            player_number.setFixedWidth(
                30)  # This need to be here to ensure numbers past 10 don't push the boxes to the right

            id_input = QLineEdit()
            id_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            codename_input = QLineEdit()
            codename_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            equipment_id_input = QLineEdit()
            equipment_id_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            # Add input fields to the player layout. The 2nd parameters are the stretch factors to size the boxes properly.
            playerLayout.addWidget(player_number)
            playerLayout.addWidget(id_input, 1)
            playerLayout.addWidget(codename_input, 3)
            playerLayout.addWidget(equipment_id_input, 1)

            # Add the player layout to the team layout
            redTeamVerLayout.addLayout(playerLayout)

            # redTeamVerLayout.addStretch(1)
            self.players_red.append((id_input, codename_input, equipment_id_input))

        # Create save button
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("border: 1px solid white; border-radius: 15px; color: white;")
        self.save_button.setFixedSize(50, 20)
        self.save_button.clicked.connect(lambda: self.save_players_ui("red"))

        redTeamVerLayout.addWidget(self.save_button)
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

            id_input = QLineEdit()
            id_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            codename_input = QLineEdit()
            codename_input.setStyleSheet(
                "color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            equipment_id_input = QLineEdit()
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

        # Create save button
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("border: 1px solid white; border-radius: 15px; color: white;")
        self.save_button.setFixedSize(50, 20)
        self.save_button.clicked.connect(lambda: self.save_players_ui("green"))

        greenTeamVerLayout.addWidget(self.save_button)
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
       def prompt_equipment_id(self):
        equipment_id, ok = QLineEdit.getText("Equipment ID Prompt", "Enter Equipment ID:")
        if ok:
            # Logic to handle the equipment ID input
            try:
                equipment_id = int(equipment_id)
                # Perform further actions with the equipment ID as needed
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid Equipment ID (integer).")
        pass

    def countdown(self):
        #Show countdown images
        pygame.init()
        # set pygame display size
        splash_display = pygame.display.set_mode((1000, 700))  # width height
        # set splashscreen image and scale to window
        pygame.display.set_caption('Photon Tag - Team 16')
        for i in range(30, -1, -1):
            filename = 'assets/splashscreen_game_sounds/countdown_images/{}.tif'.format(i)
            countdown_img = pygame.image.load(filename)
            countdown_img = pygame.transform.scale(countdown_img, (1000, 700))
            # display splashscreen
            splash_display.blit(countdown_img, (0, 0))
            pygame.display.update()
            # show for 3 seconds then close splashscreen
            time.sleep(1)
        pygame.quit()
        return 1

    def save_players_ui(self, team_color):
        # Convert input data to active Player objects and store them in backend lists
        try:
            # Handle red team players
            if team_color == "red":
                for id_input, codename_input, equipment_id_input in self.players_red:
                    player_id_text = id_input.text().strip()
                    # Check if player ID is provided
                    if player_id_text:
                        try:
                            # Perform Supabase search using player ID
                            db_search = self.main.database.getPlayer(int(player_id_text))
                            # If player is found in Supabase, prompt for codename and equipment ID
                            if not db_search['needsAdding']:
                                codename_input.setText(str(db_search['playerName']))
                                equipment_id_input.setFocus()  # Set focus to equipment ID input
                            else:
                                # Prompt user to input codename and equipment ID using QInputDialog
                                codename, ok1 = QInputDialog.getText(self, "Player Information", "Enter Codename:")
                                equipment_id, ok2 = QInputDialog.getText(self, "Player Information", "Enter Equipment ID:")
                                if ok1 and ok2:
                                    codename_input.setText(codename)
                                    equipment_id_input.setText(equipment_id)
                                    # add player to database
                                    self.main.database.addPlayer(int(player_id_text), codename)
                                    # transmit equipment code
                                    self.main.udp_server.transmit_message(equipment_id)
                        except ValueError:
                            print("Player ID must be an integer.")
            pass

            # Handle green team players
            if team_color == "green":
                for id_input, codename_input, equipment_id_input in self.players_green:
                    player_id_text = id_input.text().strip()
                    # Check if player ID is provided
                    if player_id_text:
                        try:
                            # Perform Supabase search using player ID
                            db_search = self.main.database.getPlayer(int(player_id_text))
                            # If player is found in Supabase, prompt for codename and equipment ID
                            if not db_search['needsAdding']:
                                codename_input.setText(str(db_search['playerName']))
                                equipment_id_input.setFocus()  # Set focus to equipment ID input
                            else:
                                # Prompt user to input codename and equipment ID using QInputDialog
                                codename, ok1 = QInputDialog.getText(self, "Player Information", "Enter Codename:")
                                equipment_id, ok2 = QInputDialog.getText(self, "Player Information", "Enter Equipment ID:")
                                if ok1 and ok2:
                                    codename_input.setText(codename)
                                    equipment_id_input.setText(equipment_id)
                                    # add player to database
                                    self.main.database.addPlayer(int(player_id_text), codename)
                                    # transmit equipment code
                                    self.main.udp_server.transmit_message(equipment_id)
                        except ValueError:
                            print("Player ID must be an integer.")
            pass
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
    mainWindow.resize(1000, 700)
    mainWindow.show()
    sys.exit(app.exec())
