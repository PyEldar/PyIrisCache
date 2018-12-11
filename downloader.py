import requests
import simplejson


class Downloader:
    def __init__(self, data_storage, stops_url, vehicles_url):
        self.stops_url = stops_url
        self.vehicles_url = vehicles_url
        self.data_storage = data_storage

    def get_json(self, url):
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
        stops_now = self.get_json(self.stops_url)
        if not stops_now == self.data_storage.get_one('stops'):
            self.data_storage.store('stops', stops_now)

    def check_vehicles(self):
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
