# required imports

# inter-reference classes
from src.Server import UDPServer
from db.PlayerDB import PlayerDB
from src.ui import ui_start

# Program Object for program inter-references (like server to ui or Player object to ui)
class Program:
    def __init__(self):
        # initialize program objects/inter-references
        self.database = PlayerDB()  # initialize database connection
        self.udp_server = UDPServer(7500, 7501)  # set server sockets transmit over 7500, recieve over 7501

        # initialize player lists, will hold player objects
        self.red_team = []
        self.green_team = []

        # start ui (frontend)
        ui_start(self)

    # Player object to hold player_id & equipment_id together
    #test
    class Player:
        def __init__(self, player_id, codename, equipment_id):
            self.player_id = player_id
            self.codename = codename
            self.equipment_id = equipment_id


# starts program
if __name__ == "__main__":
    main = Program()
