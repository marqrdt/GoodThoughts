from desktop_notifier import DesktopNotifier, Urgency, Icon
import time
import asyncio
import signal
import json
import random

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

    async def run(self):
        messages_length = len(self.messages_json.get('messages'))

        while True:
            message = self.messages_json.get('messages')[ self.rand.randint(0, messages_length-1) ]
            #dtn = self.notifier( message['text'])
            #print(f"notification id is {dtn.id}, summary is {dtn.summary}")
            #dtn.set_id(dtn.id).set_timeout(app_config["min_message_interval"])
            await self.notifier.send(
                title=self.app_name,
                message=message['text'],
                timeout=int(self.app_config["min_message_interval"] / 2)

            )
            stop_event = asyncio.Event()
            loop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGINT, stop_event.set)
            loop.add_signal_handler(signal.SIGTERM, stop_event.set)
            await asyncio.sleep(self.rand.randint(self.app_config["min_message_interval"], self.app_config["max_message_interval"])) 
            await self.notifier.clear_all()

if __name__ == "__main__":
    message_file = "messages.json"
    gtn = GoodThoughtNotifier(message_file=message_file)
    asyncio.run(gtn.run())
