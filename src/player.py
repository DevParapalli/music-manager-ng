from typing import BinaryIO


class Player:

    def __init__(self):
        """ Init the player here."""
        pass

    def load_song(self, filelike: BinaryIO) -> None:
        """ Load song into player."""
        pass

    def play(self) -> None:
        """Play the currently loaded song, error if no song is present."""
        pass

    def pause(self) -> None:
        """Pause if playing error if not."""
        pass

    def _try_seek(self, seconds: float, force_partial_play: bool) -> None:
        """ The function that actually seeks with fallback."""
        pass

    def seek(self, seconds: float) -> None:
        """ Seek given number of seconds, if not supported replay song """
        pass

    def unload(self) -> None:
        """Unload the current song from player."""
        pass


# Need ideas about queue management, do we put it inside the Player Object or split into another Queue Object?
class Queue:
    pass


class QueueItem:
    pass
