# infinitetrain-bot

Listen to [トレイン to トレイン](https://www.youtube.com/watch?v=LJ9vkt7BHYI) forever, now in your own Discord server.
Uses [infinitetrain](https://github.com/aixxe/infinitetrain)

## Requirements

- FFmpeg
- Python 3.10+
- Docker
- Built infinitetrain added to `INFINITETRAIN_PATH` environment variable (running local only)

Songs are not included in this repository due to copyright reasons. They should be placed in a folder named 
Tetsudou-Musume adjacent to the infinitetrain executable.

## How to Run

### With Docker Compose

- Create a .env file using the provided example.
- Run `docker compose up -d`

### Without Docker

- Clone this repo
- Create a new venv and run `pip install -r requirements.txt`
- Set the environment variables `DISCORD_TOKEN` and `INFINITETRAIN_PATH`
- Run `__main__.py`
