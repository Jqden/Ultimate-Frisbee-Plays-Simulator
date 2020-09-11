from Include.player import Player


# A defender is a type of player who is assigned to "guard" an offender. Once assigned to an offender,
# the defender remains glued to them, exactly matching the offenders movements. The user chooses the
# initial relative positioning of the defender and offender, and this relative positioning remains
# constant throughout.
class Defender(Player):

    def __init__(self, xy, offender=None):
        super().__init__(xy)
        self.x_offset = self.y_offset = self.offender = None
        if offender:
            self.assign_offender(offender)

        self.main_color = (0, 0, 200)  # blue
        self.off_color = (60, 110, 250)  # light blue
        self.image.fill(self.main_color)

    # The defender's positioning update should always be called after the offender's update,
    # so that they can match the offender's positioning.
    def update(self):
        if self.offender is not None:
            self.rect.x = self.offender.rect.x + self.x_offset
            self.rect.y = self.offender.rect.y + self.y_offset

    def assign_offender(self, offender):
        self.x_offset = self.rect.x - offender.x
        self.y_offset = self.rect.y - offender.y
        self.offender = offender
