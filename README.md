# Tonearm

Tonearm is a no nonsense Discord music bot that you can self-host.

Compared to most other music bots, Tonearm doesn't rely on Lavalink to play audio, but instead on [yt-dlp](https://github.com/yt-dlp/yt-dlp).

The docker images can be used on `amd64` and `arm64` systems.

## Starting the bot

You can run this bot using docker CLI, `docker compose` or directly on you host machine once the python package is installed.

### Startup parameters

| CLI flag              | Environment variable | Description                                                                                                      | Required | Default                  |
|-----------------------|----------------------|------------------------------------------------------------------------------------------------------------------|----------|--------------------------|
| `--discord-token`     | `DISCORD_TOKEN`      | The Discord bot token used to access the Discord API                                                             | Yes      |                          |
| `--log-level`         | `LOG_LEVEL`          | The log level used for the bot                                                                                   | No       | `INFO`                   |
| `--youtube-api-key`   | `YOUTUBE_API_KEY`    | YouTube API key used to fetch video metadata, playlists and search                                               | Yes      |                          |
| `--ffmpeg-executable` | `FFMPEG_EXECUTABLE`  | ffmpeg executable. This can also be a full path to the executable file                                           | No       | `ffmpeg`                 |
| `--youtube-cookies`   | `YOUTUBE_COOKIES`    | Path to the YouTube cookies file to use to avoid content restrictions or bot detection                           | No       |                          |
| `--data-path`         | `DATA_PATH`          | Path where Tonearm will store its configuration files                                                            | No       | `.` (`/data` for Docker) |
| `--buffer-length`     | `BUFFER_LENGTH`      | Length (in seconds) of the audio buffer in seconds. This is useful to control how much memory is used by the bot | No       | `7200` (2 hours)         |
| `--embed-color`       | `EMBED_COLOR`        | Color of the embeds sent by the bot. Error embeds are not affected by this setting and will always be red        | No       | `#71368A` (dark purple)  |
| `--status`            | `STATUS`             | Bot status (online, idle, ...)                                                                                   | No       | `online`                 |
| `--activity-type`     | `ACTIVITY_TYPE`      | Activity type that will be displayed on the bot status                                                           | No       | `listening`              |
| `--activity-name`     | `ACTIVITY_NAME`      | Activity name that will be displayed on the bot status                                                           | No       | `/play`                  |
| `--activity-state`    | `ACTIVITY_STATE`     | Activity state that will be displayed on the bot status, if custom activity type                                 | No       |                          |
| `--activity-url`      | `ACTIVITY_URL`       | Stream url that will be displayed if the activity type is streaming                                              | No       |                          |

### Docker CLI

```bash
docker run \
  -d \
  --name tonearm
  --restart unless-stopped \
  -e DISCORD_TOKEN=yourtoken \
  -e YOUTUBE_API_KEY=yourapikey \
  -v /opt/tonearm/tonearm:/data \
  ghcr.io/renaud11232/tonearm
```

### Docker compose

`compose.yaml`:

```yml
services:
  tonearm:
    image: ghcr.io/renaud11232/tonearm
    restart: unless-stopped
    environment:
      DISCORD_TOKEN: "yourtoken"
      YOUTUBE_API_KEY: "yourapikey"
    volumes:
      - /opt/tonearm/tonearm:/data
```

```bash
docker compose up -d
```

Check `compose.yaml` for a more complete example including all the required services and how to avoid getting blocked by Google, if you use a cloud VPS.

### Bare metal

Pick a version from the releases page and copy the link to the `.whl` file.
You can then install the bot by running the following command (creating a venv is highly recommended) :

```bash
pip install "https://github.com/Renaud11232/Tonearm/releases/download/<selected_version>>/tonearm-<selected_version>-py3-none-any.whl"
```

Once it's installed, you can start it either by setting the correct environment variables :

```bash
export DISCORD_TOKEN=yourtoken
export YOUTUBE_API_KEY=yourapikey
tonearm
```

Or by providing the corresponding flags :

```bash
tonearm \
  --discord-token "yourtoken" \
  --youtube-api-key "youapikey"
```