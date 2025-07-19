
from staging_service.StagingService import StagingService
from content_service.ContentSerivce import ContentService

import time
from dotenv import load_dotenv
import os


def main():

    load_dotenv()

    WINDOWS_IP = os.getenv("WINDOWS_IP")
    VTS_PORT = os.getenv("VTS_PORT")
    VTS_AUTH_TOKEN = os.getenv("VTS_AUTH_TOKEN")
    OBS_WEBSOCKET_PASSWORD = os.getenv("OBS_WEBSOCKET_PASSWORD")
    OBS_WEBSOCKET_PORT = os.getenv("OBS_WEBSOCKET_PORT")

    content_service = ContentService()
    staging_service = StagingService( windows_ip=WINDOWS_IP,
                                      vts_port=VTS_PORT,
                                      vts_auth_token=VTS_AUTH_TOKEN,
                                      obs_websocket_password=OBS_WEBSOCKET_PASSWORD,
                                      obs_websocket_port=OBS_WEBSOCKET_PORT)


    try:
        while True:
            story_id = content_service.get_story()
            StagingService.play_story(story_id)

            time.sleep(1) # idle buffer time between stories
    
    except KeyboardInterrupt:
        print("There was a manual stop. Shutting down...")

    finally:
        # cleanup
        content_service.cleanup()
        staging_service.cleanup()
    



if __name__ == '__main__':
    main()