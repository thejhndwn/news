
from staging_service.StagingService import StagingService
from content_service.ContentService import ContentService
from twitch_service.TwitchService import TwitchService

import time
from dotenv import load_dotenv
import os
from pathlib import Path
import argparse
import threading

class Orchestrator:
    def __init__(self):

        load_dotenv()
        WINDOWS_IP = os.getenv("WINDOWS_IP")
        VTS_PORT = os.getenv("VTS_PORT")
        VTS_AUTH_TOKEN = os.getenv("VTS_AUTH_TOKEN")
        OBS_WEBSOCKET_PASSWORD = os.getenv("OBS_WEBSOCKET_PASSWORD")
        OBS_WEBSOCKET_PORT = os.getenv("OBS_WEBSOCKET_PORT")
        TWITCH_KEY = os.getenv("TWITCH_KEY")


        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        TMP_DIR = project_root / "tmp"
        (TMP_DIR).mkdir(parents=True, exist_ok=True)
        (TMP_DIR / "audio").mkdir(parents=True, exist_ok=True)
        (TMP_DIR / "viseme").mkdir(parents=True, exist_ok=True)
        (TMP_DIR / "images").mkdir(parents=True, exist_ok=True)
        (TMP_DIR / "animation").mkdir(parents=True, exist_ok=True)

        self.content_service = ContentService(tmp_dir = TMP_DIR, output_path = TMP_DIR)
        self.staging_service = StagingService(output_path = TMP_DIR,
                                        windows_ip=WINDOWS_IP,
                                        vts_port=VTS_PORT,
                                        vts_auth_token=VTS_AUTH_TOKEN,
                                        obs_websocket_password=OBS_WEBSOCKET_PASSWORD,
                                        obs_websocket_port=OBS_WEBSOCKET_PORT,
                                        twitch_key=TWITCH_KEY)
        self.twitch_service = TwitchService(twitch_key = TWITCH_KEY)
        self.injection_queue = []
        self.input = {
                'm': self.story_injection_from_url,
                's': self.story_injection_from_uuid,
                'd': self.donation_shoutout,
                'e': self.expression_injection,
                'a': self.animation_trigger
                }

    # I want to inject: a story, a "scene" (donation shoutout, expression trigger, animation trigger)
    def injection(self):  
        while True:
            input = input("Inject something: make story from url(m,M), inject already made story by uuid(s,S), donation shoutout(d,D), trigger expression(e,E) or animation(a,A)").lower()
            if input not in self.input.keys():
                continue
            self.input[input]()

    def story_injection_from_url(self):
        # make story and add to all the necessary files
        url = input("please enter a url, or press d/D to go back").lower()
        if url == 'd':
            return
        story_id = self.content_service.make_story_from_url(url)
        self.injection_queue.append(story_id)

    def story_injection_from_uuid(self):
        story_id = input("please enter a story uuid, or press d/D to go back").lower()
        if story_id == 'd':
            return
        self.injection_queue.append(story_id)
        
        pass
    def expression_injection(self):
        expression_set = set()
        expression = ""
        while expression not in expression_set:
        # determine what expression 
            expression = input("please enter an expression, or press d/D to go back").lower()
            if expression == 'd':
                return
            if expression not in expression_set:
                continue
            # might need to open a new thread to send the expression request
            expression_injection = threading.Thread(target = self.staging_service.VTS.send_expression, args=(expression))
            expression_injection.start()
    def animation_trigger(self):
        animation_set = set()
        animation = input("please enter an animation, or press d/D to go back").lower()
        
        while animation not in animation_set:
        # determine what animation 
            animation = input("please enter an animation, or press d/D to go back").lower()
            if animation == 'd':
                return
            if animation not in animation_set:
                continue
            # might need to open a new thread to send the animation request
            animation_injection = threading.Thread(target = self.staging_service.VTS.send_animation, args=(animation))
            animation_injection.start()
        # open new thread to trigger custom scene
    def donation_shoutout(self):
        donations = self.twitch_service.get_donations()
        story_id=self.content_service.generate_donation(donations)
        self.injection_queue.append(story_id)

    def main_loop(self):
        try:
            if not args.stream:
                print("we are streaming btw")
                self.staging_service.start_streaming()
            while True:
                if self.injection_queue:
                    story_id = self.injection_queue.pop()
                else:    
                    story_id = self.content_service.get_story()
                self.staging_service.play_story(story_id)
                time.sleep(1) # idle buffer time between stories
        
        except KeyboardInterrupt:
            print("There was a manual stop. Shutting down...")

        finally:
            # cleanup
            self.content_service.cleanup()
            self.staging_service.cleanup()

    def run(self, args):
        if not args.stream:
            print("Starting up stream")
            self.staging_service.start_streaming

        input_thread = threading.Thread(target = self.injection, daemon = True)
        input_thread.start()

        self.main_loop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= " blank text")
    parser.add_argument('-s', '--stream', action = 'store_true', help= "stop streaming")
    args = parser.parse_args()

    orchestrator = Orchestrator()
    orchestrator.run(args)

