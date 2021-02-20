import sys, tty, termios, signal
from constants import *

class Get:
    '''
    Explanation: The class is used to define functions required for input.

    Libraries Required:
        sys: This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
        tty: tty is basically a terminal (teletype). The library tty defines functions for putting the terminal into cbreak mode and raw modes.
        termios: This is a module which provides an interface to POSIX calls for tty I/O controls. This is only avaialble for OS which adhere to POSIX. For more information: https://manpages.debian.org/buster/manpages-dev/termios.3.en.html#Retrieving_and_changing_terminal_settings
    
    Additional Explanation: 
        POSIX: Basically this is the industry standard which IEEE have set. These define the API, shell and utility interfaces for an OS. This was done to distinguish between compatible and non compatible systems. For more information: https://stackoverflow.com/questions/1780599/what-is-the-meaning-of-posix
        cbreak: is a mode between raw mode (passes data as-is to the program without interpretting any special characters) and cooked mode (data is preprocessed before being given to a program).
    '''

    def __call__(self):
        '''
            Explanation: This function is used to accept single character input.

            Parameters: 
                None

            Return Values:
                ch: The single character which was input.

            Additional Explanation:
                sys.stdin.fileno: File number are low level concepts which describe open file. 0, 1 and 2 represent standard input, standard output and standard error respectively.
                fd: A file descriptor is an abstract indicator used to access a file or other input/output resource.
                termios.tcgetattr(): Gets the parameters associated with the object reffered by fd and stores them in the termios structures referenced by termios_p.
                tty.setraw(): Changes the mode of the file descriptor fd to raw. By default uses termios.TCSAFLUSH
                TCSAFLUSH: the change occurs after all output written to the object referred by fd has been transmitted, and all input that has been received but not read will be discarded before the change is made.
                termios.tcsetattr(): Sets the parameters associated with the terminal from the termios structure referred to by termios_p.
        '''
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class AlarmException(Exception):
    pass

class Input:
    def alarmHandler(self, signum, frame):
        raise AlarmException

    def getInput(self, getch=Get(), timeout=TIMEOUT):
        signal.signal(signal.SIGALRM, self.alarmHandler)
        signal.setitimer(signal.ITIMER_REAL, timeout)
        try:
            text = getch()
            signal.alarm(0)
            if text == 'a' or text == 'd' or text == ' ':
                return text
            else:
                return None
        except AlarmException:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
            return None
