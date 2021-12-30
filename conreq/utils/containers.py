class FillList(list):
    """Modified `list` that allows for setting a value at
    any arbitrary index."""

    def __setitem__(self, index, value):
        try:
            super().__setitem__(index, value)
        except IndexError:
            for _ in range(index - len(self) + 1):
                self.append(None)
            super().__setitem__(index, value)
