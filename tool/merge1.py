from moviepy.editor import VideoFileClip, AudioFileClip, clips_array
import os

root_path = r'E:\UserStudy'
video_path = os.path.join(root_path, 'Video')
audio_path = os.path.join(root_path, 'Audio')
output_path = os.path.join(root_path, 'Demo_ablation')

# test_seq_list = [
#     '4_lawrence_0_81_81', '4_lawrence_0_87_87'
# ]
# test_seq_list = [
#     '4_lawrence_0_4_4', '4_lawrence_0_73_73', '4_lawrence_0_81_81', '4_lawrence_0_87_87'
# ]
# test_seq_list = [
#     '2_scott_0_1_1', '2_scott_0_2_2', '2_scott_0_95_95',
#     '4_lawrence_0_1_1', '4_lawrence_0_2_2', '4_lawrence_0_95_95',
#     '6_carla_0_1_1', '6_carla_0_2_2', '6_carla_0_95_95',
#     '8_catherine_0_1_1', '8_catherine_0_2_2', '8_catherine_0_95_95',
#     '4_lawrence_0_4_4', '4_lawrence_0_73_73', '4_lawrence_0_81_81', '4_lawrence_0_87_87'
# ]

test_seq_list = [
    '2_scott_0_2_2', 
    '4_lawrence_0_4_4',
]

os.makedirs(output_path, exist_ok=True)

for pre in test_seq_list:
    if(os.path.exists(os.path.join(output_path, f'{pre}.mp4'))):
        continue
    
    print(f'Processing: {pre}...')

    # 加载3个视频并设置静音
    video1 = VideoFileClip(os.path.join(video_path, 'Ours_rymth', f'{pre}.mp4')).without_audio()
    video2 = VideoFileClip(os.path.join(video_path, 'Ours_rymth_sem', f'{pre}_merge_retrieval.mp4')).without_audio()
    video3 = VideoFileClip(os.path.join(video_path, 'Ours', f'{pre}_merge.mp4')).without_audio()

    # 获取所有视频的最短时长，并与目标时长比较
    min_duration = min(video1.duration, video2.duration, video3.duration)

    # 将视频剪裁为最短时长或目标时长
    video1 = video1.subclip(0, min_duration)
    video2 = video2.subclip(0, min_duration)
    video3 = video3.subclip(0, min_duration)

    # 定义裁剪比例（
    def crop_horizontal(video):
        width, height = video.size
        crop_margin = width // 8  
        return video.crop(x1=crop_margin, x2=width - crop_margin, y1=0, y2=height)

    # 裁剪视频左右两边
    video1 = crop_horizontal(video1)
    video2 = crop_horizontal(video2)
    video3 = crop_horizontal(video3)

    # 将视频水平拼接在同一行
    final_video = clips_array([[video1, video2, video3]])

    # 加载音频文件并剪裁到目标时长
    audio = AudioFileClip(os.path.join(audio_path, f'{pre}.wav'))
    if audio.duration > min_duration:
        audio = audio.subclip(0, min_duration)

    # 给视频添加音频
    final_video = final_video.set_audio(audio)

    # 导出合成后的视频
    final_video.write_videofile(os.path.join(output_path, f'{pre}.mp4'), fps=30, codec="libx264", audio_codec="aac")
