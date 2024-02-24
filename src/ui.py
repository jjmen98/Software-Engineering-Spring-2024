import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMenuBar, QMenu, QSplashScreen, QMessageBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont

class MainWindow(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        # allows calls Database from self.main.database & UDP_Server calls from self.main.udp_server
        self.main = backend

        self.setWindowTitle("Photon | Team 16")
        self.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.setupUI()

        self.setMinimumSize(1000, 600)


    def setupUI(self):

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        #Sets up outer layout... Superimposes the buttons ontop of the player entry layout
        #mainLayout = QVBoxLayout(self.centralwidget)

        #Sets up Player entry (inner) layout
        playerEntryLayout = QHBoxLayout(self.centralwidget)

        #Sets left background then superimposes Red Team's Layout
        self.frame = QFrame()   #frame is the leftmost red background picture
        self.frame.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(120, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));")
        self.frame.setContentsMargins(20, 0, 100, 0) # To compensate for the table margins (Left, Up, Right, Down)

        redTeamLayout = self.setupRedTeam()
        self.frame.setLayout(redTeamLayout)

        #Sets right background then superimposes Green Team's Layout
        self.frame_2 = QFrame() #frame_2 is the rightmost green background picture
        self.frame_2.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.495074, fy:0.494, stop:0 rgba(0, 107, 24, 255), stop:1 rgba(0, 0, 0, 255));")
        self.frame_2.setContentsMargins(100, 0, 20, 0) # To compensate for the table margins (Left, Up, Right, Down)

        greenTeamLayout = self.setupGreenTeam()
        self.frame_2.setLayout(greenTeamLayout)

        #Adds Background + Team Layouts
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

        self.setStatusBar(None)

    # def load_player_ids_from_database(self):
    #     try:
    #         # Query the database to fetch all player IDs and usernames
    #         data, _ = self.supabase_client.from_("player").select("id", "codename").execute()
    #         print("Data from database:", data)  # Add this line for debugging

    #         # Ensure data is in the expected format
    #         if isinstance(data, list):
    #             # Extract player IDs and usernames from the fetched data
    #             player_data = [(record["id"], record["codename"]) for record in data]
    #             print("Processed player data:", player_data)  # Add this line for debugging
    #             return player_data
    #         else:
    #             print("Unexpected data format received from database:", data)
    #             return []
    #     except Exception as e:
    #         print("Error occurred while loading player data from database:", e)
    #         return []

    def setupRedTeam(self):
        # Red Team Layout
        redTeamLayout = QVBoxLayout()
        redTeamHeaderLayout = QHBoxLayout()

        redTeamLayout.setContentsMargins(70, 0, 20, 0) #Margin spacers: (Left, Up, Right, Down)
        redTeamLayout.addStretch(1)

        self.red_team_label = QLabel("RED TEAM")
        self.red_team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_team_label.setStyleSheet("color: white; background-color: transparent;")
        redTeamLayout.addWidget(self.red_team_label)

        # Red Team Headers
        self.red_id_header = QLabel("ID")
        self.red_id_header.setFixedWidth(50)        
        self.red_id_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_id_header.setStyleSheet("color: white; background-color: transparent;")
        #self.red_id_header.setSizePolicy(QSizePolicy.expandingDirections, 0)

        self.red_codename_header = QLabel("Codename")
        self.red_codename_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_codename_header.setStyleSheet("color: white; background-color: transparent;")
        #self.red_codename_header.setSizePolicy(QSizePolicy.expandingDirections, 0)

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
        redTeamLayout.addLayout(redTeamHeaderLayout)


        self.players_red = []

        for i in range(15):
            playerLayout = QHBoxLayout()

            # Create the player number label
            player_number = QLabel(str(i+1))
            player_number.setStyleSheet("color: white; background-color: transparent;")
            player_number.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            player_number.setFixedWidth(30)   #This need to be here to ensure numbers past 10 don't push the boxes to the right

            id_input = QLineEdit()
            id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            codename_input = QLineEdit()
            codename_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")


            equipment_id_input = QLineEdit()
            equipment_id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            # Add input fields to the player layout. The 2nd parameters are the stretch factors to size the boxes properly.
            playerLayout.addWidget(player_number)
            playerLayout.addWidget(id_input, 1)
            playerLayout.addWidget(codename_input, 3)
            playerLayout.addWidget(equipment_id_input, 1)

            # Add the player layout to the team layout
            redTeamLayout.addLayout(playerLayout)

            
            #redTeamLayout.addStretch(1)
            self.players_red.append((id_input, codename_input, equipment_id_input))

        
        #Create save button
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("border: 1px solid white; border-radius: 15px; color: white;")
        self.save_button.setFixedSize(50,20)
        self.save_button.clicked.connect(lambda: self.save_players_ui("red"))

        redTeamLayout.addWidget(self.save_button)
        redTeamLayout.addStretch(1)

        return redTeamLayout

    def setupGreenTeam(self):
        # Green Team Layout
        greenTeamLayout = QVBoxLayout()
        greenTeamHeaderLayout = QHBoxLayout()

        greenTeamLayout.setContentsMargins(20, 0, 70, 0) #Margin spacers: (Left, Up, Right, Downn)
        greenTeamLayout.addStretch(1)

        self.green_team_label = QLabel("GREEN TEAM")
        self.green_team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_team_label.setStyleSheet("color: white; background-color: transparent;")
        greenTeamLayout.addWidget(self.green_team_label)

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
        greenTeamLayout.addLayout(greenTeamHeaderLayout)


        self.players_green = []
        for i in range(15):
            playerLayout = QHBoxLayout()

            # Create the player number label
            player_number = QLabel(str(i+1))
            player_number.setStyleSheet("color: white; background-color: transparent;")
            player_number.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            player_number.setFixedWidth(30)   #This need to be here to ensure numbers past 10 don't push the boxes to the right

            id_input = QLineEdit()
            id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            codename_input = QLineEdit()
            codename_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            equipment_id_input = QLineEdit()
            equipment_id_input.setStyleSheet("color: white; background-color: black; border: 1px solid white; border-radius: 7px;")

            # Add input fields to the player layout. The 2nd parameters are the stretch factors to size the boxes properly.
            playerLayout.addWidget(player_number)
            playerLayout.addWidget(id_input, 1)
            playerLayout.addWidget(codename_input, 3)
            playerLayout.addWidget(equipment_id_input, 1)

            # Add the player layout to the team layout
            greenTeamLayout.addLayout(playerLayout)

            self.players_green.append((id_input, codename_input, equipment_id_input))


        #Create save button
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("border: 1px solid white; border-radius: 15px; color: white;")
        self.save_button.setFixedSize(50,20)
        self.save_button.clicked.connect(lambda: self.save_players_ui("green"))

        greenTeamLayout.addWidget(self.save_button)
        greenTeamLayout.addStretch(1)

        return greenTeamLayout

    def prompt_player_id(self):
        # Logic to prompt for player ID and handle database lookup
        pass

    def prompt_equipment_id(self):
        # Logic to prompt for equipment ID after player ID is entered
        pass

    def save_players_ui(self, team_color):
        # Convert input data to active Player objects and store them in backend lists
        try:
            # Handle red team players
            if team_color == "red":
                for id_input, codename_input, equipment_id_input in self.players_red:
                    player_id_text = id_input.text().strip()
                    codename_text = codename_input.text().strip()
                    equipment_id_text = equipment_id_input.text().strip()
                    # will need to be adjusted not require codename and equipment id fields and to prompt each of them
                    if player_id_text and codename_text and equipment_id_text:
                        try:
                            player = self.main.Player(int(player_id_text), codename_text, int(equipment_id_text))
                            # check for id in database
                            db_search = self.main.database.getPlayer(player.player_id)
                            # if id was found, replace codename with found one
                            if not db_search['needsAdding']:
                                player.codename = str(db_search['playerName'])
                                codename_input.setText(str(db_search['playerName']))
                            # else add player to database
                            else:
                                #attempt adding new player to database and "replace" codename text
                                codename_input.setText(str(self.main.database.addPlayer(player.player_id, player.codename)))
                            # add to player list (Do at game start)
                            # self.main.red_team.append(player)
                            # transmit equipment code
                            self.main.udp_server.transmit_message(str(player.equipment_id))
                        except ValueError:
                            print("Player ID and Equipment ID must be integers.")
            pass

            # Handle green team players
            if team_color == "green":
                for id_input, codename_input, equipment_id_input in self.players_green:
                    player_id_text = id_input.text().strip()
                    codename_text = codename_input.text().strip()
                    equipment_id_text = equipment_id_input.text().strip()
                    if player_id_text and codename_text and equipment_id_text:
                        try:
                            player = self.main.Player(int(player_id_text), codename_text, int(equipment_id_text))
                            # check for id in database
                            db_search = self.main.database.getPlayer(player.player_id)
                            # if id was found, replace codename with found one
                            if not db_search['needsAdding']:
                                player.codename = str(db_search['playerName'])
                                codename_input.setText(str(db_search['playerName']))
                            # else add player to database
                            else:
                                # attempt adding new player to database and "replace" codename text
                                codename_input.setText(
                                    str(self.main.database.addPlayer(player.player_id, player.codename)))
                            # add to player list (Do at game start)
                            # self.main.green_team.append(player)
                            # transmit equipment code
                            self.main.udp_server.transmit_message(str(player.equipment_id))
                        except ValueError:
                            print("Player ID and Equipment ID must be integers.")
            pass
        except Exception as e:
                print("Error occurred while saving data to Supabase:", e)



def ui_start(backend):
    app = QApplication(sys.argv)
    splash_pix = QPixmap('assets/splashscreen_game_sounds/logo.jpg').scaled(QSize(1000, 700), Qt.AspectRatioMode.KeepAspectRatio)
    splash = QSplashScreen(splash_pix)
    splash.show()
    app.processEvents()
    time.sleep(3)  # Display the splash screen for 3 seconds.
    splash.close()

    mainWindow = MainWindow(backend)
    mainWindow.resize(1000, 700)
    mainWindow.show()
    sys.exit(app.exec())
    
    