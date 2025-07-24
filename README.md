# news

j methologies
## audio
[coquitts](https://github.com/coqui-ai/TTS)

## concerning model generation

if 2D:
    - we can draw the 9 important visemes, then use a viseme locator like [rhubarb-lip-sync](https://github.com/DanielSWolf/rhubarb-lip-sync?tab=readme-ov-file) to figure out the timings

if 3D:
    = generate a free vtuber via [VRoidStudio](https://vroid.com/en/studio)

# current services
news aggregation
story picking/priority
 twitch suggestions
content generation
 text generation
 audio generation
 video generation
production orchestration
streaming 

# flow and work
1. grab stories 
=> almost done, just need to finish the story grabbing
2. figure out which stories are important /relevant to air
=> just make a simple version, no priority for now
3. generate script based on previous on-board stories and context
=> just make a simple version for now
4. convert to audio
=> todo
5. generate lip movements markers
=> use the rhubarb thing for this
(5a) generate sentiment markers for model actions
6. generate video based on markers, and tie with audio
=> todo
7. stream
=> todo

other features
1. user donations get shoutouts in sponsored segments
2. donators can suggest stories to be queued 


release stages
1. stream to twitch as a radio for one story
2. add continuous stories
3. add video
4. add twitch interactivity
5. add text improvements
6. add story selection improvements

eureka, you can stream mp4 to twitch via ffmpeg and a URL with your twitch stream key
