import math
import mathutils
import time

import bpy
from bpy.props import *
import bmesh

from bpy_extras.io_utils import ExportHelper

class MakeNeuronMeta_Panel(bpy.types.Panel):
	bl_label = "Neuron Launcher - SWC Mesher"

	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Neuron Launcher"

	@classmethod
	def poll(cls, context):
		return (context.scene is not None)

	def draw(self, context):
		mnm = context.scene.make_neuron_meta
		mnm.draw ( self.layout )

class MakeNeuronStick_Operator ( bpy.types.Operator ):
	bl_idname = "mnm.make_line_mesh"
	bl_label = "Make Line Mesh from File"
	bl_description = "Generate a skeleton of line segments from the SWC file directly"
	bl_options = {"REGISTER", "UNDO"}
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "objectmode"

	def execute ( self, context ):
		mnm = context.scene.make_neuron_meta
		mnm.build_neuron_stick_from_file ( context )
		return {"FINISHED"}

	def invoke ( self, context, event ):
		mnm = context.scene.make_neuron_meta
		mnm.build_neuron_stick_from_file ( context )
		return {"FINISHED"}

# Class to make spheres
class MakeSpheres_Operator( bpy.types.Operator ):
	bl_idname = "mnm.make_spheres"
	bl_label = "Make spheres for each vertex"
	bl_description = "Generate a sphere at each vertex of the cable model"
	bl_options = {"REGISTER", "UNDO"}
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "objectmode"

	def execute ( self, context ):
		mnm = context.scene.make_neuron_meta
		mnm.make_spheres_from_object ( context )
		return {"FINISHED"}

	def invoke ( self, context, event ):
		mnm = context.scene.make_neuron_meta
		mnm.make_spheres_from_object ( context )
		return {"FINISHED"}

# Class to update the cable model from the sphere locations/radii
class UpdateCableFromSpheres_Operator( bpy.types.Operator ):
	bl_idname = "mnm.update_cable"
	bl_label = "Update cable from spheres"
	bl_description = "Update the cable model from sphere locations/radii"
	bl_options = {"REGISTER", "UNDO"}
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "objectmode"

	def execute ( self, context ):
		mnm = context.scene.make_neuron_meta
		mnm.update_cable_model_from_spheres ( context )
		return {"FINISHED"}

	def invoke ( self, context, event ):
		mnm = context.scene.make_neuron_meta
		mnm.update_cable_model_from_spheres ( context )
		return {"FINISHED"}

# Export a cable model to SWC file
class ExportCableModel_Operator ( bpy.types.Operator , ExportHelper ):
	bl_idname = "mnm.export_swc"
	bl_label = "Export Cable Model to SWC file"
	bl_description = "Generate an SWC file of segments from the skeleton"
	
	filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

	filename_ext = ".swc" # allowed extensions

	def execute ( self, context ):

		# Check that an object is selected
		if context.scene.objects.active == None:
			raise TypeError("Please select the cable model to export.")

		# Export the SWC file
		context.scene.make_neuron_meta.export_cable_model(context, self.filepath)

		return {"FINISHED"}

	def invoke ( self, context, event ):

		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

# Class to show all vertex spheres
class ShowVertexSpheres_Operator( bpy.types.Operator ):
	bl_idname = "mnm.show_spheres"
	bl_label = "Show"
	bl_description = "Show all vertex spheres"
	bl_options = {"REGISTER", "UNDO"}
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "objectmode"

	def execute ( self, context ):
		mnm = context.scene.make_neuron_meta
		mnm.hide_vertex_spheres ( context, False )
		return {"FINISHED"}

	def invoke ( self, context, event ):
		mnm = context.scene.make_neuron_meta
		mnm.hide_vertex_spheres ( context, False )
		return {"FINISHED"}

# Class to hide all vertex spheres
class HideVertexSpheres_Operator( bpy.types.Operator ):
	bl_idname = "mnm.hide_spheres"
	bl_label = "Hide"
	bl_description = "Hide all vertex spheres"
	bl_options = {"REGISTER", "UNDO"}
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "objectmode"

	def execute ( self, context ):
		mnm = context.scene.make_neuron_meta
		mnm.hide_vertex_spheres ( context, True )
		return {"FINISHED"}

	def invoke ( self, context, event ):
		mnm = context.scene.make_neuron_meta
		mnm.hide_vertex_spheres ( context, True )
		return {"FINISHED"}

# Class to show all vertex spheres
class DeleteAllVertexSpheres_Operator( bpy.types.Operator ):
	bl_idname = "mnm.delete_all_spheres"
	bl_label = "Delete All"
	bl_description = "Delete all vertex spheres"
	bl_options = {"REGISTER", "UNDO"}
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "objectmode"

	def execute ( self, context ):
		mnm = context.scene.make_neuron_meta
		mnm.delete_vertex_spheres ( context )
		return {"FINISHED"}

	def invoke ( self, context, event ):
		mnm = context.scene.make_neuron_meta
		mnm.delete_vertex_spheres ( context )
		return {"FINISHED"}

class MakeNeuronMeta_Operator ( bpy.types.Operator ):
	bl_idname = "mnm.make_neuron_from_file"
	bl_label = "Make Surface Mesh from File"
	bl_description = "Generate a surface mesh from the SWC file"
	bl_options = {"REGISTER", "UNDO"}
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "objectmode"

	def execute ( self, context ):
		mnm = context.scene.make_neuron_meta
		segments = mnm.read_segments_from_file()
		mnm.build_neuron_meta_from_segments ( context, segments )
		return {"FINISHED"}

	def invoke ( self, context, event ):
		mnm = context.scene.make_neuron_meta
		segments = mnm.read_segments_from_file()
		mnm.build_neuron_meta_from_segments ( context, segments )
		return {"FINISHED"}

class MakeNeuronMeta_Operator ( bpy.types.Operator ):
	bl_idname = "mnm.make_neuron_from_data"
	bl_label = "Make Surface Mesh from Data"
	bl_description = "Generate a surface mesh from the current skeleton"
	bl_options = {"REGISTER", "UNDO"}
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "objectmode"

	def execute ( self, context ):
		mnm = context.scene.make_neuron_meta
		segments = mnm.read_segments_from_object(context)
		mnm.build_neuron_meta_from_segments ( context, segments )
		return {"FINISHED"}

	def invoke ( self, context, event ):
		mnm = context.scene.make_neuron_meta
		segments = mnm.read_segments_from_object(context)
		mnm.build_neuron_meta_from_segments ( context, segments )
		return {"FINISHED"}

class MakeNeuronMetaAnalyze_Operator ( bpy.types.Operator ):
	bl_idname = "mnm.analyze_file"
	bl_label = "Analyze File"
	bl_description = "Read the file to determine numbers of segments, nodes, and various size ranges"
	bl_options = {"REGISTER", "UNDO"}
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "objectmode"

	def execute ( self, context ):
		mnm = context.scene.make_neuron_meta
		mnm.read_segments_from_file()
		return {"FINISHED"}

	def invoke ( self, context, event ):
		mnm = context.scene.make_neuron_meta
		mnm.read_segments_from_file()
		return {"FINISHED"}


def file_name_change ( self, context ):
	mnm = context.scene.make_neuron_meta
	mnm.file_name_change()
	


class MakeNeuronMetaPropGroup(bpy.types.PropertyGroup):
	# frames_dir = StringProperty(name="frames_dir", default="")
	neuron_file_name = StringProperty ( subtype='FILE_PATH', default="", update=file_name_change)
	neuron_file_data = StringProperty ( default="" )

	convert_to_mesh = BoolProperty ( name="Convert to Mesh", default=False )
	show_analysis = BoolProperty ( default=False )
	show_stick    = BoolProperty ( default=False )
	show_create   = BoolProperty ( default=False )
	file_analyzed = BoolProperty ( default=False )
	num_lines_in_file = IntProperty ( default=-1 )
	num_segments_in_file = IntProperty ( default=-1 )
	num_nodes_in_file = IntProperty ( default=-1 )
	largest_radius_in_file = FloatProperty ( default=-1 )
	smallest_radius_in_file = FloatProperty ( default=-1 )
	min_x = FloatProperty ( default=-1 )
	max_x = FloatProperty ( default=-1 )
	min_y = FloatProperty ( default=-1 )
	max_y = FloatProperty ( default=-1 )
	min_z = FloatProperty ( default=-1 )
	max_z = FloatProperty ( default=-1 )
	
	scale_file_data = FloatProperty ( default=1.0, precision=4, description="Scale factor applied to data read from a file" )
	mesh_resolution = FloatProperty ( default=0.1, precision=4, description="Intended resolution of the final mesh" )
	min_forced_radius = FloatProperty ( default=0.0, precision=4, description="Smallest radius allowed in all segments (smaller forced up to this radius)" )
	num_segs_limit = IntProperty ( default=0, description="Only generate this number of segments (useful for testing settings in large neurons)" )


	def draw ( self, layout ):

		box = layout.box()
		row = box.row(align=True)
		row.alignment = 'LEFT'

		if not self.show_analysis:
			row.prop(self, "show_analysis", icon='TRIA_RIGHT', text="Original File", emboss=False)
		else:
			row.prop(self, "show_analysis", icon='TRIA_DOWN', text="Original File", emboss=False)

			#row = box.row()
			#row.label ( "Neuron File:" )

			row = box.row()
			row.prop ( self, "neuron_file_name", text="" )

			row = box.row()
			row.operator ( "mnm.analyze_file" )

			if self.file_analyzed:
				row = box.row()
				box = row.box()
				row = box.row()
				row.label ( "File contains " + str(self.num_lines_in_file) + " lines." )
				row = box.row()
				row.label ( "File contains " + str(self.num_segments_in_file) + " segments." )
				row = box.row()
				row.label ( "File contains " + str(self.num_nodes_in_file) + " nodes." )
				row = box.row()
				row.label ( "Largest radius is %g" % self.largest_radius_in_file )
				row = box.row()
				row.label ( "Smallest radius is %g" % self.smallest_radius_in_file )
				row = box.row()
				row.label ( "X range: %g to %g" % (self.min_x, self.max_x) )
				row = box.row()
				row.label ( "Y range: %g to %g" % (self.min_y, self.max_y) )
				row = box.row()
				row.label ( "Z range: %g to %g" % (self.min_z, self.max_z) )

		box = layout.box()
		row = box.row(align=True)
		row.alignment = 'LEFT'

		if not self.show_stick:
			row.prop(self, "show_stick", icon='TRIA_RIGHT', text="Line Mesh", emboss=False)
		else:
			row.prop(self, "show_stick", icon='TRIA_DOWN', text="Line Mesh", emboss=False)

			row = box.row()
			row.operator ( "mnm.make_line_mesh" )

			row = box.row()
			split = box.split()
			col = split.column(align=True)
			col.operator ( "mnm.make_spheres" )
			rw = col.row()
			rw.operator("mnm.show_spheres")
			rw.operator("mnm.hide_spheres")
			rw.operator("mnm.delete_all_spheres")

			row = box.row()
			row.operator ( "mnm.update_cable" )

			row = box.row()
			row.operator ( "mnm.export_swc" )

		box = layout.box()
		row = box.row(align=True)
		row.alignment = 'LEFT'

		if not self.show_create:
			row.prop(self, "show_create", icon='TRIA_RIGHT', text="Surface Mesh", emboss=False)
		else:
			row.prop(self, "show_create", icon='TRIA_DOWN', text="Surface Mesh", emboss=False)

			row = box.row()
			row.prop ( self, "scale_file_data", text="Scale File Factor" )
			row = box.row()
			row.prop ( self, "mesh_resolution", text="Resolution of the Final Mesh" )
			row = box.row()
			row.prop ( self, "min_forced_radius", text="Minimum Forced Radius" )
			row = box.row()
			row.prop ( self, "num_segs_limit", text="Limit Number of Segments" )
			#row = box.row()
			#row.prop ( self, "convert_to_mesh", text="Convert Meta to Mesh" )
			row = box.row()
			row.operator ( "mnm.make_neuron_from_file" )
			row.operator ( "mnm.make_neuron_from_data" )

	# Check that there are no duplicate vertices in the cable model (based on their id)
	def check_duplicate_verts( self, context ):

		# Try to get the object
		if bpy.data.objects.get("my_obj") is None:
			raise TypeError("Cannot get cable model object.")

		# Get the object
		ob = bpy.data.objects["my_obj"]

		# Get the idxs
		index_number_layer = ob.data.vertex_layers_float['index_number']
		n_v = len(ob.data.vertices)
		idx_vals = [index_number_layer.data[i].value for i in range(0,n_v)]

		# Check against duplicates
		if len(idx_vals) != len(set(idx_vals)):
			# Duplicates exist
			self.update_cable_model_post_extrusion(context)

		# No duplicates
		return

	# Update cable model post extrusion/deletion
	def update_cable_model_post_extrusion( self, context ):

		# Try to get the object
		if bpy.data.objects.get("my_obj") is None:
			raise TypeError("Cannot get cable model object.")

		# Get the object
		ob = bpy.data.objects["my_obj"]

		# Get the parent layer
		parent_index_layer = ob.data.vertex_layers_float['parent_index']

		# Get a list of all edge's vertex id pairs
		edge_vert_pair_list = [list(edge.vertices) for edge in ob.data.edges]

		# Get the idxs
		index_number_layer = ob.data.vertex_layers_float['index_number']

		# We need to start somewhere - choose the idx = 1 element to be the same
		# Find the idx = 1 element
		n_v = len(ob.data.vertices)
		idx_vals = [int(index_number_layer.data[i].value) for i in range(0,n_v)]
		i_start = idx_vals.index(1)

		# All vertices to check
		verts_check = [i_start]

		# Vertices we have already checked
		verts_done = []

		# Id dict from i in the object's vertex list to idx in the SWC file
		i_idx_dict = {}
		i_idx_dict[i_start] = 1

		# Current index number to assign
		idx_assign = 2

		# Go through all vertices
		while len(verts_check) > 0:

			# The vertex to check
			i_check = verts_check[0]
			idx_check = i_idx_dict[i_check]

			# Find all connecting edges
			i_conns = []
			for vs in edge_vert_pair_list:
				if vs[0] == i_check and not vs[1] in verts_done:
					i_conns.append(vs[1])
					verts_check.append(vs[1])
				elif vs[1] == i_check and not vs[0] in verts_done:
					i_conns.append(vs[0])
					verts_check.append(vs[0])

			# If there are any connecting vertices, store their index numbers and parent
			for i_conn in i_conns:
				# New index
				index_number_layer.data[i_conn].value = float(idx_assign)
				i_idx_dict[i_conn] = idx_assign
				idx_assign += 1

				# Get parent
				parent_index_layer.data[i_conn].value = float(idx_check)

			# Add to verts_done to ensure no repetition
			verts_done.append(i_check)

			# Delete this vertex to check
			del verts_check[0]

	# Add spheres to the cable model for visualizing the vertices
	def make_spheres_from_object( self, context ):

		# Try to get the object
		if bpy.data.objects.get("my_obj") is None:
			# The object is not foundmake it first
			self.build_neuron_stick_from_file(context)

		# Get the object
		ob = bpy.data.objects["my_obj"]

		# Ensure that the object is ok post any extrusion/deletion of vertices that may have occured
		self.check_duplicate_verts(context)

		# Radius layer
		radius_layer = ob.data.vertex_layers_float["radius"]

		# Id layer
		index_number_layer = ob.data.vertex_layers_float["index_number"]

		# Get the number of vertices (for naming purposes)
		n_v = len(ob.data.vertices)
		v_name = "%0"+str(len(str(n_v)))+"d"

		# Go through each vertex
		for i_v,v in enumerate(ob.data.vertices):

			# Get the pos
			loc = v.co
			# Get the radius
			r = radius_layer.data[i_v].value
			# Get the id
			idx = int(index_number_layer.data[i_v].value)

			# Make a sphere
			bpy.ops.mesh.primitive_uv_sphere_add(segments=16, 
				ring_count=8, 
				size=r, 
				enter_editmode=False, 
				location=tuple(loc))

			# Get the new object
			new_ob = context.active_object

			# Rename it appropriately
			new_ob.name = ("Vertex_" + v_name) % idx 

	# Update the cable model based on the sphere locations
	def update_cable_model_from_spheres( self, context ):

		# Try to get the object
		if bpy.data.objects.get("my_obj") is not None:

			# Get the object
			ob = bpy.data.objects["my_obj"]

			# Get the number of vertices (for naming purposes)
			n_v = len(ob.data.vertices)
			v_name = "%0"+str(len(str(n_v)))+"d"

			# New positions, radii of the vertices
			new_pos_dict = {}
			new_r_dict = {}

			# Go through all the vertices
			for i_v in range(1,n_v+1):

				# Vertex sphere name
				sphere_name = ("Vertex_" + v_name) % i_v

				# Get the sphere object
				if bpy.data.objects.get(sphere_name) is None:
					# Couldn't get the object; stop
					break

				# Get the object
				ob_sphere = bpy.data.objects[sphere_name]

				# Calculate it's radius
				dim = ob_sphere.dimensions
				# scale = ob_sphere.scale
				r = sum([0.5*dim[i] for i in [0,1,2]]) / 3.0

				# Store
				new_pos_dict[i_v] = ob_sphere.location
				new_r_dict[i_v] = r

			# Update the vertex data on the cable model

			# Radius layer
			radius_layer = ob.data.vertex_layers_float["radius"]

			# Id layer
			index_number_layer = ob.data.vertex_layers_float["index_number"]

			# Go through all the vertices
			for i_v, v in enumerate(ob.data.vertices):

				# Get the index
				idx = int(index_number_layer.data[i_v].value)

				# Update the position
				v.co = mathutils.Vector(new_pos_dict[idx])

				# Update the radius - FOR WHATEVER REASON, WE ACTUALLY STORE TWICE THE RADIUS HERE
				radius_layer.data[i_v].value = new_r_dict[idx]


	# Export a cable model to an SWC file
	def export_cable_model( self, context, fpath ):

		# Construct the file to open
		if fpath[-4:] != ".swc":
			fpath += ".swc"

		# Write things
		file_lines = self.get_swc_from_mesh_stick ( context )
		if file_lines == None:
			print ( "Unable to save file" )
		else:
			f = open(fpath, "w")
			for l in file_lines:
				f.write ( l + "\n" )
			f.close()

	# Show/Hide all vertex spheres
	def hide_vertex_spheres(self, context, flag):

		# Go through all objects
		for ob in bpy.data.objects:
			if len(ob.name) >= 6 and ob.name[0:6] == "Vertex":
				ob.hide = flag

	# Delete all vertex spheres
	def delete_vertex_spheres(self, context):

		# Ensure object mode
		bpy.ops.object.mode_set(mode='OBJECT')

		# Current selection, and ensure everything is DE-selected
		ob_sel_list = []
		for ob in bpy.data.objects:
			if ob.select == True:
				ob_sel_list.append(ob.name)
				# Deselect the object
				ob.select = False

		# Go through all objects and delete
		for ob in bpy.data.objects:
			if len(ob.name) >= 6 and ob.name[0:6] == "Vertex":
				ob.hide = False
				ob.select = True
				bpy.ops.object.delete()

		# Reselect
		for ob in bpy.data.objects:
			if ob.name in ob_sel_list:
				ob.select = True

	def file_name_change ( self ):
		self.read_segments_from_file()
		# self.file_analyzed = True

	def read_segments_from_object ( self, context ):
		# Read in the data
		segments = []
		
		print ( "Reading from active object" )

		if context.scene.objects.active == None:
			print ( "Select a mesh object to make active" )
		elif context.scene.objects.active.type != 'MESH':
			print ( "Active object is not a mesh" )
		else:
			obj = context.scene.objects.active
			mesh = obj.data
			verts = mesh.vertices
			print ( "Mesh has " + str(len(verts)) + " verts" )

			index_number_layer = mesh.vertex_layers_float['index_number']
			parent_index_layer = mesh.vertex_layers_float['parent_index']
			segment_type_layer = mesh.vertex_layers_float['segment_type']
			#packed_layer = mesh.vertex_layers_int['packed_data']
			radius_layer = mesh.vertex_layers_float['radius']

			self.num_nodes_in_object = 0
			num_total_segments = 0

			# Start by putting all points into a dictionary keyed by their label n

			point_dict = {}
			i = 0
			for v in verts:
				# Fields: n T x y z R P

				n = int(index_number_layer.data[i].value)
				# n = (packed_layer.data[i].value >> 17) & 0x03fff
				T = int(segment_type_layer.data[i].value)
				# T = packed_layer.data[i].value & 0x07
				x = v.co.x
				y = v.co.y
				z = v.co.z
				R = radius_layer.data[i].value
				P = int(parent_index_layer.data[i].value)
				# P = (packed_layer.data[i].value >> 3) & 0x03fff

				# For some reason, many of these fields need to be swapped!!

				#fields = [ str(int(P)), str(int(T)), str(x), str(y), str(z), str(int(n)), str(R) ]
				fields  = [ str(int(n)), str(int(T)), str(x), str(y), str(z), str(R), str(int(P)) ]

				print ( "  Fields from " + obj.name + " = " + str(fields) )
				point_dict[fields[0]] = fields
				i += 1

			sorted_int_keys = sorted ( [ int(k) for k in point_dict.keys() ] )
			point_keys = ( [ str(k) for k in sorted_int_keys ] )
			self.num_lines_in_file = len(point_keys)
			self.num_nodes_in_file = len(point_keys)

			# Next create the list of segments - one for each child that has a parent
			for k in point_keys:
				child_fields = point_dict[k]
				print ( "  Sorted Fields from " + obj.name + " = " + str(child_fields) )
				if child_fields[6] in point_keys:
					# This point has a parent, so make a segment from parent to child
					parent_fields = point_dict[child_fields[6]]
					px = float(parent_fields[2])
					py = float(parent_fields[3])
					pz = float(parent_fields[4])
					pr = float(parent_fields[5])
					cx = float(child_fields[2])
					cy = float(child_fields[3])
					cz = float(child_fields[4])
					cr = float(child_fields[5])
					segments = segments + [ [ [px, py, pz, pr], [cx, cy, cz, cr] ] ]
					num_total_segments += 1

			if self.num_segs_limit > 0:
				# Limit the number of segments
				segments = segments[0:self.num_segs_limit]
				num_total_segments = len(segments)

			self.num_segments_in_file = num_total_segments

			self.perform_analysis ( segments )

		return segments



	def read_segments_from_file ( self ):
		# Read in the data
		segments = []
		
		print ( "Reading from file " + self.neuron_file_name )

		self.num_nodes_in_file = 0
		num_total_segments = 0

		if (self.neuron_file_name[-4:] == ".nbf"):

			# Read Node Branch Format
			# Node Branch Format has explicit connections, but they're not needed with metaballs
			segment = []
			f = open ( self.neuron_file_name, 'r' )
			lines = f.readlines();
			self.num_lines_in_file = len(lines)
			for l in lines:
				l = l.strip()
				print ( "Line: " + l )
				if len(l) > 0:
					if l[0:6] == "Branch":
						print ( "Branch" )
						if len(segment) > 0:
							segments = segments + [ segment ]
							segment = []
							num_total_segments += 1
					if l[0:4] == "Node":
						print ( "Node" )
						values = l.split()[1:]
						segment = segment + [ values ]
						self.num_nodes_in_file += 1
			if len(segment) > 0:
				segments = segments + [ segment ]
				segment = []
				num_total_segments += 1

		elif (self.neuron_file_name[-4:] == ".swc") or (self.neuron_file_name[-8:] == ".swc.txt"):

			# Read SWC Format
			# SWC format has explicit connections, but they're not needed with metaballs
			"""
			The format of an SWC file is fairly simple. It is a text file consisting of 
			a header with various fields beginning with a # character, 
			and a series of three dimensional points containing 
			an index, radius, type, and connectivity information. 
			The lines in the text file representing points have the following layout.

						n T x y z R P

						n is an integer label that identifies the current point and 
								increments by one from one line to the next.

						T is an integer representing the type of neuronal segment, 
								such as soma, axon, apical dendrite, etc. The standard 
								accepted integer values are given below.

								0 = undefined
								1 = soma
								2 = axon
								3 = dendrite
								4 = apical dendrite
								5 = fork point
								6 = end point
								7 = custom

						x, y, z gives the cartesian coordinates of each node.

						R is the radius at that node.
						P indicates the parent (the integer label) of the current 
								point or -1 to indicate an origin (soma).
			"""
			# Note that the SWC format could define cyclic references,
			#   However, since we just need to generate segments, this is not a problem.
			#   This is done by making each segment only one line (from parent to child)
			
			# Start by reading all the points into a dictionary keyed by their label n

			f = open ( self.neuron_file_name, 'r' )
			lines = f.readlines();
			point_dict = {}
			for l in lines:
				l = l.strip()
				print ( "Line: " + l )
				if len(l) > 0:
					if l[0] != "#":
						fields = l.split()
						point_dict[fields[0]] = fields
			point_keys = sorted ( [ k for k in point_dict.keys() ] )
			self.num_lines_in_file = len(point_keys)
			self.num_nodes_in_file = len(point_keys)

			# Next create the list of segments - one for each child that has a parent
			for k in point_keys:
				child_fields = point_dict[k]
				if child_fields[6] in point_keys:
					# This point has a parent, so make a segment from parent to child
					parent_fields = point_dict[child_fields[6]]
					px = float(parent_fields[2])
					py = float(parent_fields[3])
					pz = float(parent_fields[4])
					pr = float(parent_fields[5])
					cx = float(child_fields[2])
					cy = float(child_fields[3])
					cz = float(child_fields[4])
					cr = float(child_fields[5])
					segments = segments + [ [ [px, py, pz, pr], [cx, cy, cz, cr] ] ]
					num_total_segments += 1

		else:

			# Read the legacy format found from early work with Neuron

			f = open ( self.neuron_file_name, 'r' )
			lines = f.readlines();
			self.num_lines_in_file = len(lines)
			num_entries_to_read = 0
			segment = []
			for l in lines:
				print ( "Line: " + l.strip() )
				if len(l.strip()) > 0:
					# This is a real line
					if num_entries_to_read == 0:
						# Look for a line containing a 1 and the number of fields
						fields = l.strip().split()
						if len(fields) != 2:
							print ( "Error: expected 2 values" )
						else:
							if int(fields[0]) != 1:
								print ( "Unexpected first value for line" + l )
							num_entries_to_read = int(fields[1])
							print ( "Read " + str(num_entries_to_read) )
							if len(segment) > 0:
								segments = segments + [ segment ]
								segment = []
								num_total_segments += 1
					else:
						# This is another entry in the current segment
						values = l.strip().split()
						segment = segment + [ values ]
						num_entries_to_read += -1
						self.num_nodes_in_file += 1
			if len(segment) > 0:
				# Be sure to save the last segment
				segments = segments + [ segment ]
				num_total_segments += 1

		if self.num_segs_limit > 0:
			# Limit the number of segments
			segments = segments[0:self.num_segs_limit]
			num_total_segments = len(segments)

		self.num_segments_in_file = num_total_segments

		self.perform_analysis ( segments )

		return segments



	def perform_analysis ( self, segments ):

		# Dump to compare:
		#print ( "========== DUMP OF SEGMENTS ==========" )
		#for seg in segments:
		#  print ( "Segment:" )
		#  for node in seg:
		#    print ( "  Node: " + str(node) )
		#print ( "======================================" )

		# Find the smallest radius

		seg_num = 1
		obj_name = None
		first_pass = True
		self.largest_radius_in_file = -1
		self.smallest_radius_in_file = -1
		self.min_x = self.max_x = self.min_y = self.max_y = self.min_z = self.max_z = -1
		for seg in segments:
			print ( "=== Finding bounds and smallest radius for segment " + str(seg_num) + " ===" )
			seg_num += 1
			lc = None
			cap1 = True
			for c in seg:
				x = float(c[0])
				y = float(c[1])
				z = float(c[2])
				r = float(c[3])
				if first_pass or (r > self.largest_radius_in_file):
					self.largest_radius_in_file = r
				if first_pass or (r < self.smallest_radius_in_file):
					self.smallest_radius_in_file = r
				if first_pass or (x < self.min_x):
					self.min_x = x
				if first_pass or (x > self.max_x):
					self.max_x = x
				if first_pass or (y < self.min_y):
					self.min_y = y
				if first_pass or (y > self.max_y):
					self.max_y = y
				if first_pass or (z < self.min_z):
					self.min_z = z
				if first_pass or (z > self.max_z):
					self.max_z = z
				first_pass = False

		print ( "X range: %g to %g" % (self.min_x, self.max_x) )
		print ( "Y range: %g to %g" % (self.min_y, self.max_y) )
		print ( "Z range: %g to %g" % (self.min_z, self.max_z) )
		print ( "Largest radius = " + str(self.largest_radius_in_file) )
		print ( "Smallest radius = " + str(self.smallest_radius_in_file) )

		self.file_analyzed = True



	# Convert the current stick mesh into an swc format file
	def get_swc_from_mesh_stick ( self, context ):

		# Check that each id is assigned to only one vertex
		self.check_duplicate_verts(context)

		# Store the SWC lines
		lines = []
		lines.append ( "# n T x y z R P" )

		# Get the object, vertices
		ob = context.scene.objects.active
		vs = ob.data.vertices
		
		# Get the data stored on the vertices
		radius_layer = ob.data.vertex_layers_float["radius"]
		index_number_layer = ob.data.vertex_layers_float["index_number"]
		parent_index_layer = ob.data.vertex_layers_float['parent_index']
		segment_type_layer = ob.data.vertex_layers_float['segment_type']

		# Index values
		n_idx = len(vs)
		id_value_list = [int(index_number_layer.data[i].value) for i in range(0,n_idx)]
		
		# Write all vertices
		idx = 1
		while idx < len(id_value_list)+1:
			i_v = id_value_list.index(idx)
			if idx == 1:
				lines.append("1 " + str(int(segment_type_layer.data[i_v].value)) + " " + str(vs[i_v].co.x) + " " + str(vs[i_v].co.y) + " " + str(vs[i_v].co.z) + " " + str(radius_layer.data[i_v].value) + " -1")
			else:
				lines.append(str(idx) + " " + str(int(segment_type_layer.data[i_v].value)) + " " + str(vs[i_v].co.x) + " " + str(vs[i_v].co.y) + " " + str(vs[i_v].co.z) + " " + str(radius_layer.data[i_v].value) + " " + str(int(parent_index_layer.data[i_v].value)))
			idx += 1

		return lines


	def build_neuron_stick_from_file ( self, context ):
		# Read once with standard code to update the display
		segments = self.read_segments_from_file()

		if (self.neuron_file_name[-4:] == ".swc") or (self.neuron_file_name[-8:] == ".swc.txt"):
			# Read again to get all the data needed for a stick figure
			
			# Start by reading all the points into a dictionary keyed by their label n

			f = open ( self.neuron_file_name, 'r' )
			file_lines = f.readlines();
			point_dict = {}
			point_keys = []
			point_num = 0
			for l in file_lines:
				l = l.strip()
				print ( "Line: " + l )
				if len(l) > 0:
					if l[0] != "#":
						fields = l.split() + [ str(point_num) ]
						point_dict[fields[0]] = fields
						point_keys.append ( fields[0] )
						point_num += 1
			self.num_lines_in_file = len(point_keys)
			self.num_nodes_in_file = len(point_keys)

			# Build the Blender mesh starting with the vertices

			print ( "Making the verts:" )

			verts = []
			for k in point_keys:
				p = point_dict[k]
				print ( str(p) )
				px = float(p[2])
				py = float(p[3])
				pz = float(p[4])
				pr = float(p[5])
				verts.append ( [ px, py, pz ] )

			print ( "Making the lines:" )

			lines = []
			for k in point_keys:
				p = point_dict[k]
				print ( str(p) )
				ppkey = p[6]
				if int(ppkey) >= 0:
					# This point has a parent, so make a line segment
					pp = point_dict[ppkey]
					lines.append ( [ int(pp[7]), int(p[7]) ] )

			print ( "Making the mesh:" )

			new_mesh = bpy.data.meshes.new ( "my_mesh" )
			new_mesh.from_pydata ( verts, lines, [] )
			new_mesh.update()
			new_obj = bpy.data.objects.new ( "my_obj", new_mesh )
			context.scene.objects.link ( new_obj )

			# Add the radius as the bevel weight, so the user can modify it
			idx = 0
			for k in point_keys:
				p = point_dict[k]
				# Get the vertex in the object
				v = new_obj.data.vertices[idx]
				idx += 1
				# Set the bevel weight
				v.bevel_weight = float(p[5])

			'''
			# All points
			point_list = list(point_dict.values())
			point_co_list = [mathutils.Vector([float(p[2]),float(p[3]),float(p[4])]) for p in point_list]
			print("------")
			print(point_co_list)
			# Go through all vertices
			for v in new_obj.data.vertices:
				# Get this vertex the point list
				print("Checking: " + str(v.co))
				for vo in point_co_list:
					if (v.co-vo).length < 0.001:
						# Get the index
						idx = point_co_list.index(v.co)
						# Set it's bevel weight
						v.bevel_weight = float(point_list[idx][5])
			'''
			print ( "Adding the metadata to each vertex:" )

			#  n T x y z R P

			mesh = new_obj.data
			index_number_layer = mesh.vertex_layers_float.new(name="index_number")
			parent_index_layer = mesh.vertex_layers_float.new(name="parent_index")
			segment_type_layer = mesh.vertex_layers_float.new(name="segment_type")
			# packed_layer = mesh.vertex_layers_int.new(name="packed_data")
			radius_layer       = mesh.vertex_layers_float.new(name="radius")

			vert_index = 0
			for k in point_keys:
				p = point_dict[k]
				print ( "Adding metadata from " + str(p) )
				index_number_layer.data[vert_index].value = int(p[0])
				parent_index_layer.data[vert_index].value = int(p[6])
				segment_type_layer.data[vert_index].value = int(p[1])
				#binary_value = (int(p[0]) << 17) | (int(p[6]) << 3) | (int(p[1]))
				#packed_layer.data[vert_index].value = binary_value
				radius_layer.data[vert_index].value = float(p[5])
				vert_index += 1

			#bpy.ops.object.mode_set()

	
	def build_neuron_meta_from_segments ( self, context, segments ):

		# segments = self.read_segments_from_file()

		# Create the object to hold the metaballs

		scene = bpy.context.scene
		mball = bpy.data.metaballs.new('neuron')
		obj = bpy.data.objects.new('Neuron',mball)
		scene.objects.link(obj)
		mball.resolution = self.mesh_resolution
		mball.render_resolution = self.mesh_resolution

		# Generate the metashape segments from the branch segments

		seg_num = 1
		obj_name = None
		for seg in segments:
			print ( "=== Building Branch " + str(seg_num) + " ===" )
			seg_num += 1
			lc = None
			for c in seg:
				if (lc != None):  # and (seg_num < 20):

					print ( "Building segment with radius of " + str(lc[3]) + " and " + str(c[3]) )

					x1 = float(lc[0]) * self.scale_file_data
					y1 = float(lc[1]) * self.scale_file_data
					z1 = float(lc[2]) * self.scale_file_data
					r1 = float(lc[3]) * self.scale_file_data
					x2 = float(c[0]) * self.scale_file_data
					y2 = float(c[1]) * self.scale_file_data
					z2 = float(c[2]) * self.scale_file_data
					r2 = float(c[3]) * self.scale_file_data

					# Make the segment from a series of meta balls

					segment_vector = mathutils.Vector ( ( (x2-x1), (y2-y1), (z2-z1) ) )
					segment_length = segment_vector.length

					# Be sure that the radiuses are non-zero
					if segment_length < 0:
						segment_length = 0.01
					if r1 < segment_length / 1000:
						r1 = segment_length / 1000
					if r2 < segment_length / 1000:
						r2 = segment_length / 1000

					if r1 < self.min_forced_radius:
						r1 = self.min_forced_radius
					if r2 < self.min_forced_radius:
						r2 = self.min_forced_radius

					dr = r2 - r1
					dx = x2 - x1
					dy = y2 - y1
					dz = z2 - z1

					r = r1
					x = x1
					y = y1
					z = z1

					length_so_far = 0
					while length_so_far < segment_length:
						# Make a sphere at this point
						ele = mball.elements.new()
						ele.radius = r
						ele.co = (x, y, z)
						
						# Move x, y, z, and r to the next point
						length_so_far += r/2
						r = r1 + (length_so_far * dr / segment_length)
						x = x1 + (length_so_far * dx / segment_length)
						y = y1 + (length_so_far * dy / segment_length)
						z = z1 + (length_so_far * dz / segment_length)

					# Make the last one just to be sure

					#ele = mball.elements.new()
					#ele.radius = r2
					#ele.co = (x2, y2, z2)

					# obj_name = self.add_segment ( obj_name, p1=mathutils.Vector((x1,y1,z1)), p2=mathutils.Vector((x2,y2,z2)), r1=r1, r2=r2, faces=10, cap1=cap1, cap2=True )
				lc = c

		if self.convert_to_mesh:
			bpy.ops.object.convert()

		obj.select = True
