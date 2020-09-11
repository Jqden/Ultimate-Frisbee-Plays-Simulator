import math
from Include.player import Player


# An offender is a type of player who can move to different places on the
# field as described by a path the user creates for him. The methods in this
# class all modify or describe this path.
class Offender(Player):

    def __init__(self, xy):
        super().__init__(xy)
        self.x, self.y = self.rect.x, self.rect.y  # double, exact player position
        self.dx = self.dy = None  # double, amount player moves each iteration of the main loop
        self.path = [(self.x, self.y)]  # list of points player must travel to in order
        self.progress = -1  # represents which points on the path the player is traveling btwn
        self.turns_to_travel = 0  # number of turns (iterations) necessary to reach next point

        self.main_color = (200, 0, 0)  # red
        self.off_color = (250, 110, 110)  # light red
        self.image.fill(self.main_color)

    def update(self):
        if not self.path_completed():
            # When player reaches the point it was traveling to, set its coordinates to exactly that point
            # to account for floating point error. Increment progress by 1, and if there's still points left
            # to travel to, calculate how to reach the next point
            if self.turns_to_travel == 0:  # player has reached the point it was traveling to
                self.x, self.y = self.path[self.progress + 1][0], self.path[self.progress + 1][1]
                self.rect.x, self.rect.y = self.x, self.y
                self.progress += 1
                if not self.path_completed():  # after updating progress, is there still more to do?
                    self.calc_dxdy(self.path[self.progress:self.progress+2])
                else:
                    self.turns_to_travel = -1
            # If player is starting to move for the first time, calculate how to reach the next point and
            # don't increment progress
            elif self.turns_to_travel == -1:
                self.calc_dxdy(self.path[self.progress:self.progress + 2])
            # Otherwise, update the player's position and decrement the number of turns left to travel
            else:
                self.x += self.dx
                self.y += self.dy
                self.rect.x, self.rect.y = self.x, self.y
                self.turns_to_travel -= 1

    def calc_dxdy(self, points):
        # Player position (x, y) should change by a magnitude of exactly 1 each iteration so that their
        # speed is always the same (1 pixel / iteration). This method calculates the necessary delta x and
        # delta y for a magnitude 1 change.
        tot_dx = points[1][0] - points[0][0]
        tot_dy = points[1][1] - points[0][1]
        if tot_dx == 0:
            self.dx = 0
            self.dy = 1 if tot_dy > 0 else -1
            self.turns_to_travel = math.ceil(tot_dy / self.dy)
        else:
            slope = tot_dy / tot_dx
            r = math.sqrt(1 / (slope ** 2 + 1))
            self.dx = r if tot_dx > 0 else -1*r
            self.dy = r*slope if tot_dx > 0 else r*slope*-1
            self.turns_to_travel = math.ceil(tot_dx / self.dx)

    # Move player back to the first point in their path. Update control variables accordingly.
    def reset_path(self):
        self.x, self.y = self.path[0][0], self.path[0][1]
        self.rect.x, self.rect.y = self.x, self.y
        self.progress = 0
        self.turns_to_travel = -1

    # Adds a new point (x, y) to the player's path. Adjusts the input (x, y) location so that the middle
    # of the square will arrive where the user clicked, instead of the top right corner.
    def add_point(self, point):
        self.path.append((point[0] - self.size / 2, point[1] - self.size / 2))

    # Returns true if no more points to travel to, false otherwise.
    def path_completed(self):
        return self.progress >= len(self.path)-1

    # Removes all points (except player's current position) from the path.
    def clear_path(self):
        self.path = [(self.rect.x, self.rect.y)]
        self.progress = 0

    # Returns the list of points in the player's path before the modification in add_point is done.
    def get_original_points(self):
        return [(point[0] + self.size / 2, point[1] + self.size / 2) for point in self.path]
