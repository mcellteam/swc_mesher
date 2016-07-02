# SWC Mesher
## Description

The SWC Mesher add-on can create both 3D centerline (stick figure) and 3D mesh representations of neurons from SWC files.
The meshes produced may be used directly with CellBlender or further improved with tools like GAMer.

## Short Tutorial

Start by enabling the add-on using the *File/User Preferences* menu and selecting the **Add Mesh** section and checking the box for the **SWC Mesher** add-on.

![Enable](../images/enable_addon.png?raw=true "Enable Addon")

Select the "SWC Mesher" tab along the left side of the 3D View:

![Installed](../images/newly_installed.png?raw=true "Newly Installed SWC Mesher")

Start by opening the **Original File** subpanel and use the file navigator to select an SWC format file:

![SelectFile](../images/select_a_file.png?raw=true "Selecting a File")

Navagate to an SWC file. In this example we'll use the P40-DEV360.CNG.swc.txt file shown here (copy and save as a text file for testing):

```
# SWC to SWC conversion from L-Measure. Sridevi Polavaram: spolavar@gmu.edu
# Original fileName:/cng_repository/Soumya/LM_Automated_Testing_Enviornment/Test_Lm3.7.2_10062011_SG_Linux_NMOConv6/TestResults/LoadTest/test_10/P40-DEV360.CNG.swc
#
# Original file P40_DEV360.swc edited by Duncan Donohue using StdSwc version 1.31 on 2/27/08.
# Irregularities and fixes documented in P40_DEV360.swc.std.  See StdSwc1.31.doc for more information.
#
# Neurolucida to SWC conversion from L-Measure. R. Scorcioni: rscorcio@gmu.edu
# Original fileName:C:\Users\Duncan\Desktop\Dat files to convert\Furtak 181 asc\P40_DEV360.ASC
#
  1 1 -0.78  -0.33 0    2.52262 -1
  2 1 -0.78   2.18 0    2.52262  1
  3 1 -0.78  -2.85 0    2.52262  1
  4 3  0      1.67 2.12 0.67     1
  5 3  0      4.68 2.12 0.67     4
  6 3  3.35   6.69 2.12 0.67     5
  7 3  3.35   9.02 2.12 0.67     6
  8 3  3.68   9.69 2.12 0.67     7
  9 3  4.01  10.37 2.12 0.67     8
 10 3 -0.33   8.69 2.12 0.67     5
 11 3  1.34   0.33 2.12 0.67     1
 12 3  2.34   0.33 2.12 0.67    11
 13 3  2.68   0.67 2.12 0.67    12
 14 3  3.35   1    2.12 0.67    13
 15 3  6.36   1    2.12 0.67    14
 16 3  6.69   1.34 2.12 0.67    15
 17 3 -0.67  -2.68 2.12 0.67     1
 18 3  3.35  -4.68 2.12 0.67    17
 19 3  4.85  -4.01 2.12 0.67    18
 20 3  6.36  -3.35 2.12 0.67    19
 21 3  6.69  -6.36 2.12 0.67    19
 22 3  3.68  -8.36 2.12 0.67    18
 23 3 -1.34  -2.34 2.12 0.67     1
 24 3 -1.34  -2    2.12 0.67    23
 25 3 -1.34  -6.02 2.12 0.67    24
 26 3  0    -10.03 2.12 0.67    25
 27 3 -3.01 -10.03 2.12 0.67    25
 28 3 -2.34   0.33 2.12 0.67     1
 29 3 -5.01   0.67 2.12 0.67    28
 30 3 -5.35   1    2.12 0.67    29
 31 3 -5.69   1    2.12 0.67    30
 32 3 -7.69   4.34 2.12 0.67    31
```

After opening that file, you should see an overview below the "Analyze File" button:

![Overview](../images/opened_P40.png?raw=true "Overview after opening")

This shows that the file contains 32 non-comment lines, 31 segments, and 32 nodes. The
largest radius of all nodes is 2.52, and the smallest is 0.67. The spatial extent of the
neuron is contained within the X, Y, and Z ranges shown.

You can create a line mesh object in Blender from that file by opening the **"Line Mesh"** 
panel and clicking the **"Make Line Mesh from File"** button as shown here:

![LineMesh](../images/make_line_mesh.png?raw=true "Making a Line Mesh")

You can create a surface mesh object in Blender from that file by opening the **"Surface Mesh"** 
panel and clicking the **"Make Surface Mesh from File"** button as shown here:

![SurfMesh](../images/make_surface_mesh.png?raw=true "Making a Surface Mesh")

As shown here, the add-on will create a series of "Meta" objects which form the surface of the Neuron. 
This isn't a mesh at this point, but can be easily converted to a mesh by selecting the object (right
clicking to turn from dark orange to lighter "gold") and then using the menu commands:

![Convert](../images/convert_to_mesh.png?raw=true "Convert Meta to Mesh")

The result will typically look the same, but it will now be a mesh. You can see the mesh itself by
entering "Edit" mode and zooming in:

![Converted](../images/converted_mesh.png?raw=true "Converted Mesh")
 
To use the mesh with CellBlender, it will need to be triangulated. You can do this by selecting 
everything in edit mode (the "a" key - should turn the entire mesh bright orange), then use the menu
to find *Mesh/Faces/Trianguate Faces* (or use control-t). The triangulated result for this model should
have 30,128 vertices, 90,378 edges, and 60,252 faces.

![Triangulated](../images/triangulated_mesh.png?raw=true "Triangulated Mesh")

This mesh can be used in CellBlender or MCell, but it has many more triangles than needed, and the
geometry is often poor quality for simulation. There are a number of ways to improve the mesh, and
the following picture show the result of applying the Coarse Dense, Coarse Flat, and Smooth operators
available in the Blender version of GAMER (https://github.com/mcellteam/gamer). Here's the final mesh:

![Gamer](../images/gamer_mesh.png?raw=true "Gamer Mesh")

The resulting Blender scene will contain both the outer mesh (shown unselected in black) and the original
centerline (shown selected in orange):

![MeshCenterline](../images/mesh_and_centerline.png?raw=true "Mesh and Centerline")

The resulting mesh can be added to a CellBlender project as part of a simulation:

![Simulate](../images/short_animation.gif?raw=true "CellBlender/MCell Simulation")

