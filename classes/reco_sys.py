import uuid


class RecommenderSystem():
    def __init__(self):
        self._id = uuid.uuid4()

    @property
    def id(self):
        return self._id
