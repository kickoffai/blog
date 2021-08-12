import json
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

# Map outcome to index for easier comparison with predictions.
outcome2idx = {
    "win": 0,
    "draw": 1,
    "loss": 2,
}


class Dataset:
    def __init__(self, path='euro2020.json'):
        self.data = self.load_data(path)
        self.bookmakers = list(
            self.data[list(self.data.keys())[0]]['odds'].keys()
        )
        # Find bookmakers that are not present in all matches.
        missing = list()
        for match in self.data.values():
            for bookmaker in self.bookmakers:
                if bookmaker not in match['odds']:
                    missing.append(bookmaker)
        self.missing = set(missing)

    @staticmethod
    def load_data(path):
        with open(path) as f:
            data = json.load(f)
        # Adding odds of Netherlands vs. Austria, as they are missing.
        # https://www.oddsportal.com/soccer/europe/euro-2020/netherlands-austria-nXGpC2OB/
        data["72785"]["odds"] = {
            "10x10bet": {"1x2": [1.65, 3.95, 5.90], "tstamp": ""},
            "1xbet": {"1x2": [1.60, 3.89, 6.82], "tstamp": ""},
            "Asianodds": {"1x2": [1.65, 3.88, 6.49], "tstamp": ""},
            "Bet-At-Home": {"1x2": [1.63, 3.95, 5.80], "tstamp": ""},
            "bet365": {"1x2": [1.60, 3.80, 6.00], "tstamp": ""},
            "Bethard": {"1x2": [1.65, 3.95, 6.25], "tstamp": ""},
            "Betsensation": {"1x2": [1.66, 4.00, 6.00], "tstamp": ""},
            "BWin": {"1x2": [1.62, 3.90, 5.75], "tstamp": ""},
            "Coolbet": {"1x2": [1.62, 3.85, 7.09], "tstamp": ""},
            "GGBET": {"1x2": [1.60, 4.13, 6.29], "tstamp": ""},
            "Marathonbet": {"1x2": [1.64, 3.92, 6.25], "tstamp": ""},
            "Pinnacle": {"1x2": [1.65, 3.85, 6.30], "tstamp": ""},
            "Unibet": {"1x2": [1.66, 3.90, 6.00], "tstamp": ""},
            "WilliamHill": {"1x2": [1.60, 3.90, 6.00], "tstamp": ""},
        }
        return data


def compute_accuracy(dataset):

    accuracies = defaultdict(list)
    data = sorted(dataset.data.items(), key=lambda x: x[1]["kickoff_time"])
    for mid, match in data:
        outcome = outcome2idx[match["outcome"]]
        # Kickoff.ai
        pred = np.argmax(match['pred'])
        if outcome == pred:
            accuracies['Kickoff.ai'].append(1)
        else:
            accuracies['Kickoff.ai'].append(0)
        # Odds.
        for bookmaker in dataset.bookmakers:
            if bookmaker not in dataset.missing:
                bet = np.argmin(match["odds"][bookmaker]["1x2"])
                if outcome == bet:
                    accuracies[bookmaker].append(1)
                else:
                    accuracies[bookmaker].append(0)

    return accuracies


def compute_logloss(dataset):

    labels = list()
    losses = defaultdict(list)
    data = sorted(dataset.data.items(), key=lambda x: x[1]["kickoff_time"])
    for mid, match in data:
        labels.append("{} - {}".format(match["team_a"], match["team_b"]))
        idx = outcome2idx[match["outcome"]]
        losses['Kickoff.ai'].append(-np.log(match["pred"][idx]))
        # Odds.
        for bookmaker in dataset.bookmakers:
            if bookmaker not in dataset.missing:
                ps = 1 / np.array(match["odds"][bookmaker]["1x2"])
                ps /= ps.sum()
                losses[bookmaker].append(-np.log(ps[idx]))

    return losses, labels


def report_accuracy(accuracies):
    print('Accuracy:')
    print('  Random:     33%')
    for model, accuracy in accuracies.items():
        print(f'  {model}: {np.mean(accuracy)*100:.2f}%')


def report_logloss(losses):
    print('Log loss:')
    print(f'  Random:     {-np.log(1/3):.4f}')
    for model, logloss in losses.items():
        print(f'  {model}: {np.mean(logloss):.4f}')


def plot_accuracy(accuracies):

    factor = 0.75
    width = 6.4 * factor
    height = 4.8 * factor
    plt.figure(figsize=(width, height))

    labels, values, colors = ['Random'], [33], ['gray']
    for i, (model, accuracy) in enumerate(accuracies.items()):
        labels.append(model)
        values.append(np.mean(accuracy) * 100)
        colors.append(f'C{i}')

    plt.bar(labels, values, color=colors)
    plt.ylabel('Accuracy [%]')
    plt.xticks(rotation=45)
    # plt.show()
    plt.tight_layout()
    plt.savefig('../../assets/posts/eu20-analysis/accuracy.png')


def plot_logloss(losses):

    factor = 0.75
    width = 6.4 * factor
    height = 4.8 * factor
    plt.figure(figsize=(width, height))

    labels, values, colors = ['Random'], [-np.log(1 / 3)], ['gray']
    for i, (model, logloss) in enumerate(losses.items()):
        labels.append(model)
        values.append(np.mean(logloss))
        colors.append(f'C{i}')

    plt.bar(labels, values, color=colors)
    plt.ylabel('Log loss')
    plt.xticks(rotation=45)
    # plt.show()
    plt.tight_layout()
    plt.savefig('../../assets/posts/eu20-analysis/logloss.png')


def main():
    dataset = Dataset()
    accuracies = compute_accuracy(dataset)
    report_accuracy(accuracies)
    plot_accuracy(accuracies)
    losses, labels = compute_logloss(dataset)
    report_logloss(losses)
    plot_logloss(losses)


if __name__ == '__main__':
    main()
