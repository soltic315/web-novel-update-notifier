import json
import requests

class SlackWebhook():

    def __init__(self, slack_url, slack_channel, slack_bot_name, slack_bot_icon):
        self.slack_url = slack_url
        self.slack_channel = slack_channel
        self.slack_bot_name = slack_bot_name
        self.slack_bot_icon = slack_bot_icon

    def post_novel(self, item):
        fields = [
            {'title': 'Author', 'value': item['author'], 'short': True},
            {'title': 'Updated', 'value': item['updated_at'].strftime('%Y/%m/%d %H:%M'), 'short': True},
        ]
        
        attachments = [{
            'fallback': f'{item["title"]} is updated',
            "color": 'good',
            'title': item['title'],
            'title_link': item['latest_url'],
            'fields': fields,
            'footer': item['domain'],
        }]
        
        payload = {'username': self.slack_bot_name, 'icon_emoji': self.slack_bot_icon, 'attachments': attachments}

        if self.slack_channel:
            payload['channel'] = self.slack_channel

        requests.post(self.slack_url, json.dumps(payload))