from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.set_properties()
        # self.defaults()
        self.create_widgets()

    def set_properties(self):
        self.settings()

        self.master.resizable(False, False)
        self.master.geometry(str(self.width) + "x" + str(self.height))

        self.position = {"x": int(root.winfo_screenwidth() / 2 - self.width / 2),
                         "y": int(root.winfo_screenheight() / 2 - self.height / 2)}
        self.master.geometry("+{}+{}".format(self.position["x"], self.position["y"]))

        self.master.title(self.title)

    # def defaults(self):

    def settings(self):
        self.title = "HTML Ingestor"

        self.height = 400
        self.width = 600

    def create_widgets(self):
        self.back = Frame(self, bg="#FFFFFF", height=self.height, width=self.width)
        self.back.pack_propagate(0)
        self.back.pack(fill=BOTH, expand=1)

        self.resolution = (self.width, self.height)

        # Frontal side excluding ribbons
        self.front = Frame(self.back, bg="#555555", height=self.height, width=self.width)
        self.front_resolution = (self.width, self.height)
        self.front.place(x=self.resolution[0] / 2, y=self.front_resolution[1], anchor="s", width=self.front_resolution[0], height=self.front_resolution[1])

        # self.button = Button(self.front)

if __name__ == "__main__":
    root = Tk()
    Application(master=root)
    root.mainloop()