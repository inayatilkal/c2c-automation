
import os
import time
from pathlib import Path
from contextlib import contextmanager

from client_config import OUTPUT_DIR

LOCK_FILE = OUTPUT_DIR / "resume.lock"


@contextmanager
def file_lock(timeout=30):
    """
    Cross-platform file lock.
    Prevents multiple processes from modifying resume files simultaneously.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lock = open(LOCK_FILE, "a+b")
    locked = False
    start_time = time.time()

    try:
        # Ensure the lock file contains at least one byte.
        lock.seek(0, os.SEEK_END)

        if lock.tell() == 0:
            lock.write(b"\0")
            lock.flush()

        while not locked:
            try:
                lock.seek(0)

                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(
                        lock.fileno(),
                        msvcrt.LK_NBLCK,
                        1
                    )
                else:
                    import fcntl
                    fcntl.flock(
                        lock.fileno(),
                        fcntl.LOCK_EX | fcntl.LOCK_NB
                    )

                locked = True

            except (OSError, BlockingIOError):
                if time.time() - start_time >= timeout:
                    raise TimeoutError(
                        "Could not acquire resume file lock."
                    )

                time.sleep(0.2)

        yield

    finally:
        if locked:
            lock.seek(0)

            if os.name == "nt":
                import msvcrt
                msvcrt.locking(
                    lock.fileno(),
                    msvcrt.LK_UNLCK,
                    1
                )
            else:
                import fcntl
                fcntl.flock(
                    lock.fileno(),
                    fcntl.LOCK_UN
                )

        lock.close()
