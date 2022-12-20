Movie Workbench
        
Introduction

    The Movie Workbench is a platform for creating and playing videos within FreeCAD itself. It is directly aimed at recording animations produced in FC, whether using its animation workbenches, scripts or macros. As a "bonus" it also allows the production and playback of videos from external files.
    
    The activation of the animation remains in the corresponding workbench (start, pause, rewind, etc.). Hence, the concept of using a "Clapperboard" on the Movie Workbench, as the "action" will be on account of the animation one.


Steps for using the Movie workbench:

1. Preparations

    1.1. Create an animation with a workbench, script or macro of FreeCAD that are prepared for using this workbench (ex. ExplodedAssembly: https://github.com/Francisco-Rosa/ExplodedAssembly). If you want to integrated one of those to Movie Workbench, see how to trigger the recording from the animation code in item 5 (below).

    1.2. Configure the Render projects and cameras if you want to use them

        Install the Render workbench and install the external rendering programs, indicating them in the FC preferences, and carry out all the necessary preparations. See instructions on the Render Workbench at:
        https://github.com/FreeCAD/FreeCAD-render
        https://wiki.freecadweb.org/Manual:Creating_renderings
        https://github.com/FreeCAD/FreeCAD-render/blob/master/docs/EngineInstall.md

        Prepare the Render project(s) as per the instructions on the mentioned websites. Click on the render button to generate an image and verify that everything is installed and configured correctly.
    
        Set up some cameras. It is preferable to adopt at least one camera from the Render Workbench so that the recording position (the point of observation) is not lost afterwards. Position and configure each of the camera(s) that you want to use in recording the animation.

        Adjust the 'Aspec Ratio' of each one of them according to the proportion that you will use between the widths and heights in pixels of the future frames (for example 1.33 for 800x600). If you want to have a more accurate idea of the final result, adjust the 'Viewport Mapping' of the camera to 'CROP_VIEW_FILL_FRAME' or 'CROP_VIEWPORT_LINE_FRAME' and update the view by clicking on 'set GUI to this camera' (pop menu opened with the right mouse button on the camera icon).

        However, it is good to point out that there is still a difference between the camera views in FC's 3D View and those in the render windows. To try to correct this, duplicate the 3D view cameras and adjust the copies with a more distant view, testing each one of them until an adequate similarity is reached.
     
2. Usage

    2.1. Create and configure the clapperboard

        Create a general animation recording configuration using the Clapperboard, clicking on its icon, Menu - Movie - Clapperboard or in the pop-up menu opened with the right mouse button.

        Configure the Clapperboard properties window according to the guidelines ('tips') for each one and your needs. It comes almost completely pre-configured, however the paths for saving the generated frames and videos must be indicated before starting any recording. After creating your first video, you can complete the last property, the path to play a video.
     
     2.2. Recording process

        Choose camera or 3D view and position your animation at the desired step.

        Create the 3D view frames - R1. For a preview of the animation with frames of the 3D view, click on 'R1' (or menu Movie - Record 3DView Frames), choose or confirm the folder (that you've configured above) to salve the frames and start the animation (from a workbench, script or macro). The animation frames will be named and saved in the folder as configured in 'R1_5FrameOutpuPath' of the Clapperboard properties window. Messages on the bottom bar of the FC will show the recording progress, to better follow the process, open the report window.

        Create the video in FC. After finishing all desired animation recording steps, click on 'Create Video' (or Menu - Movie - Create Video), choose or confirm the input frames folder (indicated in Video 'InputFrames' of the Clapperboard). After finishing the recording, a message in the report window will confirm the location where the file was saved. Important: it will be named and saved in the folder you configured before, respectively in Video Name and Video OutputPath of Clapperboard properties window.

        Play the video in the FC or an external program. Click on 'Play Video' (or Menu - Movie - Play Video or workbench pop menu) and choose the file you want to play, or directly click on the created video file to open it with your system's video playback program for confirmation of the result.If you prefer, you can also import the frames created into an external video editing program that you already know, or assemble the final video with the various partial footage from the cameras used and include the sound.

        Repeat the previous items using the render frames - R2. Once satisfied with the result of the animation of the 3D views of the FC, you can start recording the rendered frames, according to the Render project(s) chosen and already properly configured (s). Repeat the four previous steps, but now confirming the properties corresponding to the Render in the Clapperboard properties window (mainly Render 'FrameOutputPath'), use the cameras configured for the render and activate 'R2' (Record Render Frames).

        Stop recording. If you need or want to interrupt the recording process, click on 'Stop Recording' or type 'Crtl k. This command interrupts the recording, for the animation use the corresponding one of the workbench, script or macro used.

3. Observations

     3.1. As mentioned, the Movie Workbench relies on animation and rendering works done on other workbenches. After carrying out these and to improve the dynamics of the recording work, we suggest using the Movietools. If you want to record your animation only using the images of the 3D views of the FC without rendering them, you can include the 'Movietools' in the used animation workbench, through Menu - Tools - Customize or, on the contrary, bring the animation toolbar to the Movie Workbench. But if you want to use one or more cameras and/or render animation frames, you will also need to include the Render toolbar.

     3.2. Usage of Render POV-Ray. In addition to already mentioned, you must configure for the render window not remains open after completion, deleting the '+P' in the 'Render parameters' field of the FC preferences.

     For the Windows version, it will also be necessary to configure the POV-Ray Gui to close after the rendering is finished. To do so, open the POV-Ray GUI, go to the render settings (menu - Render), click 'On Completion' and enable 'Exit POV-Ray for Windows'. Also disable all sound warnings (in Render menu - 'SoundSettings...') and any message openings that may appear after each completed render.

     3.3. Usage of other renderers. Still are necessary adjustments for animation, mainly the inclusion of work halt instructions (sample numbers, time or noise level - denoising) and automatic closing of the program window. If anyone knows how and wants to contribute, please post the instructions in the FC forum (https://forum.freecadweb.org/viewtopic.php?f=8&t=74432).

4. Installation of the Movie Workbench and download the test file
    
     4.1. The Movie Workbench is available at https://github.com/Francisco-Rosa/FreeCAD-Movie, but you can install it through the addon manager within the FC: Menu Tools - Addon Manager.

     4.2. The ExplodedAssembly workbench modified and prepared for recording is available at: https://github.com/Francisco-Rosa/ExplodedAssembly

     If you have mastery over the functioning of the different python files of worthe benches contained in the Mod folder of FC, you can only replace the modified file ('ExplodedAssembly.py'), first of all, save the original file or rename it, adding a _orig, for example.

     4.3. Test file. A file (that uses the ExplodedAssembly Workbench animation) is prepared to test the Movie workbench, just download it (from https://forum.freecadweb.org/viewtopic.php?f=8&t=74432) and configure the clapperboard for your machine.

5. How to integrate your animation with Movie Workbench:

     5.1. The idea is that the workbench record an image of each step of the created animation (frame). For this happens, it is necessary to insert the following lines in the code of the animation workbench, script or macro used:

         #At the beginning:

         import RecordPlayVideo as rpv

         #Inside the command to start the animation, two more insertions, one before the loop (to generate frame 1) and another at the end of each step (other frames):

         if 'Clapperboard' in FreeCAD.ActiveDocument.Content:
             CL = FreeCAD.ActiveDocument.Clapperboard
             if CL.Cam_3OnRec == True:
                 rpv.runRecordCamera()
  
         #After the animation loop and inside the instruction for halting the animation (pause and/or stop), include:
  
         if 'Clapperboard' in FreeCAD.ActiveDocument.Content:
             rpv.stopRecordCamera()

     5.2. You also can see the example applied to the ExplodedAssembly Workbench in the link mentioned.
