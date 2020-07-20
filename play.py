import pygame as pg
from sys import exit
from create_level import CreateLevels
from solve import Solver
from draw import Drawer


WIDTH = 800
HEIGHT = 420
SCREEN_SIZE = (WIDTH, HEIGHT)
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)
BUTTON_SMALL = (BUTTON_WIDTH / 2, BUTTON_HEIGHT)


def main():
    """ Main program for playing the game. """
    pg.init()
    clock = pg.time.Clock()
    fps = 60
    pg.display.set_caption('Tricky Circles')
    icon = pg.image.load('resources/icon.jpg')
    pg.display.set_icon(icon)

    # Create display
    screen = pg.display.set_mode(SCREEN_SIZE)

    # Load resources such as wallpaper and fonts
    bg = pg.image.load('resources/desert.jpg')
    font = pg.font.Font('resources/western.ttf', 30)
    font_big = pg.font.Font('resources/western.ttf', 50)

    # Create buttons
    space = 50  # Space in between action buttons: a, b, x
    button_x = pg.Rect((WIDTH / 2 - BUTTON_WIDTH / 2, 250), BUTTON_SIZE)
    button_a = pg.Rect((button_x.x - space - BUTTON_WIDTH, button_x.y), BUTTON_SIZE)
    button_b = pg.Rect((button_x.x + space + BUTTON_WIDTH, button_x.y), BUTTON_SIZE)

    button_solve = pg.Rect((10, 0), BUTTON_SIZE)
    button_reset = pg.Rect((BUTTON_WIDTH + 20, button_solve.y), BUTTON_SIZE)
    button_info = pg.Rect((WIDTH - BUTTON_WIDTH / 2, button_solve.y), BUTTON_SMALL)

    button_difficulty = pg.Rect((WIDTH / 2 - BUTTON_WIDTH / 2, 0), BUTTON_SIZE)
    button_min = pg.Rect(button_difficulty.topleft, BUTTON_SMALL)
    button_plus = pg.Rect(button_difficulty.midtop, BUTTON_SMALL)

    buttons = {'A': button_a, 'X': button_x, 'B': button_b,
               'Solve': button_solve, 'Reset': button_reset,
               '-': button_min, '+': button_plus, '?': button_info}

    # Create starting level
    difficulty = 4  # Number of circles
    level_maker = CreateLevels()
    level = level_maker.get_random(difficulty)
    solver = Solver(level)
    min_moves, _ = solver.solve()  # Minimum moves needed to solve level

    # Creates Drawer for drawing levels
    drawer = Drawer(screen, WIDTH, level)
    drawer.draw_level(font, bg, min_moves, buttons, animation=False)

    auto_solve = False

    while True:

        if level.circles == level.answer:  # Level is solved

            # Draw finish-screen, depending on how level was solved
            if auto_solve:
                new_level = drawer.draw_solved(font_big, "Try it yourself?")
                auto_solve = False
            elif level.counter == min_moves:
                new_level = drawer.draw_solved(font_big, "Perfect score!")
            else:
                new_level = drawer.draw_solved(font_big, "Solved in {} moves!".format(level.counter))

            if new_level:
                # Start a new game
                print('New game')
                level = level_maker.get_random(difficulty)
                drawer.level = level
                solver = Solver(level)
                min_moves, _ = solver.solve()
            else:
                # Reset level to try again
                print('Retry level')
                level.reset()

            drawer.draw_level(font, bg, min_moves, buttons, animation=False)

        for event in pg.event.get():

            # Quit when exit-button is clicked
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Get mouse position

                # Checks if mouse position is over a button
                # Perform corresponding action
                if button_info.collidepoint(*mouse_pos):
                    print('Show info')
                    drawer.show_help()

                if button_a.collidepoint(*mouse_pos):
                    print('A clicked, ', level.counter + 1)
                    drawer.animate_ab(font, bg, min_moves, buttons, 'a')
                    level.click_a()
                if button_b.collidepoint(*mouse_pos):
                    print('B clicked, ', level.counter + 1)
                    drawer.animate_ab(font, bg, min_moves, buttons, 'b')
                    level.click_b()
                if button_x.collidepoint(*mouse_pos):
                    print('X clicked, ', level.counter + 1)
                    drawer.animate_x(font, bg, min_moves, buttons)
                    level.click_x()

                if button_reset.collidepoint(*mouse_pos):
                    print("Reset level")
                    level.reset()

                if button_difficulty.collidepoint(*mouse_pos):
                    changed = False

                    # Check whether - or + was clicked
                    if button_min.collidepoint(*mouse_pos):
                        if difficulty > 4:  # 4 is minimum
                            difficulty -= 1
                            changed = True
                    else:
                        if difficulty < 8:  # 8 is maximum
                            difficulty += 1
                            changed = True

                    if changed:  # When minimum/maximum was not exceeded
                        print("Set difficulty {}".format(difficulty))

                        # Create new level with new difficulty
                        level = level_maker.get_random(difficulty)
                        drawer.level = level
                        solver = Solver(level)
                        min_moves, _ = solver.solve()

                if button_solve.collidepoint(*mouse_pos):
                    print('Show solution')
                    auto_solve = True

                    # Get solution for current level-state
                    # Solution is represented by sequence of actions to perform
                    solver = Solver(level)
                    _, min_actions = solver.solve()

                    # Execute and animate each action separately
                    for action in min_actions:
                        if action == 'a':
                            drawer.animate_ab(font, bg, min_moves, buttons, 'a')
                            level.click_a()
                        if action == 'b':
                            drawer.animate_ab(font, bg, min_moves, buttons, 'b')
                            level.click_b()
                        if action == 'x':
                            drawer.animate_x(font, bg, min_moves, buttons)
                            level.click_x()

                        # Redraw Level after each animated action
                        drawer.draw_level(font, bg, min_moves, buttons, animation=False)
                        pg.display.update()
                        pg.time.delay(500)  # So that animation can be followed

                # Redraw Level after each event
                drawer.draw_level(font, bg, min_moves, buttons, animation=False)

        pg.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    main()
