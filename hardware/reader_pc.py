import time, random

class ReaderSim:
    def __init__(self, mode="manual", interval_s=2.0, sequence=None, loop_sequence=True):
        self.mode = mode
        self.interval_s = interval_s
        self.sequence = list(sequence) if sequence else []
        self.loop_sequence = loop_sequence
        self._i = 0

    def _rand_hex(self, n=8):
        return "".join(random.choice("0123456789ABCDEF") for _ in range(n))

    def read_once(self):
        time.sleep(0.2)
        if self.sequence:
            if self._i >= len(self.sequence):
                return None if not self.loop_sequence else self._rand_hex()
            val = self.sequence[self._i]
            self._i += 1
            return val
        return self._rand_hex()
