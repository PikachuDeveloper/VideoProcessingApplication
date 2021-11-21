# VideoProcessingApplication

GUI developed to create ROIs and mask the video using videoMask.py. To create the GUI on Windows type in the cmd for example

>python ROIsCreationGUI.py -v < path to the video to display > -wsize <Width of the screen 'x' Heigth of the screen in pixels>

>python ROIsCreationGUI.py -v ladybug.mp4

>python ROIsCreationGUI.py -v ladybug.mp4 -wsize 1600x1200

* To draw ROI on the frame use LmouseButton and drag it until ROI is ok. To delete a ROI do the RmouseButton click inside ROI's area.

* Draw your first ROI to make a child box appear (drawing helper).

* To navigate use the trackbar in the top of the child window.

* To choose the displaying (masking) interval write down the first and the last frames in the corresponding entry field.

* To choose the displaying (masking) interval write down the first and the last frames in the corresponding entry field.

* To go to the frame write in the entry field next to "Go to" label and push the "Jump" button.

* To switch to a next or a previous frame push "Next" or "Previous" button in the left bottom corner.

* To terminate the process and shut down the GUI push "Cancel" button in the right bottom corner.

* To choose the shape use the radiobuttons in the left bottom corner above buttons.

* To choose a name to the output video write it's name in the entry field near the label "New name". Do nt delete the ".mp4" type!

* Optionmenu with the question about background helps you choose the mask background.
  * color - goes for a random color per frame
  * pixel static - goes for a random pixel coloring which is constant during the output video
  * pixel dynamic - goes for a random pixel coloring which is changes on the each frame
