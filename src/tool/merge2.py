from moviepy.editor import VideoFileClip, AudioFileClip, clips_array
import os

root_path = r'E:\UserStudy'
video_path = os.path.join(root_path, 'Video')
audio_path = os.path.join(root_path, 'Audio')
output_path = os.path.join(root_path, 'Demo')

test_seq_list = [
    '2_scott_0_1_1', 
    '4_lawrence_0_95_95',
]
os.makedirs(output_path, exist_ok=True)

for pre in test_seq_list:
    if(os.path.exists(os.path.join(output_path, f'{pre}.mp4'))):
        continue
    
    print(f'Processing: {pre}...')

    video0 = VideoFileClip(os.path.join(video_path, 'gt', f'{pre}.mp4')).without_audio()
    video1 = VideoFileClip(os.path.join(video_path, 'Ours', f'{pre}_merge.mp4')).without_audio()
    video2 = VideoFileClip(os.path.join(video_path, 'camn', f'{pre}.mp4')).without_audio()
    video3 = VideoFileClip(os.path.join(video_path, 'diffstylegesture+', f'{pre}.mp4')).without_audio()
    video4 = VideoFileClip(os.path.join(video_path, 'diffsheg', f'{pre}.mp4')).without_audio()
    video5 = VideoFileClip(os.path.join(video_path, 'semantic_gesticulator', f'{pre}_semantic_results.mp4')).without_audio()

    # 获取所有视频的最短时长，并与目标时长比较
    min_duration = min(video0.duration, video1.duration, video2.duration, video3.duration, video4.duration, video5.duration)

    # 将视频剪裁为最短时长或目标时长
    video0 = video0.subclip(0, min_duration)
    video1 = video1.subclip(0, min_duration)
    video2 = video2.subclip(0, min_duration)
    video3 = video3.subclip(0, min_duration)
    video4 = video4.subclip(0, min_duration)
    video5 = video5.subclip(0, min_duration)

    # 定义裁剪比例（
    def crop_horizontal(video):
        width, height = video.size
        crop_margin = width // 8  
        return video.crop(x1=crop_margin, x2=width - crop_margin, y1=0, y2=height)

    # 裁剪视频左右两边
    video0 = crop_horizontal(video0)
    video1 = crop_horizontal(video1)
    video2 = crop_horizontal(video2)
    video3 = crop_horizontal(video3)
    video4 = crop_horizontal(video4)
    video5 = crop_horizontal(video5)

    # 将视频水平拼接在同一行
    final_video = clips_array([[video0, video1, video2, video3, video4, video5]])

    # 加载音频文件并剪裁到目标时长
    audio = AudioFileClip(os.path.join(audio_path, f'{pre}.wav'))
    if audio.duration > min_duration:
        audio = audio.subclip(0, min_duration)

    # 给视频添加音频
    final_video = final_video.set_audio(audio)

    # 导出合成后的视频
    final_video.write_videofile(os.path.join(output_path, f'{pre}.mp4'), fps=30, codec="libx264", audio_codec="aac")
