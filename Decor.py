from GameObject import Decor

class Door(Decor):
    def __init__(self, pos):
        super().__init__("Door", 'D', pos, 40, (0.7, 0.7, 0.3, -1, 0, 1, 1, 0, 1, 1, 1, 1, 1), False, True, "NO", "")
        def onInteract(self, ceature):
            if(self.passable == False):
                self.passable = True
                self.blockSight = False
            else:
                self.passable = False
                self.blockSight = True