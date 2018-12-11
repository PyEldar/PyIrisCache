import requests
import simplejson
import time


class Downloader:
    def __init__(self, data_storage, stops_url, vehicles_url, lines, stop, interval):
        self.interval = interval
        self.stops_url = stops_url
        self.vehicles_url = vehicles_url
        self.data_storage = data_storage
        self.lines = lines
        self.stop_event = stop

    def get_json(self, url):
        """Requests JSON returns None if response is non-JSON"""
        try:
            r = requests.get(url)
            if r.status_code == 200:
                try:
                    return r.json()
                except simplejson.errors.JSONDecodeError:
                    return None
        except requests.exceptions.RequestException:
            return None

    def check_stops(self):
        """If stops changed strone new version to DB"""
        stops_now = self.get_json(self.stops_url)
        if not stops_now == self.data_storage.get_one('stops'):
            self.data_storage.store('stops', stops_now)

    def check_vehicles(self):
        """Downloads and filters vehicles"""
        data = self.get_json(self.vehicles_url)
        if data:
            vehicles = data['Data']
            filtered = list()

            for key, vehicle in vehicles.items():
                if vehicle.get('Line') in self.lines:
                    vehicle['key'] = key
                    filtered.append(vehicle)
        if filtered:
            self.data_storage.store(
                'mhd_data',
                {
                    'last_updated': data['LastUpdate'],
                    'vehicle': filtered
                }
            )
        else:
            print('No vehicles')

    def run(self):
        """Runs in loop - downloads data after specified interval"""
        while not self.stop_event.is_set():
            self.check_vehicles()
            self.check_stops()
            time.sleep(self.interval)
