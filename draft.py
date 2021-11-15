import cv2


class App:
    def __init__(self, video, w0=1880, h0=1021):
        # Drawing rect to define the roiRect
        self.drawingRect = None
        self.vid = cv2.VideoCapture(video)
        self.windowName = 'image'
        self.trTitle = 'tracker'
        self.trackerPos = 0
        self.w0, self.h0 = h0, w0
        _, self.frame = self.vid.read()
        # ROI coordinates (x0, y0), (x1, y1) of the top left and bottom right corners
        self.roiRect = []
        self.initVideo = None
        self.start()

    def start(self):
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        h, w = self.frame.shape[:2]
        # h2h = h / self.h0
        # w2w = w / self.w0
        if h / self.h0 > w / self.w0:
            cv2.resizeWindow(self.windowName, int(w * self.h0 / h), self.h0)
        else:
            cv2.resizeWindow(self.windowName, self.w0, int(h * self.w0 / w))
        img = self.frame.copy()

        cv2.imshow(self.windowName, img)
        cv2.createTrackbar(self.trTitle, self.windowName, 0,
                           int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT)) - 1, self.on_change)
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
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawingRect = [(x, y), (x, y)]

        elif event == cv2.EVENT_LBUTTONUP:
            pTL = (min(self.drawingRect[0][0], self.drawingRect[1][0]),
                   min(self.drawingRect[0][1], self.drawingRect[1][1]))

            pBR = (max(self.drawingRect[0][0], self.drawingRect[1][0]),
                   max(self.drawingRect[0][1], self.drawingRect[1][1]))
            self.drawingRect = None
            # Set the roiRect or reset it
            if pTL != pBR or self.roiRect:
                self.initVideo = True  # Init video output
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
            self.drawingRect = None
            self.roiRect = self.roiRect[:-1]

        if event == cv2.EVENT_MOUSEMOVE and self.drawingRect:
            self.drawingRect[1] = (x, y)

        self.drawRoi()


    def drawRoi(self):
        img = self.frame.copy() # Copy image to not draw in over the original frame
        cv2.putText(img, str(self.trackerPos + 1), (0, img.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 4)
        if self.roiRect or self.drawingRect:
            rcs = self.roiRect + [self.drawingRect] if self.drawingRect else self.roiRect
            rt = max(1, int(img.shape[1] / self.w0) + 1)
            for rc in rcs:
                img = cv2.rectangle(img, rc[0], rc[1], (0, 255, 0), rt)
        cv2.imshow(self.windowName, img)


    def on_change(self, val):
        self.trackerPos = val
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, int(val))
        _, self.frame = self.vid.read()
        self.drawRoi()

    def end(self):
        cv2.destroyAllWindows()
        self.vid.release()


if __name__ == '__main__':

    video = 'E:\\work\\100testimages.mp4'
    App(video) #.end()
