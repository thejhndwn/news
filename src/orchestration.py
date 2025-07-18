
from staging_service.StagingService import StagingService
from content_service.ContentSerivce import ContentService

import time


def main():
    content_service = ContentService()
    staging_service = StagingService()


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