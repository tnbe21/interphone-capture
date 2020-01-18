import time
import slack
import os


class SlackApp:
    _last_ringed = None

    def notify_slack(self, msg='test'):
        INTERVAL_SEC = 20
        CHANNEL = 'interphone_notification'
        MENTIONED_USER = 'tanabe_taichi'

        if self._last_ringed is not None and time.time() < self._last_ringed + INTERVAL_SEC:
            return

        self._last_ringed = time.time()
        client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
        client.chat_postMessage(
            channel='#%s' % CHANNEL,
            link_names=True,
            text='@%s %s' % (MENTIONED_USER, msg)
        )


if __name__ == '__main__':
    slackApp = SlackApp()
    slackApp.notify_slack()
