# COMP590_Face_Filters

## Instructions to run ##

1. run `git clone https://github.com/asdunnbe/COMP590_Face_Filters.git` to clone the repository into your local directory
2. run `conda env create -f env.yml` to create a conda environment with the necessary dependencies
3. run `python gui.py` to open the program
4. enjoy!

## Project description ##

**GUI**

The first thing the user sees upon opening our program is the GUI, which contains a cartoon face and interactive controls. These controls include scales and toggle buttons that allow the user to customize the filter that they want to apply to their face. Customizable features consist of rotating the eyes, doubling the size of the eyes, blurring the background, and adding sunglasses. Adding sunglasses is mutually exclusive to the other eye related features. The cartoon face on the GUI will change to reflect the controls that the user inputs, so the user can easily see an example of what the end result might look like. Then, the user can click the submit button, which will launch a webcam with the applied filters. From the webcam, the user can take a screenshot or exit the webcam to readjust the filter. The applied filters will be described in further detail below. 

**Filters**

The first step in building our filters was recognizing multiple faces in an image in real time. To do facial recognition we used opencv2’s pre-trained Haar Cascade detectors. After recognizing all faces in the image we performed another round of detection to find the eyes in each face.

For the eye filter each of these detected eyes was taken as a separate subimage and rotated and scaled based on user specified input. The left eye and right eye would rotate in opposite directions to keep a symmetrical look, this was done using a simple affine transformation. The eye filter also allows the user to increase the size of their eyes, in order to do this a linear interpolation was applied to the eyes to create good looking results. The eyes were then drawn onto the original image with a blur to remove sharp edges and create more seamless results.

For the sunglasses filter the coordinates of the detected eyes played an important role. The filter was created by appropriately scaling and rotating a png of sunglasses and applying it to the detected faces. The coordinates of the eyes on each face were used to determine how to scale and rotate the sunglasses to fit the face. Using a simple arctan on the y and x distances between the eyes the rotation angle could be calculated. The sunglasses were scaled to match the euclidean distance between the two eyes.

**Blur**

Blurring was used in two parts of this project. One was to blur the eye object onto the face and the other was to blur the background. Although we had several attempts on how to implement blurring the edges of the eye object to the background face, we settled on a build in opencv seamless blend function after attempting to implement a Laplacian pyramid blur. From our experiments, the feathering from the pyramid was subpar and there was a lot of artifacts. Because of this, we used said built in function with a custom mask to achieve the best results. In order to blur the background, we used a mediapipe selfie-segmentation pre-trained model to segment the user from the background. Once the user was selected, a Gaussian blur was applied to the background. This did not visually affect the other filter being used; however, this additional step did slow down the processing time. 

**Obstacles**

The order in which eyes were detected wasn’t always the same and this would create a weird flickering effect that was undesired. To fix this problem the detected eyes were sorted in order of their x coordinates to ensure that they were always in left to right order. Additionally, if there were more than 2 eyes detected on a face the filter would not be applied. Sometimes other parts of the face were detected as eyes and this would create flickers that were also undesired.

**Shortcomings**

Lighting
The detector has a hard time detecting faces and features in poor lighting conditions leading to bad filter results
Face detection
If the user tilts their head to the side too much the haar cascades are not able to detect faces well
Real time
Having too many faces present in the image slows down the runtime of the filter, this is noticeable when using the webcam with a live video feed
