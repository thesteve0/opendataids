

class Image:
    name = ''
    title = ''

    def __init__(self, catid):
        self.catid = catid




    def __repr__(self):
        return repr((self.catid, self.name, self.title))
