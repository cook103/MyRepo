from plyer import notification
from bs4 import BeautifulSoup
import requests

icon_path = "/home/dboolin/GitRepos/MyRepo/MyApps/DesktopNotifier/m.ico"

def notify(title: str, msg: str) -> None:
    """write a custom desktop notification"""
    notification.notify(
        title = title,
        message = msg,
        app_icon = icon_path,
        timeout = 10,
    )


def get_data(url: str):
    """given a url scrape data from the web"""
    try:
        data = requests.get(url)
        soup = BeautifulSoup(data.content, "html.parser")
    except Exception as e:
        raise Exception("Failed to get the specified URL.")
    else:
        return data

data = get_data("https://www.coindesk.com/price/bitcoin/")
data = [x for x in data]

print(data)
