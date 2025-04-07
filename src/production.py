
from production.ScriptGenerator import ScriptGenerator
from production.VideoGenerator import VideoGenerator

video_queue = []

def get_story():
    pass

def main():
    # story queuing
    # figures out what videos should content be generated for. 
    if len(video_queue) < 3:
        video_queue.append(get_story())
    
    # staging
    context = {}
    text = ScriptGenerator.generate(video_queue.pop(0), context)
    
    # content generation
    video = VideoGenerator.generate(text)

    # production orchestration
    # figures out what videos are queued to be played, if we need more video and all that





    
    pass



if __name__ == '__main__':
    main()