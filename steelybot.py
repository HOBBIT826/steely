#!/usr/bin/env python3


from fbchat import log, Client
import imp
import config
import os
import random


class SteelyBot(Client):

    def __init__(self, *args, **kwargs):
        super(SteelyBot, self).__init__(*args, **kwargs)
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        for file in os.listdir('plugins'):
            if file.startswith("_"):
                continue
            elif not file.endswith(".py"):
                continue
            plugin_path = os.path.join('plugins', file)
            plugin = imp.load_source(file, plugin_path)
            self.plugins[plugin.COMMAND] = plugin

    def onEmojiChange(self, author_id, new_emoji, thread_id, thread_type, **kwargs):
        nose = '👃'
        if new_emoji != nose:
            self.changeThreadEmoji(nose, thread_id=thread_id)

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        if author_id == self.uid:
            return

        if message in ('.list', '.help'):
            commands = ', '.join((command for command in self.plugins.keys() if command))
            self.sendMessage('available commands: ' + commands, thread_id=thread_id, thread_type=thread_type)
            return

        if message == '.reload':
            self.load_plugins()
            self.sendMessage('plugins reloaded', thread_id=thread_id, thread_type=thread_type)
            return

        # run plugins that have no command
        for plugin in self.plugins.values():
            if not plugin.COMMAND:
                plugin.main(self, author_id, message, thread_id, thread_type, **kwargs)

        # run plugins that have a command
        try:
            command, message = message.split(' ', 1)
        except ValueError:
            command, message = message.strip(), ""
        if not command in self.plugins:
            return
        plugin = self.plugins[command]
        plugin.main(self, author_id, message, thread_id, thread_type, **kwargs)


if __name__ == '__main__':
    client = SteelyBot(config.EMAIL, config.PASSWORD)
    client.listen()
