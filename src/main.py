import threading
from ui import run_ui
def thread_alpha():
    """Thread in-charge of UI
    Exit on UI Exit Event.
    """
    run_ui()


def thread_beta():
    """Thread in-charge of audio"""
    pass

def thread_gamma():
    """Empty thread"""
    pass


if __name__ == "__main__":
    # Init and start threads
    alpha = threading.Thread(target=thread_alpha, daemon=True)
    beta = threading.Thread(target=thread_beta, daemon=True)
    gamma = threading.Thread(target=thread_gamma, daemon=True)
    alpha.start()
    beta.start()
    gamma.start()
    # wait for alpha to exit and then auto exit others.
    alpha.join()