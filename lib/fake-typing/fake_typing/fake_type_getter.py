class FakeTypeGetter:
    def __getattr__(self, item):
        return self


faker = FakeTypeGetter()
