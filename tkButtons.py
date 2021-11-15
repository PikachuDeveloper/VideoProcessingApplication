import tkinter as tk
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import RectangleSelector


class App:
    def __init__(self, vidpath):
        self.vid = cv2.VideoCapture(vidpath)
        _, self.frame = self.vid.read()
        self.framenum = 1
        self.roi = None
        self.fig, self.ax = plt.subplots()
        # self.root = tk.Tk()
        self.button()

    def button(self):
        # bar1 = FigureCanvasTkAgg(self.fig, self.root)
        b1 = tk.Button(text="Next",
                       width=15, height=3)
        b1.config(command=self.next)
        b2 = tk.Button(text="Prev",
                       width=15, height=3)
        b2.config(command=self.prev)
        b1.pack()
        b2.pack()
        RectangleSelector(self.ax, self.line_select_callback,
                          drawtype='box', useblit=True,
                          button=[1, 3],  # disable middle button
                          minspanx=5, minspany=5,
                          spancoords='pixels',
                          interactive=True)

        # fig.canvas.mpl_connect('key_press_event', toggle_selector)
        self.draw(True)

    def line_select_callback(self, eclick, erelease):
        """
        Callback for rectangle selection.

        *eclick* and *erelease* are the press and release events.
        """
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print(f"({x1:3.2f}, {y1:3.2f}) --> ({x2:3.2f}, {y2:3.2f})")
        print(f" The buttons you used were: {eclick.button} {erelease.button}")
        self.roi = [[x1, y1], [x2, y2]]

    def next(self):
        """
        Button to change frame on the window into the next vid frame
        """
        try:
            _, self.frame = self.vid.read()
            self.framenum += 1
            plt.clf()
            # clear_output(wait=True)
            self.draw()
        except Exception as e:
            print(e)

    def prev(self):
        """
        Button to change frame on the window into the previous vid frame
        """
        try:
            self.framenum = max(1, self.framenum - 1)
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, self.framenum)
            _, self.frame = self.vid.read()
            plt.clf()
            # clear_output(wait=True)
            self.draw()
        except Exception as e:
            print(self.framenum, e)

    def draw(self, flag=False):
        """
        Used to visualize the frame (probably I should change the name of the function...)
        :param flag: if it is the first showing, then True
        :return:
        """
        self.frame = self.frame[:, :, ::-1]
        plt.imshow(self.frame)
        plt.title('frameNumber ' + str(self.framenum))
        plt.show()
        # if flag:
        #     self.root.mainloop()


video = 'E:\\work\\3-38_3-52.mp4'

app = App(video)
app.vid.release()
