import cv2
from tkinter import *
from videoMask import roi_processing
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class App:
    def __init__(self, video, w0=1880, h0=1021):
        # ------------------Drawing frames block------------------
        self.drawingRect = None  # Drawing rect to define the roiRect
        self.roiRect = []  # ROI coordinates (x0, y0), (x1, y1) of the top left and bottom right corners

        # ----------------OpenCV GUI block-----------------------
        self.w0, self.h0 = w0, h0
        self.vidpath = video
        self.vid = cv2.VideoCapture(video)
        _, self.frame = self.vid.read()
        self.windowName = 'image'
        self.trTitle = 'tracker'
        self.trackerPos = 0

        # ----------------Tkinter block---------------------------
        self.window = None
        self.wFrame = None
        self.rowFrames = []
        self.fName = None
        self.bg = None
        self.shape = None
        self.begin(w0, h0)

    def begin(self, w0, h0):
        """
        Starts
        + frame showing
        + creates a trackbar for navigation
        + set mouse callback to draw Roi
        + calls drawROI
        """
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        h, w = self.frame.shape[:2]
        if h / h0 > w / w0:
            cv2.resizeWindow(self.windowName, int(w * h0 / h), h0)
        else:
            cv2.resizeWindow(self.windowName, self.w0, int(h * w0 / w))

        self.drawRoi(True)
        cv2.createTrackbar(self.trTitle, self.windowName, 0,
                           int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT)) - 1, self.trackbar)
        cv2.setMouseCallback(self.windowName, self.setRoi)
        cv2.waitKey(0)

    def setRoi(self, event, x, y, flags, params):
        """Mouse callback to set ROI

        event  - mouse event
        x: int  - x coordinate
        x: int  - y coordinate
        flags  - additional flags
        params - extra parameters
        """
        flag = False
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawingRect = [(x, y), (x, y)]

        elif event == cv2.EVENT_LBUTTONUP:
            flag = True
            pTL = (min(self.drawingRect[0][0], self.drawingRect[1][0]),
                   min(self.drawingRect[0][1], self.drawingRect[1][1]))

            pBR = (max(self.drawingRect[0][0], self.drawingRect[1][0]),
                   max(self.drawingRect[0][1], self.drawingRect[1][1]))
            self.drawingRect = None
            # Set the roiRect or reset it
            if pTL != pBR:
                # Adjust to X px padding
                pxBlock = 8
                dx = (pBR[0] - pTL[0]) % pxBlock
                if dx:
                    dx = pxBlock - dx
                dy = (pBR[1] - pTL[1]) % pxBlock
                if dy:
                    dy = pxBlock - dy
                self.roiRect.append((pTL, (pBR[0] + dx, pBR[1] + dy)))
            else:
                self.roiRect = self.roiRect[:-1]

        if event == cv2.EVENT_RBUTTONUP:
            """
            Delete drawn ROI by clicking inside it's area from the parent and child window
            """
            self.drawingRect = None

            for i, ((x1, y1), (x2, y2)) in enumerate(self.roiRect):
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.roiRect.remove(((x1, y1), (x2, y2)))
                    self.rowFrames.pop(i).destroy()

        if event == cv2.EVENT_MOUSEMOVE and self.drawingRect:
            self.drawingRect[1] = (x, y)

        self.drawRoi(flag)

    def drawRoi(self, flag=False):
        """
        Draws the set ROI and calls tkWidget function to change info in the child box
        :param flag: helping tool to understand if it is necessary to add drawn ROIs to the child box
        :return:
        """
        img = self.frame.copy()  # Copy image to not draw in over the original frame
        cv2.putText(img, str(self.trackerPos), (0, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 4)

        if self.roiRect or self.drawingRect:
            rcs = self.roiRect + [self.drawingRect] if self.drawingRect else self.roiRect
            rt = max(1, int(img.shape[1] / self.w0) + 1)

            # If it is the first completed ROI, then create the child box
            if not self.window and not self.drawingRect:
                self.createWidget()
            # if flag is on and drawing is completed then add new ROI to the child box
            elif not self.drawingRect and flag:
                self.updateWidget()

            for i, rc in enumerate(rcs):
                try:
                    row = self.rowFrames[i]
                    if int(row.winfo_children()[-3].get()) <= self.trackerPos <= int(row.winfo_children()[-1].get()):
                        img = cv2.rectangle(img, rc[0], rc[1], (0, 255, 0), rt)
                except IndexError:
                    img = cv2.rectangle(img, rc[0], rc[1], (0, 255, 0), rt)
                except Exception as e:  # done just to be sure that not unpredictable exception will occur
                    if str(e) != """can't invoke "winfo" command: application has been destroyed""":
                        print(e)

        cv2.imshow(self.windowName, img)

    def createWidget(self):
        """
        Creates child window
        """
        self.window = Tk()
        self.wFrame = LabelFrame(self.window, text="ROIs", padx=30, pady=10)
        self.wFrame.pack(side="top", fill="x")

        rowFrame = Frame(self.window)
        rowFrame.pack(side="bottom", fill="x")
        self.bg = StringVar(rowFrame)
        self.bg.set("color")  # default value

        Label(rowFrame, text="Random background:", font=('Calibri 12')).pack(side="left")
        OptionMenu(rowFrame, self.bg, *["color", "pixel static", "pixel dynamic"]).pack(side="left", padx=8)
        rowFrame.pack(side="bottom", fill="x")
        Button(rowFrame, text="Cancel", font=('Helvetica bold', 10), command=self.end, padx=8, pady=4).pack(
            padx=4, pady=4, side="right")
        Button(rowFrame, text="Accept", font=('Helvetica bold', 10), command=self.accept, padx=8, pady=4).pack(
            padx=4, pady=4, side="right")

        self.shape = IntVar()
        self.shape.set(1)
        rowFrame = LabelFrame(self.window, text="ROI shape", padx=30, pady=10)
        rowFrame.pack(side="bottom", fill="x")
        Radiobutton(rowFrame, text='rectangle', variable=self.shape, value=0).pack(anchor=W)
        Radiobutton(rowFrame, text='ellipse', variable=self.shape, value=1).pack(anchor=W)

        rowFrame = Frame(self.window)
        rowFrame.pack(side="bottom", fill="x")
        Label(rowFrame, text="New name:", font=('Calibri 12')).pack(side="left", padx=8)
        self.fName = Entry(rowFrame, font=('Calibri 12'))
        self.fName.insert(0, ".mp4")
        self.fName.pack(side="left", padx=8)

        self.updateWidget()

    def updateWidget(self):
        """
        If new Roi was drawn, the child box
        + adds ROI coordinates
        + creates entry field to get frame interval
        """
        roiRect = self.roiRect[-1]
        text = "x1: %g, y1: %g, w: %g, h: %g" % (roiRect[0][0], roiRect[0][1],
                                                 roiRect[1][0] - roiRect[0][0],
                                                 roiRect[1][1] - roiRect[0][1])

        rowFrame = Frame(self.wFrame)
        rowFrame.pack(side="top", fill="x")

        label = []
        label.append(Label(rowFrame, text=text, font=('Calibri 15 bold')))
        label.append(Label(rowFrame, text='interval:', font=('Calibri 15 bold')))
        label.append(Entry(rowFrame, width=4, font=('Calibri 15 bold')))
        label.append(Label(rowFrame, text='-', font=('Calibri 15 bold')))
        label.append(Entry(rowFrame, width=4, font=('Calibri 15 bold')))

        label[0].pack(side="left", padx=(0, 40))
        label[2].insert(0, '0')
        label[4].insert(0, str(int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT)) - 1))
        for i in range(1, len(label)):
            label[i].pack(side="left")

        self.rowFrames.append(rowFrame)
        self.window.mainloop()

    def accept(self):
        """
        Accept information and call function to mask a video
        """
        rois = []
        shape = ";ellipse" if self.shape.get() else ''
        for i, row in enumerate(self.rowFrames):
            roiRect = self.roiRect[i]
            rois.append("%i,%i,%i,%i%s^%s!%s" % (roiRect[0][0], roiRect[0][1],
                                                 roiRect[1][0] - roiRect[0][0],
                                                 roiRect[1][1] - roiRect[0][1],
                                                 shape,
                                                 row.winfo_children()[-3].get(),
                                                 row.winfo_children()[-1].get()))

        rand = "pixel" in self.bg.get()
        static = "static" in self.bg.get()
        roi_processing(self.vidpath, rois, self.fName.get(), rand=rand, static=static, color=None)
        self.end()

    def trackbar(self, val):
        """
        If trackbar changes position the new frame is shown on the screen
        :param val: new trackbar position
        """
        self.trackerPos = val
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, int(val))
        _, self.frame = self.vid.read()
        self.drawRoi()

    def end(self):
        cv2.destroyAllWindows()
        self.window.destroy()
        self.vid.release()


if __name__ == '__main__':
    parser = ArgumentParser(description='Document Taxonomy Builder.',
                            formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('-v', '--video', type=str, help='path to video')

    parser.add_argument('-wsize', type=str, default="1600x1200", help='Your screen parameters WxH')
    opt = parser.parse_args("-v E:\\work\\11-23_11-34.mp4".split())

    w, h = opt.wsize.split('x')
    App(opt.video, int(w), int(h))
