import threading
import sys
import time

from downloader import Downloader
from calculator import Calculator
from data_interface import DataInterface
from viewer import Viewer


class DataManager:
    """Manages downloader thread and calculates and saves data on demand"""
    def __init__(self, lines, dbname, data_sources, update_interval):  # should be in config.py
        self.data_sources = data_sources
        self.lines = lines
        self.update_interval = update_interval
        self.data_interface = DataInterface(dbname)
        self.downloader_thread = None
        self.THREAD_COUNT = 2  # including main thread
        self.stop_event = threading.Event()
        self.calculator = Calculator(self.data_interface, self.lines)
        self.viewer = Viewer()

    def run(self):
        self.downloader_thread = threading.Thread(
            target=Downloader(
                self.data_interface,
                self.data_sources[0],
                self.data_sources[1],
                self.lines,
                self.stop_event,
                self.update_interval
            ).run
        )
        self.downloader_thread.setDaemon(True)
        self.downloader_thread.start()
        self.interact()

    def watch_threads(self):
        while True:
            if threading.active_count() < self.THREAD_COUNT:
                sys.exit(0)
            time.sleep(1)

    def interact(self):
        while True:
            option = input('Calculate new data? <yes/no>\n')
            if option == 'yes':
                filename = input('Enter output filename\n')
                self.calculator.data = {}
                self.calculator.process_lines()
                self.viewer.show(self.calculator.data, display=False, file=filename)
            else:
                filename = input('Enter output filename\n')
                self.viewer.show(self.calculator.data, display=False, file=filename)


if __name__ == '__main__':
    manager = DataManager(
        [1, 6, 40, 63, 48],
        'iris_cache',
        ['https://iris.bmhd.cz/api/stops.json', 'https://iris.bmhd.cz/api/data.json'],
        60
    )
    manager.run()
