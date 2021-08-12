import json

import matplotlib.pyplot as plt
import numpy as np

# Map outcome to index for easier comparison with predictions.
outcome2idx = {
    "win": 0,
    "draw": 1,
    "loss": 2,
}
idx2outcome = {
    0: "win",
    1: "draw",
    2: "loss",
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


def simulate_betting(dataset, money=100):
    data = dataset.data
    trace = [money]

    for mid, match in sorted(data.items(), key=lambda x: x[1]["kickoff_time"]):
        # print(f'---- {match["team_a"]} vs {match["team_b"]} ({mid})')
        idx = outcome2idx[match["outcome"]]
        pred = np.array(match["pred"])
        odds = np.zeros(shape=(len(match["odds"]), 3))
        for i, d in enumerate(match["odds"].values()):
            odds[i, :] = d["1x2"]
        odds = np.median(odds, axis=0)
        expected_gain = pred * odds - 1
        if np.max(expected_gain) > 0:
            outcome = np.argmax(expected_gain)
            frac = expected_gain[outcome] / (odds[outcome] - 1)
            # print(f'betting {frac*money:.2f} on {idx2outcome[outcome]}')
            win = (
                frac * money * (odds[outcome] - 1)
                if outcome == idx
                else -frac * money
            )
            # print("delta winnings: {:.2f}".format(win))
            money += win
            # print("current stash: {:.2f}".format(money))
        # else:
        # print("no good bet available")
        trace.append(money)
    return trace


def plot(dataset, trace):
    labels = list()
    data = sorted(dataset.data.items(), key=lambda x: x[1]["kickoff_time"])
    for mid, match in data:
        labels.append("{} - {}".format(match["team_a"], match["team_b"]))

    fig, ax = plt.subplots(figsize=(12, 6))

    indices = np.arange(len(labels))
    ax.plot(indices, trace[1:], marker="o")
    ax.set_xticks(indices)
    ax.set_xticklabels(labels, ha="right", rotation=45)
    ax.set_ylabel('Money')
    ax.grid(axis="both")
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig('../../assets/posts/eu20-analysis/betting.png')


def main():
    dataset = Dataset()
    trace = simulate_betting(dataset)
    plot(dataset, trace)


if __name__ == '__main__':
    main()
