from paraview.simple import *
import os

foam_file = os.path.abspath("case.foam")
if os.path.exists(foam_file):
    reader = OpenFOAMReader(registrationName='case.foam', FileName=foam_file)
    reader.MeshRegions = ['internalMesh']
    
    scene = GetAnimationScene()
    scene.UpdateAnimationUsingDataTimeSteps()
    if scene.TimeKeeper.TimestepValues:
        scene.AnimationTime = scene.TimeKeeper.TimestepValues[-1]

    view = GetActiveViewOrCreate('RenderView')
    view.ViewSize = [1920, 1080]
    
    display = Show(reader, view)
    
    # Extract Pressure Screenshot
    ColorBy(display, ('CELLS', 'p'))
    view.ResetCamera()
    Render()
    SaveScreenshot("pressure_contour.png", view)

    # Extract Velocity Magnitude Screenshot
    ColorBy(display, ('CELLS', 'U'))
    Render()
    SaveScreenshot("velocity_contour.png", view)
    
    print("ParaView automated extraction complete: pressure_contour.png & velocity_contour.png saved.")
