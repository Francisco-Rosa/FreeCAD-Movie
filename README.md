# FreeCAD Movie Workbench
FreeCAD Workbench to create and animate camera, record and play videos of animations


The Movie Workbench icon

<img src=./icons//CreateVideoIcon.svg height=50>

### Features
##### The Movie Camera toolbar (create and animate cameras):

* Create animations of one or more cameras, showing the details of your project.
* With the connection module, it is possible to create animations of cameras and objects simultaneously.
* It is possible to create camera animations between two chosen points, making it follow a path or keeping it on a fixed base.
* The camera targets can be free, fixed or mobile with the option to make them follow the path together with the camera.
* Once the camera animations are established, it is possible to make further adjustments to the positions, rotations and zooms of the cameras until reaching the final desired settings.

##### The Clapperboard toolbar (record and play videos):

* Create frames from the FreeCAD 3D views (**R1**) or the rendered ones (**R2**).   
* Create videos from them.  
* Check the results playing the videos you have created.

(Watch the [sample video](https://www.youtube.com/watch?v=NXHm2nitWug))

### Installation

##### Via Addon Manager (Recommended)

- Menu Tools > Addon Manager
- Locating Movie Worbench and installing it
- Restart FreeCAD
   

##### Manually install using GitHub
  
- Download the ZIP file (click 'Clone or Download' button above) 
- For Ubuntu and similar OS's, extract it inside */home/username/.local/share/FreeCAD/Mod*   
- For Windows, extract it inside *C: \Users\your_user_name\AppData\Roaming\FreeCAD\Mod*
- On macOS it is usually */Users/username/Library/Preferences/FreeCAD/Mod*
- Launch FreeCAD

### Preparation

* If yoy want use the rendered frames (**R2**), you must install the Render Workbench, prepare rendering projects and test them preventively to make sure everything is working correctly (see information in [FreeCAD-Render](https://github.com/FreeCAD/FreeCAD-render)). It is also recommended to take advantage and use some cameras from this workbench that better show the animation.
* If you want to use an animation from another workbench, script or macro of FreeCAD, it is necessary to prepare connection module for using then (ex. [Modified ExplodedAssembly](https://github.com/Francisco-Rosa/ExplodedAssembly)). For this, see the instructions inside the [Connection.py](https://github.com/Francisco-Rosa/FreeCAD-Movie/blob/master/Connection.py).


### Usage

##### To create camera animation go to Movie Camera toolbar and:
<img src=./Docs/Image_MC_toolbar.jpg height=50>

1. Click on the Create a Movie Camera button <img src=./icons//CreateMovieCameraIcon.svg height=20> to create one and to configure it (see the tips showed for each item in the property window - a Movie Camera properties image is showed below).
2. To configure the movie camera to animations between two positions, first, select and activate the Movie Camera you want to configure with the Enable Movie Camera icon <img src=./icons//EnableMovieCameraIcon.svg height=20>. Position the 3D view with the desired framing to be the start of the animation (Pos A), click on Set the position A button <img src=./icons//SetMovieCameraPosAIcon.svg height=20>. Position the 3D view with the desired framing to be the end of the animation (Pos B), then click on Set the position B button <img src=./icons//SetMovieCameraPosBIcon.svg height=20>. Click on go to beginning <img src=./icons//IniMovieAnimationIcon.svg height=20> and to the end of the animation buttons <img src=./icons//EndMovieAnimationIcon.svg height=20> to confirm the configurations. Make the adjustments you want in the position, rotation and zoom of the Movie Camera (see Movie Camera properties image below).
3. To make that the Movie Camera follows a route, you must create a segment first to do so. It can be a line, arc, circle, ellipse, B-spline or Bézier curve, from Sketcher or Draft Workbenches. Select the segment created in Cam_Route_Selection property. Configure the remaining camera properties.
4. To keep the movie Camera on a fixed base, you can use the Pos A <img src=./icons//SetMovieCameraPosAIcon.svg height=20> and B <img src=./icons//SetMovieCameraPosBIcon.svg height=20> buttons method explained, for example. Use the same position for then, adjusting the remaining settings as desired (rotation, zoom, steps, target, etc.).
5. The targets of the Movie Cameras can be adjusted to follow paths, fixed or mobile points or objects or living free to permit use of rotations angles, for example.
6. To create animations of cameras and objects simultaneously, you have to use an additional workbench that the connection module be already prepared to communicate with, if so, select the workbench you want to work in Cam_3Connection property.
7. To perform an animation, first select the Movie Cameras <img src=./icons//MovieCameraIcon.svg height=20> you want to animate , the sequence of selection will be the one adopted for the animation. Run a round trip in the animation with the go buttons to the end <img src=./icons//EndMovieAnimationIcon.svg height=20> and to the beginning of the animation <img src=./icons//IniMovieAnimationIcon.svg height=20> to reset all the steps of the animation in their initial positions. Then click on play animation button <img src=./icons//PlayMovieAnimationIcon.svg height=20>. If there is a connection activated, the animation of objects will work too.
8. Use the go to beginning <img src=./icons//IniMovieAnimationIcon.svg height=20>, one step back <img src=./icons//PrevMovieAnimationIcon.svg height=20> , pause <img src=./icons//PauseMovieAnimationIcon.svg height=20>, one step forward <img src=./icons//PostMovieAnimationIcon.svg height=20> and go to end <img src=./icons//EndMovieAnimationIcon.svg height=20> buttons as needed. They will also work with the workbench animations connected, if so.

##### After the animations are done, go to Clapperboard toolbar and:
<img src=./Docs/Image_MW_toolbar_2.jpg height=50>

1. Click on <img src=./icons//CreateClapperboardIcon.svg height=20>  to **create the Clapperboard** and <img src=./icons//ClapperboardIcon.svg height=20> to **configure it** (see the tips showed for each item in the property window).
2. Activate one or more movie cameras. Run a round trip, mentioned before.
3. Position your animation at the desired step.
4. Click on <img src=./icons//StartRecord3DViewIcon.svg height=20> for **record 3D view frames** or <img src=./icons//StartRecordRenderIcon.svg height=20> for **record rendered** ones, choose or confirm the folder to salve the frames.
5. Start the animation with the play animation button.
6. If You want only to stop recording, click on <img src=./icons//StopRecordCameraIcon.svg height=20>  **stop recording**.
7. If you need to stop the animation, click on **pause button** <img src=./icons//PauseMovieAnimationIcon.svg height=20>, it will also stop recording.
8. After the animation finished, choose the folder to salve your video and click on <img src=./icons//CreateVideoIcon.svg height=20>  **create video**, choose or confirm the input frames folder.
9. For playing video, choose the file and click on <img src=./icons//PlayVideoIcon.svg height=20> **play video**.

(Watch the [Clapperboard tutorial video](https://www.youtube.com/watch?v=_IiIWtO76Tg))

The Movie Camera properties

<img src=./Docs/Image_MC_properties.jpg height=600>

The Clapperboard properties

<img src=./Docs/Image_MW_toolbar_propr.jpg height=600>

The Clapperboard menu

<img src=./Docs/Image_MW_menu.jpg height=600>

 
### Documentation
For more information, see the [TUTORIAL.md](https://github.com/Francisco-Rosa/FreeCAD-Movie/blob/master/TUTORIAL.md) (also inside the Movie folder, after the installation).
Wiki documentation will be available as soon as possible.
  
### Feedback 
For discussion, please use the [Movie Workbench thread](https://forum.freecadweb.org/viewtopic.php?f=8&t=74432) in the FreeCAD forum.

#### License 
LGPL-2.1

#### Author
Francisco Rosa
