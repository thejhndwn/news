import bpy

# Use the current scene (already loaded)
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = 240  # 10 seconds at 24 FPS


# Find Armature and Camera
armature = bpy.data.objects.get("Armature")  # Adjust name if needed
if not armature:
    raise Exception("Armature not found! Check name in Outliner.")

camera = bpy.data.objects.get("Camera")
if not camera:
    raise Exception("Camera not found!")
scene.camera = camera

# Switch to Pose Mode
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

# Access Arm Bones
left_arm = armature.pose.bones.get("J_Bip_L_UpperArm")
right_arm = armature.pose.bones.get("J_Bip_R_UpperArm")
if not left_arm or not right_arm:
    print("Bones not found! Available bones:")
    for bone in armature.pose.bones:
        print(bone.name)
    raise Exception("Check bone names above and update script.")

# Animation
scene.frame_set(0)
left_arm.rotation_euler = (0, 0, 0)
right_arm.rotation_euler = (0, 0, 0)
left_arm.keyframe_insert(data_path="rotation_euler", frame=0)
right_arm.keyframe_insert(data_path="rotation_euler", frame=0)

scene.frame_set(120)  # Halfway (5 seconds)
left_arm.rotation_euler = (0, 0, -1.5708)  # -90 degrees (left arm up)
right_arm.rotation_euler = (0, 0, 0)  # Right arm stays still
left_arm.keyframe_insert(data_path="rotation_euler", frame=120)
right_arm.keyframe_insert(data_path="rotation_euler", frame=120)

scene.frame_set(240)  # End (10 seconds)
left_arm.rotation_euler = (0, 0, 0)
right_arm.rotation_euler = (0, 0, 0)
left_arm.keyframe_insert(data_path="rotation_euler", frame=240)
right_arm.keyframe_insert(data_path="rotation_euler", frame=240)

# Rendering Setup
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.filepath = "/home/john-duan/Celia/news/output/video/blendertest.mp4"
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'

# Render
bpy.ops.render.render(animation=True)
print("Rendering complete! Check:", scene.render.filepath)