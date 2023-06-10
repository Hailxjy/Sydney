# README.md

This is a Discord bot built using the `discord.py` library and the `poe` library. The bot is designed to process and respond to messages with the help of a language model (e.g., GPT-4). The bot also has the ability to change its mode, clear its conversation history, and handle backticks for code blocks.

## Features

- Change the bot's mode for different language models
- Clear the bot's conversation history for the current mode
- Process messages and respond using the selected language model
- Handles backticks for code blocks
- Has a few other commands and utilities

## Commands

- `.mode <mode>`: Changes the bot's mode to the specified mode.
- `.modes`: Lists all available modes.
- `.cleargpt`: Clears the conversation history for the current mode.

## Usage

To use this bot, you need to install the required libraries mentioned in the code and set up a Discord bot with the appropriate token. Once the bot is invited to a server, it will listen for messages and process them using the selected language model.

# TODO List

- [x] Set up the bot with `discord.py` and `poe` library
- [x] Implement commands to change the bot's mode, list modes, and clear conversation history
- [x] Process and respond to messages using the selected language model
- [x] Handle backticks for code blocks in the bot's responses
- [ ] Add error handling and logging for potential issues
- [ ] Implement additional features or commands as needed

## Additional Notes

The code provided contains some hard-coded values, such as the bot token, which should be replaced with environment variables or secure storage solutions for proper security. Also, it's important to note that the code uses the GPT-4 language model, and any future changes to the language model or the `poe` library may require adjustments to the code.
