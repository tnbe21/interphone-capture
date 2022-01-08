import time
import os
from slack_sdk import WebClient as SlackWebClient


class SlackApp:
    __last_ringed = None
    __client = SlackWebClient(token=os.environ["SLACK_API_TOKEN"])

    def notify_slack(self, msg="test"):
        interval_sec = 20
        channel = "interphone_notification"
        mentioned_user = "tanabe_taichi"

        if self.__last_ringed is not None and time.time() < self.__last_ringed + interval_sec:
            return

        self.__last_ringed = time.time()
        self.__client.chat_postMessage(
            channel="#%s" % channel,
            link_names=True,
            text="@%s %s" % (mentioned_user, msg)
        )


if __name__ == "__main__":
    slackApp = SlackApp()
    slackApp.notify_slack()
