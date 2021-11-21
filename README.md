# VideoProcessingApplication
GUI developed to create ROIs and mask the video using videoMask.py


Author: (c) Valentyna Pryhodiuk <vpryhodiuk@lumais.com>
Date: 2021-11-21


## Usage
```
usage: ROIsCreationGUI.py [-h] [-v VIDEO] [-wsize WSIZE]

Document Taxonomy Builder.

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEO, --video VIDEO
                        path to video (default: None)
  -wsize WSIZE          Your screen parameters WxH (default: 1600x1200)
```
### Examples
```
$python ROIsCreationGUI.py -v ladybug.mp4

$python ROIsCreationGUI.py -v ladybug.mp4 -wsize 1600x1200
```
## Help with navigation
* To __draw ROI__ on the frame use LmouseButton and drag it until ROI is ok. To __delete a ROI__ do the RmouseButton click inside ROI's area.

* Draw your first ROI to make a child box appear (drawing helper).

* To __navigate__ use the trackbar in the top of the child window.

* To choose the displaying (masking) __interval__ write down the first and the last frames in the corresponding entry field.

* To change the frame into desired one the frame write in the entry field next to "Go to" label and push the "Jump" button.

* To switch to a __next or a previous__ frame push "Next" or "Previous" button in the left bottom corner.

* To __terminate__ the process and shut down the GUI push "Cancel" button in the right bottom corner.

* To choose the __shape__ use the radiobuttons in the left bottom corner above buttons.

* To input the __name of the resulting video__ write it's name in the entry field near the label "New name". Do not delete the ".mp4" type!

* Optionmenu with the question about background helps you choose the mask background.
  * color - goes for a random color per frame
  * pixel static - goes for a random pixel coloring which is constant during the output video
  * pixel dynamic - goes for a random pixel coloring which is changes on the each frame
