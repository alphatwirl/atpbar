import sys

from atpbar.presentation import Presentation

from .output import OutputStream
from .pickup import StreamPickup
from .type import FD, StreamQueue


class StreamRedirection:
    def __init__(self, queue: StreamQueue, presentation: Presentation) -> None:
        self.disabled = not presentation.stdout_stderr_redirection
        if self.disabled:
            return

        self.queue = queue
        self.presentation = presentation

        self.stdout = OutputStream(self.queue, FD.STDOUT)
        self.stderr = OutputStream(self.queue, FD.STDERR)

    def start(self) -> None:
        if self.disabled:
            return

        self.pickup = StreamPickup(
            self.queue, self.presentation.stdout_write, self.presentation.stderr_write
        )
        self.pickup.start()

        self.stdout_org = sys.stdout
        sys.stdout = self.stdout  # type: ignore

        self.stderr_org = sys.stderr
        sys.stderr = self.stderr  # type: ignore

    def end(self) -> None:
        if self.disabled:
            return

        sys.stdout = self.stdout_org
        sys.stderr = self.stderr_org
        self.queue.put(None)
        self.pickup.join()
