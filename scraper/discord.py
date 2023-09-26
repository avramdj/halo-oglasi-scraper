from discord import SyncWebhook


def send_to_discord(link, price, name, location, hook_url):
    """
    sends name, location and price, and then posts link
    """
    SyncWebhook.from_url(hook_url).send(
        content=f"{name}\n\n{location}\n\n{int(price)}€ \n{link}", wait=True
    )
