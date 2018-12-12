import threading
import sys
import time

from downloader import Downloader
from data_interface import DataInterface


class DataManager:
    """Manages downloader and viewer threads"""
    def __init__(self, lines, dbname, data_sources, update_interval):  # should be in config.py
        self.data_sources = data_sources
        self.lines = lines
        self.update_interval = update_interval
        self.data_interface = DataInterface(dbname)
        self.downloader_thread = None
        self.viewer_thread = None
        self.THREAD_COUNT = 2  # including main thread
        self.stop_event = threading.Event()

    def run(self):
        self.downloader_thread = threading.Thread(
            target=Downloader(
                self.data_interface,
                self.data_sources[0],
                self.data_sources[1],
                self.lines,
                self.stop_event,
                self.update_interval
            ).run()
        )
        self.downloader_thread.setDaemon(True)
        self.downloader_thread.start()
        self.watch_threads()

    def watch_threads(self):
        while True:
            if threading.active_count() < self.THREAD_COUNT:
                sys.exit(0)
            time.sleep(1)


if __name__ == '__main__':
    manager = DataManager(
        [1, 6, 40, 63, 48],
        'iris_cache',
        ['https://iris.bmhd.cz/api/stops.json', 'https://iris.bmhd.cz/api/data.json'],
        60
    )
    manager.run()
