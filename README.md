# infinitetrain-bot

Listen to [トレイン to トレイン](https://www.youtube.com/watch?v=LJ9vkt7BHYI) forever, now in your own Discord server.
Uses [infinitetrain](https://github.com/aixxe/infinitetrain)

## Requirements

- Built infinitetrain added to INFINITETRAIN_PATH environment variable
- FFmpeg
- Python 3.10+
- Docker (optional)

Songs are not included in this repository due to copyright reasons.

## How to Run

### With the Docker CLI

Recommends using external .env file with Docker due to security reasons.

```
# Pull from docker hub
$> docker pull misonoyuni/infinitetrain:latest

# Prepare built infinitetrain and songs data in ./data directory, and Setting.env file in root directory

# Settings.env
DISCORD_TOKEN=INSERT YOUR TOKEN HERE
INFINITETRAIN_PATH=/app/data/

# Run
$> docker run --name infinitetrain      \
              --volume ./data:/app/data \
              --env-file ./Settings.env \
              --detach                  \
              misonoyuni/infinite-train 
```
 
### Without the Docker CLI

- Clone this repo
- Create a new venv and run `pip install -r requirements.txt`
- Copy the .env example to `/src/` and add your Discord bot token
- Run `__main__.py`
