
from staging_service.StagingService import StagingService
from content_service.ContentService import ContentService

import time
from dotenv import load_dotenv
import os
from pathlib import Path
import argparse

def main():

    load_dotenv()

    WINDOWS_IP = os.getenv("WINDOWS_IP")
    VTS_PORT = os.getenv("VTS_PORT")
    VTS_AUTH_TOKEN = os.getenv("VTS_AUTH_TOKEN")
    OBS_WEBSOCKET_PASSWORD = os.getenv("OBS_WEBSOCKET_PASSWORD")
    OBS_WEBSOCKET_PORT = os.getenv("OBS_WEBSOCKET_PORT")
    TWITCH_KEY = os.getenv("TWITCH_KEY")

    parser = argparse.ArgumentParser(description= " blank text")

    parser.add_argument('-s', '--stream', action = 'store_true', help= "stop streaming")
    args = parser.parse_args()

    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    TMP_DIR = project_root / "tmp"
    # check if tmp_dir/audio and tmp_dir/viseme exist, if not create them
    (TMP_DIR).mkdir(parents=True, exist_ok=True)
    (TMP_DIR / "audio").mkdir(parents=True, exist_ok=True)
    (TMP_DIR / "viseme").mkdir(parents=True, exist_ok=True)

    content_service = ContentService(tmp_dir = TMP_DIR, output_path = TMP_DIR)
    staging_service = StagingService(output_path = TMP_DIR,
                                    windows_ip=WINDOWS_IP,
                                    vts_port=VTS_PORT,
                                    vts_auth_token=VTS_AUTH_TOKEN,
                                    obs_websocket_password=OBS_WEBSOCKET_PASSWORD,
                                    obs_websocket_port=OBS_WEBSOCKET_PORT,
                                    twitch_key=TWITCH_KEY)

    try:
        if not args.stream:
            print("we are streaming btw")
            staging_service.start_streaming()
        while True:
            story_id = content_service.get_story()
            if story_id:
                print("got story_id: ", story_id)
            staging_service.play_story(story_id)

            time.sleep(1) # idle buffer time between stories
    
    except KeyboardInterrupt:
        print("There was a manual stop. Shutting down...")

    finally:
        # cleanup
        content_service.cleanup()
        staging_service.cleanup()
        # clean up tmp_dir




if __name__ == '__main__':
    main()
