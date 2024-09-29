from GameObject import Decor

class Door(Decor):
    def __init__(self, pos):
        super().__init__("Door", 'D', pos, 40, "haven't made resistances datastructure yet", False, True, "NO", "")
        def onInteract(self, ceature):
            if(self.passable == False):
                self.passable = True
                self.blockSight = False
            else:
                self.passable = False
                self.blockSight = True