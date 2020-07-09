from statistics import mean
import time
import sys

from pynput.keyboard import Key, Listener


ONE_SECOND = 1

class KeyboardListener:
    running = True

    def on_press(self, key):
        if key == Key.esc or key == Key.enter:
            self.running = False

    def on_release(self, key):
        pass

    def run(
        self,
        before_running=None,
        while_running=None,
        after_running=None
    ):
        listener = Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
        if before_running:
            before_running(self)  # This should allow us to initialize variables
        while self.running:
            if while_running:
                while_running(self) # this should swallow input https://github.com/moses-palmer/pynput/issues/47
                sys.stdin.read()
            time.sleep(1)
        if after_running:
            after_running(self)

## Example Usage B
class WPMListener(KeyboardListener):
    chars_pressed_this_second = 0
    chars_per_second = []  # update this count every second
    _timestep = 0

    def on_press(self, key):
        self.chars_pressed_this_second += 1
        super().on_press(key)

    def calculate_wpm(self, listener):
        # https://pypi.org/project/wpm/#calculating-wpm
        av = mean(self.chars_per_second)
        wpm = (av / 5) * 60
        print(f"\nWPM: {wpm}")

    def perform_single_step(self, listener):
        self.chars_per_second += [self.chars_pressed_this_second]
        self.chars_pressed_this_second = 0
        time.sleep(ONE_SECOND)

    def run(self):
        super().run(
            while_running=self.perform_single_step,
            after_running=self.calculate_wpm
        )



def main():
    k = WPMListener()
    k.run()


if __name__ == "__main__":
    main()
