#!/usr/bin/env python
import random
import pygame
import pygame.gfxdraw
import Actor
import cfg


def main():
    init()
    main_loop()


def init():

    pygame.init()

    cfg.SURFACE_MAIN = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
    cfg.PLAYER = Actor.Player()

    cfg.PLAYER.x = (int)(cfg.SCREEN_WIDTH / 2 - (cfg.PLAYER.width / 2))
    cfg.PLAYER.y = (int)(cfg.SCREEN_HEIGHT / 2 - (cfg.PLAYER.height / 2))
    cfg.PLAYER.add(cfg.ACTORS, cfg.INFECTED)

    for i in range(0, cfg.INIT_ACTORS):
        new_actor = Actor.Circle()
        new_actor.x = random.randint(0, cfg.SCREEN_WIDTH - new_actor.width)
        new_actor.y = random.randint(0, cfg.SCREEN_HEIGHT - new_actor.height)
        new_actor.add(cfg.ACTORS, cfg.AI_ACTORS, cfg.HEALTHY)


def main_loop():

    run_loop = True

    while run_loop:

        run_loop = process_events()
        process_player_input()
        process_ai_input()
        move_actors()
        handle_collisions()
        kill_actors()
        generate_new_actors()
        draw()
        pygame.time.wait(cfg.REFRESH_DELAY)

    pygame.quit()
    exit()


def process_events():
    # Returns whether to keep running the main loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True


def process_player_input():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        cfg.PLAYER.vert_accel(1)
    if pressed[pygame.K_DOWN]:
        cfg.PLAYER.vert_accel(-1)
    if pressed[pygame.K_RIGHT]:
        cfg.PLAYER.hori_accel(1)
    if pressed[pygame.K_LEFT]:
        cfg.PLAYER.hori_accel(-1)

    if pressed[pygame.K_ESCAPE]:
        print("abort!")
        # todo: abort


def move_actors():
    for actor in cfg.ACTORS:
        actor.move()


def handle_collisions():
    collisions = set()
    for infected in cfg.INFECTED.sprites():
        collisions.update(infected.collided_with(cfg.HEALTHY))

    for collision in collisions:
        # 75% chance of infection every 50ms of contact
        if checkTimeInterval(cfg.INFECTION_INTERVAL) and checkProbability(cfg.INFECTION_PROB):
            print("INFECTED! size: %d" % collision.width)
            collision.color = cfg.INFECTED_COLOR
            collision.image = collision.load_sprite()
            cfg.INFECTED.add(collision)
            cfg.HEALTHY.remove(collision)


def kill_actors():
    """Infected actors have a 20% chance of dying every 1000ms"""
    for actor in cfg.INFECTED.sprites():
        if actor is cfg.PLAYER:
            continue
        if checkTimeInterval(cfg.KILL_INTERVAL) and checkProbability(cfg.KILL_PROB):
            actor.die()


def generate_new_actors():
    """
    50% chance of generation every 200ms if less than MAX_ACTORS
    Circles shoot in from the sides
    """
    if len(cfg.AI_ACTORS) < cfg.MAX_ACTORS and checkTimeInterval(cfg.GENERATION_INTERVAL) and checkProbability(cfg.GENERATION_PROB):

        new_circle = Actor.Circle()
        new_circle.x = 0 - new_circle.width if checkProbability(0.5) else cfg.SCREEN_WIDTH
        new_circle.y = random.randint(0, cfg.SCREEN_HEIGHT - new_circle.height)

        initial_v = random.randint(new_circle.MOVE_SPEED, new_circle.MAX_SPEED)
        direction = 1 if new_circle.x < 0 else -1
        new_circle.x_speed = initial_v * direction

        new_circle.add(cfg.ACTORS, cfg.AI_ACTORS, cfg.HEALTHY)


def process_ai_input():
    """Each actor has a 25% chance of random movement every 100ms"""
    for actor in cfg.AI_ACTORS.sprites():
        if checkTimeInterval(cfg.MOVE_INTERVAL) and checkProbability(cfg.MOVE_PROB):
            actor.hori_accel(random.randint(-1 * actor.MOVE_SPEED, actor.MOVE_SPEED))
            actor.vert_accel(random.randint(-1 * actor.MOVE_SPEED, actor.MOVE_SPEED))


def checkTimeInterval(interval):
    return pygame.time.get_ticks() % interval < cfg.REFRESH_DELAY


def checkProbability(probability):
    return random.random() < probability


def draw():
    cfg.SURFACE_MAIN.fill(cfg.BG_COLOR)

    for actor in cfg.ACTORS:
        cfg.SURFACE_MAIN.blit(actor.image, actor.get_pos())

    pygame.display.flip()


main()
