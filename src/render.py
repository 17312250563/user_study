import bpy
import os
import math

def import_bvh(filepath):
    bpy.ops.import_anim.bvh(filepath=filepath)
    
    # 应用变换
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

def retarget_animation(source, target):
    if source not in bpy.data.objects or target not in bpy.data.objects:
        print(f"Error: One or both of the armatures '{source}' or '{target}' do not exist.")
        return
    
    bpy.context.scene.rsl_retargeting_armature_source = bpy.data.objects[source]
    bpy.context.scene.rsl_retargeting_armature_target = bpy.data.objects[target]
    print('Source and target armatures set.')
    
    try:
        bpy.ops.rsl.build_bone_list()
        
        # semantic ges
        bpy.context.scene.rsl_retargeting_bone_list[7].bone_name_target = ""
        bpy.context.scene.rsl_retargeting_bone_list[11].bone_name_target = ""


#        bpy.context.scene.rsl_retargeting_bone_list[1].bone_name_target = "" # 避免重复映射
#        bpy.context.scene.rsl_retargeting_bone_list[5].bone_name_target = ""
        
        
        bpy.ops.rsl.retarget_animation()
        print("Animation retargeting completed.")
    except Exception as e:
        print(f"Error during retargeting: {e}")
        

def delete_object(obj_name):
    obj = bpy.data.objects.get(obj_name)

    if obj:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.delete()
        print(f"Object '{obj_name}' has been deleted.")
    else:
        print(f"Object '{obj_name}' not found for deletion.")

def remove_existing_objects(obj_name_prefix):
    # 创建一个要删除的对象列表
    objects_to_delete = [obj for obj in bpy.data.objects if obj.name.startswith(obj_name_prefix)]
    
    # 检查列表是否为空
    if not objects_to_delete:
        print(f"No objects found with prefix '{obj_name_prefix}' to delete.")
        return
    
    # 现在迭代这个列表并删除对象
    for obj in objects_to_delete:
        obj.select_set(False)  # 确保对象不被选中
        if bpy.context.view_layer.objects.active == obj:
            bpy.context.view_layer.objects.active = None  # 设置一个不同的活动对象
        bpy.data.objects.remove(obj, do_unlink=True)
        
def clear_all_objects():
    # 确保处于对象模式
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # 选择所有对象
    bpy.ops.object.select_all(action='SELECT')
    
    # 删除所有选择的对象
    bpy.ops.object.delete()

def render_animation_to_mp4(output_path, resolution_x=1080, resolution_y=1080, resolution_percentage=100, engine='BLENDER_EEVEE_NEXT', start_frame=None, end_frame=None, fps=30):
    # 获取当前场景
    scene = bpy.context.scene

    # 设置输出路径（包括文件名和扩展名）
    scene.render.filepath = output_path

    # 设置分辨率
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.resolution_percentage = resolution_percentage

    # 设置渲染引擎
    scene.render.engine = engine

    # 设置帧率
    scene.render.fps = fps

    # 设置视频格式为FFmpeg视频
    scene.render.image_settings.file_format = 'FFMPEG'

    # 设置编码格式为H.264
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'

    # 设置输出质量
    scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'  

    # # 设置音频编码（如果需要）
    # scene.render.ffmpeg.audio_codec = 'AAC'
    # scene.render.ffmpeg.audio_bitrate = 192

    # 设置渲染的帧范围
    if start_frame is None:
        start_frame = scene.frame_start
    if end_frame is None:
        end_frame = scene.frame_end

    # 渲染动画
    scene.frame_start = start_frame
    scene.frame_end = end_frame
    bpy.ops.render.render(animation=True)

if __name__ == '__main__': 
    source_directory_path = r'E:\UserStudy\Bvh'
    render_root_path = r'E:\UserStudy\Video'
    target = 'Armature.001'

    for root, dirs, files in os.walk(source_directory_path):
        for filename in files:
            if filename.endswith('.bvh'):
                method = os.path.basename(root)
                if method != 'semantic_gesticulator': continue
            
                source_path = os.path.join(root, filename)
                source = os.path.splitext(os.path.basename(source_path))[0] 
                render_path = os.path.join(render_root_path, method, f'{source}.mp4')
                os.makedirs(os.path.join(render_root_path, method), exist_ok=True)

                if os.path.exists(render_path): continue

                if bpy.context.object and bpy.context.object.mode != 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')
                        
                if source not in bpy.data.objects:
                    import_bvh(source_path) 
                
                retarget_animation(source, target) 
                render_animation_to_mp4(render_path)
                 
                if source in bpy.data.objects:
                    bpy.data.objects.remove(bpy.data.objects[source])
                
                break

