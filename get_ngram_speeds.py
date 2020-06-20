from utils import KeyboardListener
from datetime import datetime

class NGramCalculator(KeyboardListener):
    events = []

    def on_press(self, key):
        super().on_press()
        event = {'key': key, 'time': datetime.now()}
        self.events += [event]


    def calculate_ngrams(self):
        pass

    def run(self):
        super().run()
        self.

# How can we make KeyboardListener easily extendable?
# I'd like to declare a custom datastructure, and functions that update them within the KeyboardListener.run() loop
