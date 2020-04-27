# Tai Sakuma <tai.sakuma@gmail.com>
import threading

##__________________________________________________________________||
def in_main_thread():
    """test if in the main threading
    """
    return threading.current_thread() == threading.main_thread()

##__________________________________________________________________||
