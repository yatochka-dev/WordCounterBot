# Project Title: Discord Leaderboard Bot

This project is a Discord bot written in Python using the disnake library. The bot tracks the usage of specific words by members in a Discord server and maintains a leaderboard of the top users.

## Features

- **Word Tracking**: The bot tracks the usage of specific words by members in a server. The words to track are defined in the `WORDs_TO_COUNT` list in `main.py`.

- **Leaderboard**: The bot maintains a leaderboard of the top users based on the usage of the tracked words. The leaderboard is stored in a JSON file (`counter.json`).

- **Commands**:
  - `/leaderboard`: This command displays the top 10 users with the most word usage in an embed message.
  - `/info`: This command displays the word usage of a specific user or the command invoker if no user is specified.

## Code Structure

The main functionality of the bot is encapsulated in the `LeaderBoard` class in `main.py`. This class handles the loading and saving of the leaderboard data, updating the word count for users, and generating the leaderboard.

The bot uses the disnake library's event system to listen for new messages and update the word count for users. It also provides slash commands for users to view the leaderboard and their word usage.

## Setup

1. Clone the repository.
2. Install the required Python packages using pip: `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory and add your Discord bot token like so: `DISCORD_TOKEN=your-bot-token`.
4. Run `main.py` to start the bot: `python main.py`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)