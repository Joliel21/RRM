# Video background timing

- Background video: `public/images/background/rare-wave-intro.mp4`
- Video begins immediately when the reader loads.
- Magazine placement motion begins 1 second after video playback starts.
- Background blur begins 0.5 seconds before the 3.2-second magazine placement motion ends.
- The video pauses on its current frame when the magazine reaches its settled position.
- The paused background remains blurred at approximately 40% visual strength (`blur(4px)`).
- The still image in `publish_manifest.json` remains the poster/fallback background.
