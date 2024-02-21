import os
# pip install supabase
from supabase import create_client, Client
# pip install python-dotenv, might need to restart terminal
from dotenv import load_dotenv


# database object to interface Photon Tag Software with codename database
class PlayerDB:
    # constructor
    def __init__(self):
        # load .env file
        load_dotenv()
        # read url & key from .env
        self.url: str = os.getenv('DATABASE_URL')
        self.key: str = os.getenv('DATABASE_KEY')
        # open client connection
        print('Opening DB')
        self.supabase: Client = create_client(self.url, self.key)
        print('DB Opened')
        # data & count returns
        self.data = None
        self.count = None

    # read table for certain ID
    # returns dict->bool:needs to be added, str:player name
    def getPlayer(self, playerId: int) -> dict:
        # db get request
        self.data, self.count = self.supabase.table('player').select('*').eq('id', playerId).execute()
        # return data is tuple containing list containing dictionary of found id and codename

        # if list is empty, need player name to add to database
        if not self.data[1]:
            # tells front end to request adding of player to database
            return {'needsAdding': True, 'playerName': None}
        else:
            # tells front end player is in database and gives name
            return {'needsAdding': False, 'playerName': self.data[1][0].get('codename')}

    # add new player with unique ID to db
    # ONLY CALL IF getPlayer REQUESTS IT, can error as ids are forced unique / primary key
    # returns player name as string to indicate successful adding to database
    def addPlayer(self, playerId: int, playerName: str) -> str:
        # don't reattempt adding to db if error occurs
        check = True
        # db post request to database
        # adds player name under their unique id. id is a signed 8 bit integer, but should only use positive
        try:
            self.data, self.count = self.supabase.table('player').insert(
                {'id': playerId, 'codename': playerName}).execute()
        except Exception as e:  # intercepts exception if an id is already present in database
            print("PostGreSQL Error: ", e)
            check = False

        if check:
            # check that player is in database
            self.data, self.count = self.supabase.table('player').select('*').eq('id', playerId).execute()
            if self.data[1]:
                return self.data[1][0].get('codename')# return sucessfully retrieved codename if addition worked

        # unsuccessful addition to database
        return 'ERROR OCCURRED'
