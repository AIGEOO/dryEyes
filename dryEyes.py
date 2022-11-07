import os, time, schedule, random, requests
from bs4 import BeautifulSoup
from datetime import datetime
from enum import Enum
from win10toast import ToastNotifier

class Essenstials():
    TASKS = [
        "Do 10 Pushups",
        "Take a walk",
        "Play A Chess Game",
        "Read 10 pages From A Book",
        "Respond to an email",
        "Make a call",
        "Feed the pets"
    ]
    URL = "https://www.islamicfinder.org/world/saudi-arabia/108410/riyadh-prayer-times/"


class DryEye:
    def __init__(self) -> None:
        self.fajr = self.sunrise = self.dhuhr = self.asr = self.maghrib = self.isha = self.current_time = None

    def assign_adhan_times_variables(self) -> None:
        """ Get prayer times from https://www.islamicfinder.org/ using BeautifulSoup """
        page = requests.get(Essenstials.URL)
        soup = BeautifulSoup(page.content, "html.parser")
        pray_titles = soup.find_all("div", class_="prayerTiles")

        self.current_time = datetime.strptime(time.strftime("%H:%M", time.localtime()), "%H:%M").strftime("%I:%M %p")

        self.fajr = pray_titles[0].find("span", class_="prayertime").text
        self.sunrise = pray_titles[1].find("span", class_="prayertime").text
        self.dhuhr = pray_titles[2].find("span", class_="prayertime").text
        self.asr = pray_titles[3].find("span", class_="prayertime").text
        self.maghrib = pray_titles[4].find("span", class_="prayertime").text
        self.isha = pray_titles[5].find("span", class_="prayertime").text

    def notification(self, content, title = "Current Task", duration = 20, toaster = ToastNotifier()) -> None:
        toaster.show_toast(
            title,
            content,
            duration = duration,
            icon_path = "icons/todo.ico", 
            threaded = True,
        )

    @staticmethod
    def sleeping() -> None:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def start(self) -> None:
        self.assign_adhan_times_variables()

        schedule.every(50).minutes.do(self.notification, random.choice(Essenstials.TASKS))
        # schedule.every(55).minutes.do(self.sleeping)

        while True:
            match self.current_time:
                case self.fajr:
                    self.notification("It's time for Fajr prayer", "Prayer Notification")
                case self.sunrise:
                    self.notification("It's time for Sunrise prayer", "Prayer Notification")
                case self.dhuhr:
                    self.notification("It's time for Dhuhr prayer", "Prayer Notification")
                case self.asr:
                    self.notification("It's time for Asr prayer", "Prayer Notification")
                case self.maghrib:
                    self.notification("It's time for Maghrib prayer", "Prayer Notification")
                case self.isha:
                    self.notification("It's time for Isha prayer", "Prayer Notification")

            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    try:
        dry = DryEye()
        dry.start()
    except Exception as e:
        print(e)