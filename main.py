import random
import arcade
import math
import os
import numpy as np
from bacteria import Bacterias, Bacteria
from conf import *


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        # Variables that will hold sprite lists
        self.food_list = None
        self.bacterias_list = None
        # Set up the player info
        self.score = 0
        self.score_text = None

        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.food_list = arcade.SpriteList()
        self.bacterias = Bacterias()
        self.bacterias.append(Bacteria(zuper=True))

        # Set up the player
        self.score = 0

        # Create the foods
        for i in range(FOOD_COUNT):
            # Create the food instance
            # food image from kenney.nl
            food = arcade.Sprite("sprites/food.png", SPRITE_SCALING_FOOD)
            # Position the food
            food.center_x = random.randrange(300, SCREEN_WIDTH-300)
            food.center_y = random.randrange(300, SCREEN_HEIGHT-300)
            # Add the food to the lists
            self.food_list.append(food)
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """ Render the screen. """
        # This command has to happen before we start drawing
        arcade.start_render()
        # Draw all the sprites.
        self.food_list.draw()
        self.bacterias.draw()
        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """
        pass
        # for bacteria in self.bacterias:
        #     bacteria.angle += 10
        #     # Taking into account the angle, calculate our change_x
        #     # and change_y. Velocity is how fast the bacteria travels.
        #     bacteria.change_x = math.cos(math.radians(bacteria.angle)) * BACTERIA_SPEED
        #     bacteria.change_y = math.sin(math.radians(bacteria.angle)) * BACTERIA_SPEED

    def on_update(self, delta_time):
        """ Movement and game logic """
        # delta_time *= 5
        if random.random() < 0.1:
            food = arcade.Sprite("sprites/food.png", SPRITE_SCALING_FOOD)
            # Position the food
            food.center_x = random.randrange(300, SCREEN_WIDTH-300)
            food.center_y = random.randrange(300, SCREEN_HEIGHT-300)
            # Add the food to the lists
            self.food_list.append(food)
        # Call update on all sprites
        self.bacterias.update(delta_time)
        # Loop through each bacteria
        for bacteria in self.bacterias:
            hit_list = arcade.check_for_collision_with_list(bacteria, self.food_list)
            for food in hit_list:
                bacteria.collision_with_food(food)

            # if bacteria.top > self.width or bacteria.bottom < 0 or bacteria.left < 0 or bacteria.right > self.width:
            #     bacteria.remove_from_sprite_lists()

        for bacteria in self.bacterias:
            # Check this bacteria to see if it hit a food
            hit_list = arcade.check_for_collision_with_list(bacteria, self.bacterias)
            for hit_to_bacteria in hit_list:
                bacteria.collision_with_bacteria(hit_to_bacteria)


        for bacteria in self.bacterias:
            nearest_bacteria = None
            nearest_b_dist = np.inf
            for b in self.bacterias:
                if b != bacteria:
                    d = bacteria.dist_to(b)
                    if d < nearest_b_dist:
                        nearest_b_dist = d
                        nearest_bacteria = b

            nearest_food = None
            nearest_f_dist = np.inf
            for f in self.food_list:
                d = bacteria.dist_to(f)
                if d < nearest_f_dist:
                    nearest_f_dist = d
                    nearest_food = f

            bacteria.forward_pass(nearest_bacteria, nearest_food)

        if len(self.bacterias) <= 5:
            for i in range(len(self.bacterias)):
                self.bacterias.append(Bacteria(parent=self.bacterias[i]))
                self.bacterias.append(Bacteria())

        for bacteria in self.bacterias:
            if bacteria.weight > 3:
                # we increase speed or we have a child
                if bacteria.priorities > 0:
                    self.bacterias.append(Bacteria(parent = bacteria))
                    bacteria.weight -= 1



def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
