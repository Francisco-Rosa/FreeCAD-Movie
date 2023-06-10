# FreeCAD Movie Workbench
FreeCAD Workbench to animate cameras and objects, record and play videos


The Movie Workbench icon

<img src=./icons//CreateVideoIcon.svg height=50>

### Features
##### The Movie Camera and Objects toolbars (animate cameras and objects):

* Create animations of cameras and objects separately or simultaneously, showing the details of your project.
* It is possible to create cameras/objects animations between two chosen points, making them follow a path or rotating them on a fixed base/axis.
* The camera targets can be free, fixed or mobile with the option to make them follow the path together with the camera.
* Once the camera animations are established, it is possible to make further adjustments to the positions, rotations and zooms of the cameras until reaching the final desired settings.
* If you already have a animation in another workbench, you can add cameras animations and produce render videos with the connection module (see below more details).

##### The Animation toolbar (visualize your animations within FreeCAD):

* You can play, pause, go back and forward the cameras/objects animations in real time within FreeCAD, before record them in videos.

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
* If you want to use an animation from another workbench, script or macro of FreeCAD, it is necessary to prepare the connection module for using then (ex. [Modified ExplodedAssembly](https://github.com/Francisco-Rosa/ExplodedAssembly)). For this, see the instructions inside the [Connection.py](https://github.com/Francisco-Rosa/FreeCAD-Movie/blob/master/Connection.py).


### Usage

##### To create camera animations go to Movie Cameras and objects toolbar and:
<img src=./Docs/Movie_cameras_objects_toolbar.png height=50>

1. Click on the Create a Movie Camera button <img src=./icons//CreateMovieCameraIcon.svg height=20> to create one and to configure it (see the tips showed for each item in the property window - a Movie Camera properties image is showed below).
2. To configure the movie camera to animations between two positions, first, select and activate the Movie Camera you want to configure with the Enable Movie Camera icon <img src=./icons//EnableMovieCameraIcon.svg height=20>. Position the 3D view with the desired framing to be the start of the animation (Pos A), click on Set the Position A button <img src=./icons//SetMoviePosAIcon.svg height=20>. Position the 3D view with the desired framing to be the end of the animation (Pos B), then click on Set the Position B button <img src=./icons//SetMoviePosBIcon.svg height=20>. Click on go to beginning <img src=./icons//IniMovieAnimationIcon.svg height=20> and to the end of the animation buttons <img src=./icons//EndMovieAnimationIcon.svg height=20> to confirm the configurations. Make the adjustments you want in the position, rotation and zoom of the Movie Camera (see Movie Camera properties image below).
3. To make that the Movie Camera follows a route, you must create a segment first to do so. It can be a line, arc, circle, ellipse, B-spline or Bézier curve, from Sketcher or Draft Workbenches. Select the segment created in Cam_Route_Selection property. Configure the remaining camera properties.
4. To keep the movie Camera on a fixed base, you can use the Pos A <img src=./icons//SetMoviePosAIcon.svg height=20> and B <img src=./icons//SetMoviePosBIcon.svg height=20> buttons method explained, for example. Use the same position for then, adjusting the remaining settings as desired (rotation, zoom, steps, target, etc.).
5. The targets of the Movie Cameras can be adjusted to follow paths, fixed or mobile points or objects or living free to permit use of rotations angles, for example.
6. To create animations of cameras and objects simultaneously, prepare one or more movie camera animations (according to the previous instructions) then create the objects animations (see instrutions below) and include them in sequency in Cam_5ObjectsSelected property, in Cam_6Enable one, chose 'Camera and objects'.
7. To apply animation from another workbench, you have to use one that the connection module be already prepared to communicate with, if so, select the workbench you want to work in Cam_3Connection property.
8. To perform an animation, first select one or more Movie Cameras <img src=./icons//MovieCameraIcon.svg height=20> you want to animate , the sequence of Movie Cameras selected will be the one adopted for the animation. Run a round trip in the animation with the go buttons to the end <img src=./icons//EndMovieAnimationIcon.svg height=20> and to the beginning of the animation <img src=./icons//IniMovieAnimationIcon.svg height=20> to reset all the steps of the animation in their initial positions. Then click on Play Animation button <img src=./icons//PlayMovieAnimationIcon.svg height=20>. You can play backwards too - Play Backward button <img src=./icons//PlayBackwardMovieAnimationIcon.svg height=20>. If a connection is previously configured and activated in the movie camera properties, objects related to this connection will be animated as well.
9. Use the go to beginning <img src=./icons//IniMovieAnimationIcon.svg height=20>, one step back <img src=./icons//PrevMovieAnimationIcon.svg height=20> , pause <img src=./icons//PauseMovieAnimationIcon.svg height=20>, one step forward <img src=./icons//PostMovieAnimationIcon.svg height=20> and go to end <img src=./icons//EndMovieAnimationIcon.svg height=20> buttons as needed. They will also work with the objects or workbench animations connected, if so.

<img src=./Docs/Movie_animation_toolbar.png height=50>

##### To create object animations go to Movie Cameras and Objects toolbar and:
<img src=./Docs/Movie_cameras_objects_toolbar.png height=50>

1. Select the objects you want to animate, click on the Create a Movie Objects button <img src=./icons//CreateMovieObjectsIcon.svg height=20> to create one and to configure it (see the tips showed for each item in the property window - a Movie Objects properties image is showed below). These initial placements of the objects will be saved and they can be rescue when you delete the movie objects with the Exclude Movie Objects button <img src=./icons//ExcludeMovieObjectsIcon.svg height=20>.
2. To configure the movie objects to animations between two positions, first, select and activate the Movie Objects you want to configure with the Enable Movie Objects icon <img src=./icons//EnableMovieObjectsIcon.svg height=20>. Position each object at the desired position and angles to be the start of the animation (Pos A), click on Set the Position A button <img src=./icons//SetMoviePosAIcon.svg height=20>. Now, position each object at the desired position and angles to be the end of the animation (Pos B), then click on Set the Position B button <img src=./icons//SetMoviePosBIcon.svg height=20>. Click on go to beginning <img src=./icons//IniMovieAnimationIcon.svg height=20> and to the end of the animation buttons <img src=./icons//EndMovieAnimationIcon.svg height=20> to confirm the configurations.
3. To make that the Movie Objects follows a route, you must create a segment first to do so. It can be a line, arc, circle, ellipse, B-spline or Bézier curve, from Sketcher or Draft Workbenches. Select the segment created in Objects_Route_Selection property. Configure the remaining object properties.
4. To rotate a group of objects around a fixed axis, you have first create a MovieObjects and set its Pos A and B, then select only those objects among the group that you want to rotate (first the objects, then the axis) and click on Set Movie Objects Axis button <img src=./icons//SetMovieObjectsAxisIcon.svg height=20>. To erase these settings, first clique on Enable the Movie Objects button <img src=./icons//EnableMovieObjectsIcon.svg height=20> then on Set Movie PosB button <img src=./icons//SetMoviePosBIcon.svg height=20>.
5. If you want that the objects rotate around their centers of gravity, after create a MovieObjects and set its Pos A and B, abilitate the Objects_RotationCG property (True option).
6. You can animate a series of movie objects in a desire sequency by clicking on them <img src=./icons//MovieObjectsIcon.svg height=20> in the property window accordinly of that and enabling them (with the Enable Movie Objects button <img src=./icons//EnableMovieObjectsIcon.svg height=20>). The animation will be preformed the sequence created.
7. To create animations of cameras and objects simultaneously, you have to prepare one or more movie cameras and objects animations first (according to the previous instructions) and combine them in sequency (cameras with objects) in Cam_5ObjectsSelected property, then in Cam_6Enable one, chose 'Camera and objects'.
8. To apply animation from another workbench, you have to use one that the connection module be already prepared to communicate with, if so, select the workbench you want to work in Cam_3Connection property.
9. To perform an animation, first select one or more Movie Objects <img src=./icons//MovieObjectsIcon.svg height=20> (objects only) or Movie Cameras <img src=./icons//MovieCameraIcon.svg height=20> (camera and objects) you want to animate, the sequence of selection will be the one adopted for the animation. Run a round trip in the animation with the go buttons to the end <img src=./icons//EndMovieAnimationIcon.svg height=20> and to the beginning of the animation <img src=./icons//IniMovieAnimationIcon.svg height=20> to reset all the steps of the animation in their initial positions. Then click on Play Animation button <img src=./icons//PlayMovieAnimationIcon.svg height=20>. You can play backwards too - Play Backward button <img src=./icons//PlayBackwardMovieAnimationIcon.svg height=20>. The animation of connected workbenches objects only works when associated with a movie camera (see instructions for movie cameras animation above).
10. Use the go to beginning <img src=./icons//IniMovieAnimationIcon.svg height=20>, one step back <img src=./icons//PrevMovieAnimationIcon.svg height=20> , pause <img src=./icons//PauseMovieAnimationIcon.svg height=20>, one step forward <img src=./icons//PostMovieAnimationIcon.svg height=20> and go to end <img src=./icons//EndMovieAnimationIcon.svg height=20> buttons as needed.

<img src=./Docs/Movie_animation_toolbar.png height=50>

##### After the animations are done, go to Movie Record and Play toolbar (Clapperboard) and:
<img src=./Docs/Movie_record_play_toolbar.png height=50>

1. Click on <img src=./icons//CreateClapperboardIcon.svg height=20>  to **create the Clapperboard** and <img src=./icons//ClapperboardIcon.svg height=20> to **configure it** in the property window (see the tips showed for each item).
2. Select the cameras and objects you want to animate and record through the clapperboard using the corresponding fields in the property window. Enable the Clapperboard <img src=./icons//EnableMovieClapperboardIcon.svg height=20> and run a round trip, mentioned before.
3. Position your animation at the desired step.
4. Click on <img src=./icons//StartRecord3DViewIcon.svg height=20> for **record 3D view frames** or <img src=./icons//StartRecordRenderIcon.svg height=20> for **record rendered** ones, choose or confirm the folder to salve the frames.
5. Start the animation with the Play Animation button <img src=./icons//PlayMovieAnimationIcon.svg height=20>. You can play backwards (and record) too - Play Backward button <img src=./icons//PlayBackwardMovieAnimationIcon.svg height=20>.
6. If You want only to stop recording, click on <img src=./icons//StopRecordCameraIcon.svg height=20>  **stop recording**.
7. If you need to stop the animation, click on **pause button** <img src=./icons//PauseMovieAnimationIcon.svg height=20>, it will also stop recording.
8. After the animation finished, choose the folder to salve your video and click on <img src=./icons//CreateVideoIcon.svg height=20>  **create video**, choose or confirm the input frames folder.
9. For playing video, choose the file and click on <img src=./icons//PlayVideoIcon.svg height=20> **play video**.

(Watch the [Clapperboard tutorial video](https://www.youtube.com/watch?v=_IiIWtO76Tg))

##### The Movie Objects properties:

<img src=./Docs/Movie_objects_properties.png height=466>

##### The Movie Camera properties:

<img src=./Docs/Movie_camera_properties.png height=1231>

##### The Clapperboard properties:

<img src=./Docs/Movie_Clapperboard_Properties.png width=900>

##### The Movie Cameras and Objects menu:

<img src=./Docs/Movie_Cameras_Objects_Menu.png width=900>

##### The Movie Animation menu:

<img src=./Docs/Movie_Animation_Menu.png width=900>

##### The Movie Record and Play menu:

<img src=./Docs/Movie_Record_Play_Menu.png width=900>

##### The context menu:

<img src=./Docs/Context_menu.png width=900>

 
### Documentation
For more information, see the [TUTORIAL.md](https://github.com/Francisco-Rosa/FreeCAD-Movie/blob/master/TUTORIAL.md) (also inside the Movie folder, after the installation).
Wiki documentation will be available as soon as possible.
  
### Feedback 
For discussion, please use the [Movie Workbench thread](https://forum.freecadweb.org/viewtopic.php?f=8&t=74432) in the FreeCAD forum.

#### License 
LGPL-2.1

#### Author
Francisco Rosa
