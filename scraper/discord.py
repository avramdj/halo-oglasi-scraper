import os

from discord import SyncWebhook

_webhook = SyncWebhook.from_url(os.environ.get("DISCORD_WEBHOOK_URL"))


def send_to_discord(link, price, name, location):
    """
    sends name, location and price, and then posts link
    """
    _webhook.send(content=f"{name}\n\n{location}\n\n{int(price)}€ \n{link}", wait=True)