import bpy
import math

################# Basic conf ######################

render_data = True
objs = [ob for ob in bpy.context.scene.objects if ob.name in ('Camera', 'Sphere','LegoGroundPlane')]
bpy.ops.object.delete({"selected_objects": objs})
scene = bpy.context.scene

scene.render.resolution_x = 100 # camera width
scene.render.resolution_y = 100 # camera height
number_of_frames = 10 # number of frames to generate

############# list of objects init ################

lego_objects = []
for object in scene.objects:
    lego_objects.append(object)
    object.location = [0,0,object.dimensions.z/2]
    object.hide_render = True
    
################ Sphere init ######################

bpy.ops.mesh.primitive_uv_sphere_add(radius=10, enter_editmode=False, location=(0, 0, 0))
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.delete(type='ONLY_FACE')
bpy.ops.object.editmode_toggle()
sphere = bpy.data.objects['Sphere']

############### Camera init #######################

bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(0, 0, 0))
camera = bpy.data.objects['Camera']
bpy.context.scene.camera = bpy.data.objects['Camera']

camera.constraints.new(type='TRACK_TO')
camera.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
camera.constraints["Track To"].up_axis = 'UP_Y'

camera.data.type = 'ORTHO'

###### Camera looking from different angles #######

vp_vs = sphere.data.vertices
bpy.context.scene.frame_start=1
bpy.context.scene.frame_end=len(vp_vs)

for (f,v) in enumerate(vp_vs,1):
    camera.location = sphere.matrix_world @ v.co
    camera.keyframe_insert(data_path="location", frame=f)
    
################# Rendering #######################

if render_data:
    for object in lego_objects:
        bpy.context.scene.frame_end = number_of_frames
        object.hide_render = False
        camera.constraints["Track To"].target = object
        
        x = object.dimensions.x
        y = object.dimensions.y
        z = object.dimensions.z
        
        camera.data.ortho_scale = math.sqrt(x*x + y*y + z*z)
        
        for frame in range(1,scene.frame_end + 1):
            scene.frame_set(frame)
            scene.render.filepath = "/Users/blazejkustra/Desktop/" + object.name.strip('.dat') + '/' + str(frame) + '.png'
            bpy.ops.render.render(write_still = True)
        
        object.hide_render = True