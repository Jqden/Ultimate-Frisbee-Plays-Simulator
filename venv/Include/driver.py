import pygame
from Include.offender import Offender
from Include.button import Button
from Include.defender import Defender
from Include.dot import Dot
import math

# define constants
GREEN = (119, 221, 119)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
FIELD_WIDTH = 200
FIELD_HEIGHT = 600
TOOLBAR_WIDTH = 30


def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Whiteboard")

    # create a surface on screen
    screen = pygame.display.set_mode((FIELD_WIDTH+TOOLBAR_WIDTH, FIELD_HEIGHT))

    # define variables to control the main loop
    clock = pygame.time.Clock()
    offenders = pygame.sprite.Group()
    defenders = pygame.sprite.Group()
    all_players = pygame.sprite.Group()
    dots = pygame.sprite.Group()
    button = pygame.sprite.GroupSingle(Button([FIELD_WIDTH + 3, 3], 24))
    game_state = 0  # 0 is placing players, 1 is altering players, 2 is running the simulation
    player_to_alter = None
    hovered_player = None

    running = True

    # main loop
    while running:
        # See if mouse hovers over any players before every non-simulation loop
        # If it does, highlight that player
        if game_state != 2:
            none_hovered = True
            for player in all_players:
                if player.rect.collidepoint(pygame.mouse.get_pos()):  # if player hovered over
                    none_hovered = False
                    if hovered_player:  # if we were previously hovering over a player
                        if player is not hovered_player:  # if mouse goes directly from hovered player to another player
                            hovered_player.set_main_color()
                            hovered_player = player
                            hovered_player.set_off_color()
                    else:
                        hovered_player = player
                        hovered_player.set_off_color()
            if none_hovered:
                if hovered_player:  # if a player was hovered last iteration, change them back to normal
                    hovered_player.set_main_color()
                    hovered_player = None

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # immediately exit the main loop
                running = False
                break
            # Placing Players Game State (the default state of the simulator)
            if game_state == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # press SPACE to run simulation
                        game_state = 2
                        print("Running sim")
                    elif event.key == pygame.K_r:  # press R to reset the players to original positions
                        for offender in offenders:
                            offender.reset_path()
                        defenders.update()
                        print("All Positions Reset")
                elif event.type == pygame.MOUSEBUTTONUP:  # mouse clicked
                    if pygame.mouse.get_pos()[0] < FIELD_WIDTH:
                        # check if the mouse clicked on a player
                        for player in all_players:
                            if player.rect.collidepoint(pygame.mouse.get_pos()):  # if player clicked on
                                player_to_alter = player
                                if isinstance(player, Offender):  # if player offense, go to adjusting offender
                                    for c, point in enumerate(player.get_original_points()):  # dots show player's path
                                        if player.path[c] != (player.rect.x, player.rect.y):
                                            dots.add(Dot(point))
                                    game_state = 1.1
                                    print("Alter offender")
                                elif isinstance(player, Defender):  # if player defense, go to adjusting defender
                                    game_state = 1.2
                                    print("Alter defender")
                                player_to_alter.lock_off_color()  # keep the player highlighted
                                break
                        # mouse didn't click on an existing player, so place a new player
                        # the type of player (offense or defense) corresponds to the color of the button (red or blue)
                        if not math.floor(game_state) == 1:
                            if button.sprite.color == button.sprite.o_color:
                                new_player = Offender(pygame.mouse.get_pos())
                                offenders.add(new_player)
                                all_players.add(new_player)
                            else:
                                new_player = Defender(pygame.mouse.get_pos())
                                defenders.add(new_player)
                                all_players.add(new_player)
                    else:  # see if mouse clicked on the button
                        if button.sprite.rect.collidepoint(pygame.mouse.get_pos()):
                            button.update()
            # Altering a Player Game State
            elif math.floor(game_state) == 1:
                if game_state == 1.1:  # Offensive player
                    # if mouse clicked on field, add the click point to player's path
                    if event.type == pygame.MOUSEBUTTONUP:
                        if pygame.mouse.get_pos()[0] < FIELD_WIDTH:
                            player_to_alter.add_point(pygame.mouse.get_pos())
                            print("Adding point:", (pygame.mouse.get_pos()))
                            dots.add(Dot(pygame.mouse.get_pos()))
                    elif event.type == pygame.KEYDOWN:
                        exit_altering = False
                        if event.key == pygame.K_s:  # press S to save the path
                            print("Saved path:", player_to_alter.path)
                            exit_altering = True
                        elif event.key == pygame.K_c:  # pres C to clear the path
                            player_to_alter.clear_path()
                            print("Cleared path")
                            exit_altering = True
                        elif event.key == pygame.K_r:  # press R to reset just this player's position
                            player_to_alter.reset_path()
                            defenders.update()
                            exit_altering = True
                        if exit_altering:  # clean up before going back to default game state
                            player_to_alter.unlock_main_color()
                            player_to_alter = None
                            dots.empty()
                            game_state = 0
                elif game_state == 1.2:  # Defensive player
                    # if an offensive player is clicked, assign the defense to that player
                    if event.type == pygame.MOUSEBUTTONUP:
                        for offender in offenders:
                            if offender.rect.collidepoint(pygame.mouse.get_pos()):
                                player_to_alter.assign_offender(offender)
                                player_to_alter.unlock_main_color()
                                player_to_alter = None
                                game_state = 0
                                print("Assigned to offender")
                # Shared behavior for altering offense and defense
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:  # press BACKSPACE to del a player
                    all_players.remove(player_to_alter)
                    if isinstance(player_to_alter, Offender):
                        dots.empty()
                        offenders.remove(player_to_alter)
                    else:
                        defenders.remove(player_to_alter)
                    game_state = 0
                    print("Deleted player")

        # set the screen background to an ultimate field
        screen.fill(GREEN)
        pygame.draw.lines(screen, WHITE, False, [(0, 125), (FIELD_WIDTH, 125)], 4)
        pygame.draw.lines(screen, WHITE, False, [(0, 475), (FIELD_WIDTH, 475)], 4)
        # draw the toolbar
        pygame.draw.rect(screen, GRAY, pygame.Rect(FIELD_WIDTH+1, 0, TOOLBAR_WIDTH, FIELD_HEIGHT))
        button.draw(screen)
        # draw on the field
        all_players.draw(screen)
        dots.draw(screen)
        # if simulation is running, check to see if it just ended.
        # if not, update all the players
        if game_state == 2:
            sim_running = False
            for offender in offenders:
                if not offender.path_completed():
                    sim_running = True
                    break
            if sim_running:
                all_players.update()
            else:
                game_state = 0
                print("Sim over")

        # update the screen
        pygame.display.flip()
        clock.tick(60)


# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    main()
