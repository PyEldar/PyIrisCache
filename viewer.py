"""Shows calculated data"""
import matplotlib.pyplot as plt


class Viewer:

    def show(self, data, display=True, file='out.png'):
        if not display:
            plt.switch_backend('Agg')
        else:
            plt.switch_backend('TkAgg')

        colors = {
            1: 'red',
            6: 'blue',
            40: 'green',
            48: 'magenta',
            63: 'black',
        }

        fig = plt.figure()
        fig.set_size_inches(70, 35)

        for key, value in data.items():
            plt.plot(list(value.keys()), list(value.values()), label=key, color=colors[key], linewidth=10)

        plt.tick_params(axis='both', labelsize=15)
        plt.title('Average delays at main station in Brno', fontsize=40)
        plt.ylabel('delay in minutes', fontsize=40)
        plt.xlabel('time during day', fontsize=40)

        leg = plt.legend(prop={'size': 100})
        for line in leg.get_lines():
            line.set_linewidth(10)

        if display:
            plt.show()
        fig.savefig(file)
