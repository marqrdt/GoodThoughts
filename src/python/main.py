from desktop_notifier import DesktopNotifier, Urgency, Icon
import time
import asyncio
import signal
import json
import random
import logging
import sys

class GoodThoughtNotifier:
    def __init__(self, message_file=None):
        #asyncio.run(self.run())
        self.notifier = DesktopNotifier(app_name='Good Thoughts',notification_limit=10)
        self.messages_json = None
        self.rand = random.Random()
        try:
            self.messages_json = json.load(open(message_file))
        except Exception as error:
            print(f"Error loading message file: {error}")
            return None
        self.app_config = self.messages_json.get('app_config')
        self.app_name = self.app_config["app_name"]

    def get_random_message(self):
        messages_length = len(self.messages_json.get('messages'))
        return self.messages_json.get('messages')[ self.rand.randint(0, messages_length-1) ]['text']

    async def run(self):
        stop_event = asyncio.Event()
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, self.stop_app)
        loop.add_signal_handler(signal.SIGTERM, self.stop_app)
        while True:
            message = self.get_random_message()
            timeout_time = self.rand.randint(self.app_config["min_message_interval"], self.app_config["max_message_interval"])
            #print(f"notification id is {dtn.id}, summary is {dtn.summary}")
            #dtn.set_id(dtn.id).set_timeout(app_config["min_message_interval"])
            await asyncio.shield( self.notifier.send(
                title=self.app_name,
                message=message,
                timeout=int(timeout_time / 2)
            ))
            await asyncio.sleep(timeout_time) 
            await self.notifier.clear_all()
    def stop_app(self):
        self.notifier.send(
                title="One last thing...",
                message=self.get_random_message(),
                timeout=int(self.app_config["min_message_interval"] / 2)
            )
        print(f"Stopping application {self.app_config['app_name']}")
        sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    message_file = "messages.json"
    gtn = GoodThoughtNotifier(message_file=message_file)
    asyncio.run(gtn.run())
