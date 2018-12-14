from collections import OrderedDict


class Calculator:
    """Calculates average delays for every 10 minutes of every weekday"""
    def __init__(self, data_interface, lines):
        self.data_interface = data_interface
        self.lines = lines
        self.stop = self.data_interface.get_stop_key('Hlavní nádraží')
        self.data = {}

    def process_lines(self):
        """Takes records from mongodb and calculates average delays"""
        for line in self.lines:
            primary_key = line
            self.data[primary_key] = {}
            line_data = self.data_interface.get_by_line(line)
            preprocessed_data = self.preprocess(line_data, self.stop)
            averaged_data = self.calculate_average(preprocessed_data)
            self.data[primary_key] = self.order_data(averaged_data)

    def preprocess(self, data, stop):
        """
        Saves only vehicles coresponding to specified stop, filter duplicate vehicles
        result dict structure:
            dict(
                ('hour,minute // 10': [vehicles]),
            )
        """
        checked = dict()
        for record in data:
            secondary_key = '{},{}'.format(
                record['last_updated'].hour,
                str(record['last_updated'].minute)[0] if len(str(record['last_updated'].minute)) > 1 else '0'
            )
            for vehicle in record['vehicles']:
                if (str(vehicle['LastStop']) == stop) and (vehicle not in checked.get(secondary_key, [])):
                    if secondary_key not in checked.keys():
                        checked[secondary_key] = []
                    checked[secondary_key].append(vehicle)
        return checked

    def calculate_average(self, data):
        """Calculates average value for every item in passed dict"""
        for key, value in data.items():
            total = 0
            if value:
                for vehicle in value:
                    total += vehicle['Delay']
                data[key] = int(total / len(value))
            else:
                data[key] = 0
        return data

    def order_data(self, data):
        """Orders dict by keys"""
        result = OrderedDict()

        # create default dict with keys in format 'hour,minute'
        for i in range(24):
            for j in range(6):
                result['{},{}'.format(i, j)] = 0

        for key, value in sorted(data.items()):
            result[key] = value

        return result
