import cv2

# Drawing rect to define the roiRect
drawingRect = None

# ROI coordinates (x0, y0), (x1, y1) of the top left and bottom right corners
roiRect = None
img = 0
initVideo = None


def setRoi(event, x, y, flags, params):
    """Mouse callback to set ROI

	event  - mouse event
	x: int  - x coordinate
	x: int  - y coordinate
	flags  - additional flags
	params - extra parameters
	"""
    global drawingRect, roiRect, img, initVideo
    frame = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        drawingRect = [(x, y), (x, y)]
    # print('\nStrting drawingRect: ', drawingRect)
    elif event == cv2.EVENT_LBUTTONUP:
        pTL = (min(drawingRect[0][0], drawingRect[1][0]), min(drawingRect[0][1], drawingRect[1][1]))
        pBR = (max(drawingRect[0][0], drawingRect[1][0]), max(drawingRect[0][1], drawingRect[1][1]))
        drawingRect = None
        # Set the roiRect or reset it
        if pTL != pBR or roiRect:
            initVideo = True  # Init video output
        if pTL != pBR:
            # Adjust to X px padding
            pxBlock = 8
            dx = (pBR[0] - pTL[0]) % pxBlock
            if dx:
                dx = pxBlock - dx
            dy = (pBR[1] - pTL[1]) % pxBlock
            if dy:
                dy = pxBlock - dy
            roiRect = (pTL, (pBR[0] + dx, pBR[1] + dy))
        # print('\nROI size is corrected by ({}, {}): ({}, {})'.format(dx, dy, roiRect[1][0]-roiRect[0][0], roiRect[1][1]-roiRect[0][1]))
        else:
            roiRect = None

    if event == cv2.EVENT_RBUTTONUP:
        drawingRect = None
        roiRect = None

    if event == cv2.EVENT_MOUSEMOVE and drawingRect:
        drawingRect[1] = (x, y)

    drawRoi(img, cv2.getTrackbarPos('slider', windowName))


def drawRoi(frame, pos):
    img = frame.copy()
    cv2.putText(img, str(pos), (0, img.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 4)
    if roiRect or drawingRect:
        rc = drawingRect if drawingRect else roiRect
        rt = max(1, int(w / w0) + 1)
        img = cv2.rectangle(img, rc[0], rc[1], (0, 255, 0), rt)
    cv2.imshow(windowName, img)

def on_change(val):
    vid.set(cv2.CAP_PROP_POS_FRAMES, int(val))
    _, img = vid.read()
    if drawingRect:
        img = img.copy()  # Copy image to not draw in over the original frame
    drawRoi(img, val)


vid = cv2.VideoCapture('E:\\work\\100testimages.mp4') #7-02_7-09
windowName = 'image'
total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
_, frame = vid.read()
# cv2.namedWindow(windowName) #, cv2.WINDOW_AUTOSIZE)
# _, _, w0, h0 = cv2.getWindowImageRect(windowName)
cv2.namedWindow(windowName,
                cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions                    # Read image
h, w = frame.shape[:2]
w0, h0 = (1880, 1021)
h2h = frame.shape[0] / h0
w2w = frame.shape[1] / w0
if h2h > w2w:
    cv2.resizeWindow(windowName, int(frame.shape[1] / h2h), h0)
else:
    cv2.resizeWindow(windowName, w0, int(frame.shape[0] / w2w))
img = frame.copy()
cv2.imshow(windowName, img)
cv2.createTrackbar('slider', windowName, 0, total, on_change)
cv2.setMouseCallback(windowName, setRoi)

cv2.waitKey(0)
cv2.destroyAllWindows()
