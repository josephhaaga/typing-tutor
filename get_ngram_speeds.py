"""Print an adjacency matrix of response times for n-gram key strokes."""
from utils import KeyboardListener
from datetime import datetime

import pandas as pd

# As N gets larger, @lru_cache might become useful for redundant calculations


class NGramListener(KeyboardListener):
    events = []

    def __init__(self, n=2):
        self.N = n

    def on_press(self, key):
        event = {"key": key, "time": datetime.now()}
        self.events += [event]
        super().on_press(key)

    def calculate_ngram_adjacency_matrix(self, listener):
        keystroke_df = pd.DataFrame(self.events)
        keys = keystroke_df['key'].apply(str)
        keystroke_df['key 1'] = keys.shift(1)
        keystroke_df['key 2'] = keys
        kt = pd.to_datetime(keystroke_df['time'])
        keystroke_df['time'] = kt.diff().apply(lambda x: x.microseconds)

        keystroke_df = keystroke_df[['key 1', 'key 2', 'time']][1:]
        adjacency_matrix = keystroke_df.pivot_table(index='key 1', columns='key 2', aggfunc='mean')
        print(adjacency_matrix)


    def run(self):
        super().run(
            after_running=self.calculate_ngram_adjacency_matrix  # should after_running() return output?
        )


def main():
    runner = NGramListener()
    runner.run()

if __name__ == '__main__':
    main()
