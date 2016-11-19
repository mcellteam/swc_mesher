# SWC Mesher
## Notes

The SWC Mesher control panel contains 2 primary subpanels:

 * **Import Cable Model from SWC File**
 * **Edit Cable Model**

![Panel](../images/controls.png?raw=true "Control Panel")

The **Import Cable Model from SWC File** section is used to select SWC files and read them into memory.
It also shows the number of non-comment lines, the number of segments, the largest and smallest radius, and the bounding box size in x, y, and z.
The **Analyze File** button will re-read the file (in case it's been changed) and update the displayed values.

The **Make Cable Model from File** button will create a cable model in Blender. The skeleton will contain all the points and segments from the original file.

The **Edit Cable Model** section contains tools to edit the cable model, as well as tools to extrapolate a surface mesh from the cable. For details on editing the cable model, see the * **[Description/Tutorial](../description)**.

The **"Make Surface Mesh from File"** button
will generate a surface mesh from the currently selected file. The **"Make Surface Mesh from Data"** button will generate a surface mesh from the
current centerline data (or skeleton). This allows comparison of changes made to the current skeleton. Note, however, that because of the way
Blender implements the "meta" objects, there can only be one object in the "meta" state. Additional meta objects will be merged into any existing
meta objects. So if multiple surface objects are to be compared, each one should first be converted to a Blender mesh object
(Object / Convert To / Mesh from ...) before making another surface mesh via these buttons.

The **Surface Mesh** section contains 4 settings that control the mesh generation:

  * **Scale File Factor** (defaults to 1.0)
  * **Resolution of the Final Mesh** (defaults to 0.1)
  * **Minimum Forced Radius** (defaults to 0)
  * **Limit Number of Segments** (defaults to 0)

The **Scale File Factor** setting allows neurons to be scaled prior to any subsequent processing. This is helpful to match the neuron size to a
size appropriate for Blender's meta objects in the scene. This can be set based on the ranges for x, y, and z shown when a new file is opened.
The scale factor should generally be set so that the resulting neuron has a maximum dimension roughly larger than 1 and roughly smaller than 20.

The **Resolution of the Final Mesh** setting serves to guide how finely the meta objects represent themselves. It also controls spacing of points
in the mesh creation process. This value should generally be smaller than the radius of the smallest feature to be preserved in the neuron. If this
setting is too large, then thin portions of the neuron may be poorly represented or missed altogether. The following sequence of images shows
this setting for the P40_DEV360 neuron with values of 0.1, 0.2, 0.5, 0.8, and 1.0.

![Mesh0.1](../images/mesh_sample_at_0p1.png?raw=true "Mesh sampled at 0.1")
![Mesh0.2](../images/mesh_sample_at_0p2.png?raw=true "Mesh sampled at 0.2")
![Mesh0.5](../images/mesh_sample_at_0p5.png?raw=true "Mesh sampled at 0.5")
![Mesh0.8](../images/mesh_sample_at_0p8.png?raw=true "Mesh sampled at 0.8")
![Mesh1.0](../images/mesh_sample_at_1p0.png?raw=true "Mesh sampled at 1.0")

This next picture shows the meta objects that created the last picture (sampled at 1.0):

![Meta1.0](../images/meta_sample_at_1p0.png?raw=true "Meta sampled at 1.0")

As you can see, this setting is very important for obtaining valid meshes. It should be small enough to properly represent the smallest features
of the neuron, and large enough to not generate more mesh points and faces than needed.

The **Minimum Forced Radius** setting provides a means of sampling the neuron at a coarser resolution without causing breaks at narrow sections.
It does this by simply increasing the radius of small sections so they are at least the size of the **Minimum Forced Radius**. Consider the
following SWC file:

```
# Demonstrates a skinny segment
#
# # T     x     y    z     r   P
  1 3  -1.0   0.0  0.0  0.50  -1
  2 3  -0.5   0.0  0.0  0.50   1
  3 3   0.0   0.0  0.0  0.01   2
  4 3   0.5   0.0  0.0  0.50   3
  5 3   1.0   0.0  0.0  0.50   4
  6 3   1.25  0.0  0.0  0.50   5
```

The radius of each segment is 0.5 except for the very small section of 0.01 in the middle. Here's what it looks like when sampled at 0.01:

![Skinny0.01](../images/skinny_segment_0p01_fine.png?raw=true "Mesh sampled at 0.01")

That sampling will capture the fine segment, but it also generates a very dense mesh. However, if the mesh is sampled more coarsely, then
there may be missing parts as shown here when sampled at 0.1:

![Skinny0.1](../images/skinny_segment_0p01_mesh.png?raw=true "Mesh sampled at 0.1")

The gap results from an insufficient sampling of the meta objects themselves as shown here:

![Skinny0.1Meta](../images/skinny_segment_0p01_meta.png?raw=true "Meta sampled at 0.1")

If the small segment is known to be important, then the fine sampling of 0.01 is the best that can be done with the current software.
However, if it's suspected that these very small segments result from some sort of measurement error (and are not realistic), then 
the **Minimum Forced Radius** can be used to artificially increase the radius of those small segments before they are sampled by
Blender's meta objects. Here is that same object sampled at 0.1 but with the **Minimum Forced Radius** also set to 0.1.

![SkinnyMinForced0.1](../images/skinny_min_forced_0p1.png?raw=true "Minimum Forced to 0.1")

## Cautions

As with any tool, it's important to understand what it's doing and to verify that it is producing satisfactory results.

This neuron meshing tool has the following known problems:

  * Sampling must be appropriate for the features being represented (discussed above).
  * The meta objects can combine in ways that create variations in the radius (both larger and smaller than expected).
  * The ends of segments may vary in lengths as much as one radius.

Many of these problems can be caught by visually comparing the final mesh with the original centerline. It can help to have the
centerline selected (orange) while having the the mesh either semi-transparent or drawn as an unselected wireframe as shown here:

![MeshCenter](../images/mesh_and_centerline.png?raw=true "Mesh and Centerline for Comparison")



