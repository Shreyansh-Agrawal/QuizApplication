'''Contains Player abstract class'''

from typing import Dict

from models.database.database_saver import DatabaseSaver
from models.users.user import User
from models.users.user_manager import UserManager


class Player(User, DatabaseSaver):
    '''
    Class representing a player user.

    Inherits from:
        User: Abstract Base Class for representing users.
        DatabaseSaver: Interface for saving to the database.

    Methods:
        save_to_database(): Saves the player to the database.
    '''

    def __init__(self, player_data: Dict) -> None:
        '''
        Initializes a Player instance.

        Args:
            player_data (Dict): A dictionary containing player details.
        '''
        super().__init__(user_data=player_data, role='player')

    def save_to_database(self) -> None:
        '''Save the player to the database.'''

        player_manager = UserManager(self)
        player_manager.save_to_database()
