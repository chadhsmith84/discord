import os, sys, requests, getopt, traceback
from config import Config

#process notification server invite link:
#https://discord.gg/E2Wy2sxb


class DiscordWebhook(object):
    def discordMessage(self, message, avatar_url=None):
        '''
        Uses different webhook which defaults to username - Status and has a green check as the avatar url
        avatar_url can be dynamic. pass full url to image to use. Example: "https://i.ibb.co/xHKPyQ0/green-check.png"
        '''
        content = {"content": message,
                   "username": "{}".format(self.project),
                   "avatar_url": "{}".format(self.avatar_url if avatar_url is None else avatar_url),
                   "tts": self.tts
                   }

        result = requests.post('{}'.format(self.privateUrl), json=content)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
        
    def discordError(self, message, error_avatar_url=None):
        '''
        Uses different webhook which defaults to username - Error and has a red X as the avatar url
        error_avatar_url can be dynamic. pass full url to image to use. Example: "https://i.ibb.co/fGcXLcg/red-x.png"
        '''
        content = {"content": message,
                   "username": "{} ERROR".format(self.project),
                   "avatar_url": "{}".format(self.error_avatar_url if error_avatar_url is None else error_avatar_url),
                   "tts": self.tts
                   }
        result = requests.post(self.privateUrl, json=content)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)

    def __init__(self, client, project, avatar_url=None, error_avatar_url=None, tts=False):
        try:

            ################################
            # defining client
            ################################
            if not client:
                raise ValueError('customer must be defined')
            else:
                self.config = Config()
                self.client = client.lower()
                self.privateUrl = self.config.env[client.lower()]

            ################################
            # defining project/username
            ################################
            if project is None:
                self.project = self.client.upper()
            else:
                self.project = project.upper()

            ################################
            # avatar profile image
            ################################
            if avatar_url is None:
                # green check
                self.avatar_url = "https://i.ibb.co/xHKPyQ0/green-check.png"
            else:
                self.avatar_url = avatar_url
            if error_avatar_url is None:
                # x with red background
                self.error_avatar_url = "https://i.ibb.co/fGcXLcg/red-x.png"
            else:
                self.error_avatar_url = error_avatar_url

            ################################
            # text to speech
            ################################
            self.tts = tts

            #print(self.privateUrl)
            if self.privateUrl == '':
                raise ValueError('client: {} is not defined in the .env file. webhook must be created for customer'.format(client.lower()))

        except BaseException as e:
            traceback.print_exc()
            #raise ValueError(e)

if __name__ == '__main__':

    opts, args = getopt.getopt(sys.argv[1:], '', ['client=', 'project=', 'messageType=', 'message=', 'avatar_url=', 'error_avatar_url=', 'tts='])

    optsDict = {}
    optsDict.update(dict(opts))

    if '--client' in optsDict:
        client = optsDict['--client'].lower()
        print('--client value: {}'.format(client))
    else:
        raise ValueError('--client not passed. --client "someclient" needed')

    if '--project' in optsDict:
        project = optsDict['--project']
        print('--project: {}'.format(project))
    else:
        project = None
        print('--project not passed. Will default to client: {} for project/username: {}'.format(client))

    if '--messageType' in optsDict:
        messageType = optsDict['--messageType']
    else:
        messageType = None
        print('--messageType "error" or --messageType "notify" (if no message type default is client name)')

    if '--message' in optsDict:
        message = optsDict['--message']
    else:
        raise ValueError('--message not passed. --message "Some Message" needed')

    if '--avatar_url' in optsDict:
        avatar_url = optsDict['--avatar_url']
    else:
        avatar_url = None
        print('--avatar_url not passed (will default to green check)')

    if '--error_avatar_url' in optsDict:
        error_avatar_url = optsDict['--error_avatar_url']
    else:
        error_avatar_url = None
        print('--error_avatar_url not passed (will default to x with red background)')

    if '--tts' in optsDict:
        tts = optsDict['--error_avatar_url']
    else:
        tts = False
        print('--tts not passed (will default to False)')

    try:
        d = DiscordWebhook(client=client, project=project)

        if messageType and messageType.lower() in ['error', 'er', 'err', 'e', 'errors']:
            d.discordError(message)
        else:
            d.discordMessage(message)

    except:
        traceback.print_exc()