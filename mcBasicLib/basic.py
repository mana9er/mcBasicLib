from PyQt5 import QtCore
from .player import Player, GhostingPlayer
import re
import time

__all__ = ['EasyMarker']


class McBasicLib(QtCore.QObject):
    """
    Provide basic functions and parsers for Minecraft Java Edition Server.
    """

    # Signals
    sig_player_input = QtCore.pyqtSignal(tuple)  # (Player, str) tuple, the player object and what he said.
    
    def __init__(logger, core):
        super(McBasicLib, self).__init__(core)
        self.logger = logger
        self.Player = Player
        self.GhostingPlayer = GhostingPlayer
        core.sig_command.connect(self.on_command)
        core.sig_server_output.connect(self.on_server_output)

    @QtCore.pyqtSlot(str)
    def on_command(self, cmd):
        self.sig_input.emit((GhostingPlayer(), cmd))

    @QtCore.pyqtSlot(list)
    def on_server_output(self, lines):
        for line in lines:
            match_obj = re.match(r'.*?<(\w+?)> (.*)', line)
            if match_obj:  # some players said something
                player = match_obj.group(1)
                text = match_obj.group(2)
                logger.debug('Player {} said: {}'.format(player, text))
                self.sig_input.emit((Player(player), text))

    def say(self, text):
        self.core.write_server('/say {}'.format(text))

    def tellraw(self, player, json_str):
        self.core.write_server('/tellraw {} {}'.format(player.name, json_str)

    def tell(self, player, text, color='yellow', bold=False):
        tell_obj = {
            'text': text,
            'color': color,
            'bold': bold
        }
        self.core.write_server('/tellraw {} {}'.format(player.name, json.dumps(tell_obj)))