import colorsys
import itertools
import random


class Level:

    def __init__(self, circle_list):
        """
        Initializes a Level-object.

        :param circle_list: shuffled list of ints,
        representing the order of the circles
        """
        self.begin_order = circle_list  # Saves the original order
        self.circles = circle_list
        self.counter = 0    # Represents the number of moves

        copy_list = circle_list.copy()
        copy_list.sort()
        self.answer = copy_list

        self.colors = self.set_colors()

    def set_colors(self):
        """
        Calculates the colors of the circles using HSV color space,
        such that they form a spectrum.

        :return: dict containing rgb-values for each element in the circles-list
        """
        color_dict = dict()

        hue = 0
        delta_hue = 1 / len(self.circles)
        saturation = 0.5
        brightness = 1.0

        # Iterates for every element in the circles-list
        for i in range(len(self.circles)):
            (r, g, b) = colorsys.hsv_to_rgb(hue, saturation, brightness)
            red, green, blue = int(255 * r), int(255 * g), int(255 * b)
            color = (red, green, blue)
            color_dict[i] = color
            hue += delta_hue

        return color_dict

    def reset(self):
        """ Resets the level to its original order and undoes all moves. """
        self.circles = self.begin_order
        self.counter = 0

    def click_a(self):
        """ Swaps the first two circles in the list. """
        copy_list = self.circles.copy()
        first = copy_list[0]
        copy_list[0] = copy_list[1]
        copy_list[1] = first

        self.circles = copy_list
        self.counter += 1

    def click_b(self):
        """ Swaps the last two circles in the list. """
        copy_list = self.circles.copy()
        last = copy_list[-1]
        copy_list[-1] = copy_list[-2]
        copy_list[-2] = last

        self.circles = copy_list
        self.counter += 1

    def click_x(self):
        """ Shifts the circles in the middle of the list. """
        copy_list = self.circles.copy()
        second_last = copy_list[-2]
        n_circles = len(copy_list)

        for i in range(n_circles - 2, 1, -1):
            copy_list[i] = copy_list[i - 1]  # Each circle moves one place to the right

        copy_list[1] = second_last  # The rightmost middle-circle moves to the left

        self.circles = copy_list
        self.counter += 1


class CreateLevels:

    def __init__(self):
        """ Initializes a MakeLevels-object. """
        levels = dict()

        # Gets all permutations of circles-list for each length of 4-8
        for length in range(4, 9):
            ordered = [x for x in range(length)]
            perm = list(itertools.permutations(ordered))
            del perm[0]  # Delete the perm already in correct order
            levels[length] = perm   # Store perm in dict corresponding to length

        self.levels = levels

    def get_random(self, length):
        """
        Creates a Level of given length with random order of circles.

        :param length: number of circles, proportional to difficulty of level
        :return: Level-object with random permutation of circles
        """
        perm = self.levels[length]
        seq = [x for x in random.choice(perm)]
        return Level(seq)
