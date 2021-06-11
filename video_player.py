import vlc
import tkinter as Tk
from tkinter import ttk


def onClick():
    print("a click was successful!")


class Player(Tk.Frame):
    """The main window has to deal with events.
    """

    def __init__(self, parent, url=""):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.url = url

        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel)

        self.canvas.pack(fill=Tk.BOTH, expand=1)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

        self.parent.update()

        self.Media = self.Instance.media_new(self.url)
        self.player.set_media(self.Media)

        # set the window id where to render VLC's video output
        self.player.set_hwnd(self.GetHandle())

        #self.player.play()

    def GetHandle(self):
        return self.videopanel.winfo_id()

    def Play(self):
        self.player.play()

    def Exit(self):
        self.player.stop()

# if __name__ == "__main__":
#     root = Tk.Tk()
#
#     player = Player(root, title="tkinter vlc", url=r"D:\CS50_Ai\00_Search\Lecture0-Search.mp4")
#     player.bind('<Button-1>', onClick)
#
#     root.mainloop()
