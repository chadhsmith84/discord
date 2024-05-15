from discord_send_message import DiscordWebhook
import traceback

class SendMessage():
    def process(self):
        self.d.discordError('Process Failed')
    def __init__(self):
        self.customer = 'testing'
        self.d = DiscordWebhook(self.customer, "Some Test Process")

        self.process()

if __name__ == '__main__':
    try:
        d = SendMessage()
    except:
        traceback.print_exc()