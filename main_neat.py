import pygame
import os
from cars import Car
import neat
pygame.font.init()  # init font

car_img_original = pygame.image.load(os.path.join("img","red-car.png"))
car_img = pygame.transform.scale(car_img_original, (car_img_original.get_size()[0]*0.55, car_img_original.get_size()[1]*0.55))

bg_img_original = pygame.image.load("img/grass.jpg")
bg_img = pygame.transform.scale(bg_img_original, (bg_img_original.get_size()[0]*2.5, bg_img_original.get_size()[1]*2.5))

track_img_original = pygame.image.load(os.path.join("img","track2.png"))
track_img = pygame.transform.scale(track_img_original, (track_img_original.get_size()[0]*0.9, track_img_original.get_size()[1]*0.9))

track_border_img_original = pygame.image.load(os.path.join("img","track-border2.png"))
track_border_img = pygame.transform.scale(track_border_img_original, (track_border_img_original.get_size()[0]*0.9, track_border_img_original.get_size()[1]*0.9))
track_border_mask = pygame.mask.from_surface(track_border_img)

finish_img = pygame.image.load("img/finish.png")
finish_mask = pygame.mask.from_surface(finish_img)
finish_pos = (130, 250)

# CHECK POINTS
# 1
checkpoint_img1_nr = pygame.image.load("img/checkpoint.png")
checkpoint_img1 = pygame.transform.rotate(checkpoint_img1_nr, 90)
checkpoint_mask1 = pygame.mask.from_surface(checkpoint_img1)
checkpoint_pos1 = (120, 25)
# 2
checkpoint_img2_nr = pygame.image.load("img/checkpoint.png")
checkpoint_img2 = pygame.transform.rotate(checkpoint_img2_nr, 0)
checkpoint_mask2 = pygame.mask.from_surface(checkpoint_img2)
checkpoint_pos2 = (20, 460)
# 3
checkpoint_img3_nr = pygame.image.load("img/checkpoint.png")
checkpoint_img3 = pygame.transform.rotate(checkpoint_img3_nr, 90)
checkpoint_mask3 = pygame.mask.from_surface(checkpoint_img3)
checkpoint_pos3 = (340, 690)
# 4
checkpoint_img4_nr = pygame.image.load("img/checkpoint.png")
checkpoint_img4 = pygame.transform.rotate(checkpoint_img4_nr, 90)
checkpoint_mask4 = pygame.mask.from_surface(checkpoint_img4)
checkpoint_pos4 = (670, 690)
# 5
checkpoint_img5_nr = pygame.image.load("img/checkpoint.png")
checkpoint_img5 = pygame.transform.rotate(checkpoint_img5_nr, 90)
checkpoint_mask5 = pygame.mask.from_surface(checkpoint_img5)
checkpoint_pos5 = (670, 220)



WIDTH, HEIGHT = track_img.get_width(), track_img.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

STAT_FONT = pygame.font.SysFont("comicsans", 50)

gen = 0


def draw_window(win, cars, seconds, gen):
    win.blit(bg_img, (0, 0))
    win.blit(track_img, (0, 0))
    win.blit(finish_img, finish_pos)
    win.blit(checkpoint_img1, checkpoint_pos1)
    win.blit(checkpoint_img2, checkpoint_pos2)
    win.blit(checkpoint_img3, checkpoint_pos3)
    win.blit(checkpoint_img4, checkpoint_pos4)
    win.blit(checkpoint_img5, checkpoint_pos5)
    win.blit(track_border_img, (0, 0))

    time_label = STAT_FONT.render("Time: " + str(seconds), 1, (255, 255, 255))
    win.blit(time_label, (WIDTH - time_label.get_width() - 15, 50))

    # generations
    gen_label = STAT_FONT.render("Gens: " + str(gen - 1), 1, (255, 255, 255))
    win.blit(gen_label, (WIDTH - time_label.get_width() - 15, 10))


    for car in cars:
        car.draw(win)

    pygame.display.update()

def main(genomes, config):
    global WIN, gen

    win = WIN
    gen += 1

    nets = []
    cars = []
    ge = []
    checkpoints = []

    game_speed = 60

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car(180,200, 0, car_img))
        checkpoints.append([0,0,0,0,0])
        ge.append(genome)


    clock = pygame.time.Clock()
    begin_time = pygame.time.get_ticks()
    frames = 0
    run = True
    while run and len(cars)>0:
        clock.tick(game_speed)
        millis = pygame.time.get_ticks()
        seconds = (millis - begin_time) // 1000
        frames += 1
        draw_window(win, cars, seconds, gen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        for x, car in enumerate(cars):
            ge[x].fitness += 0.1*car.speed
            moved = False
            inputs = car.calc_inputs(track_border_mask)
            outputs = nets[x].activate((inputs))
            if outputs[1] > 0.5:
                car.move_forward()
                moved = True
            elif outputs[1] < -0.5:
                car.move_backward()
                ge[x].fitness -= 1
                moved = True

            if outputs[0] > 0.5:
                car.steer_left()
            elif outputs[0] < -0.5:
                car.steer_right()

            if not moved:
                car.reduce_speed()

            car.move()

        for x, car in enumerate(cars):
            if car.collide(track_border_mask) != None:
                ge[x].fitness -= 3
                cars.pop(x)
                nets.pop(x)
                ge.pop(x)
                checkpoints.pop(x)

        for x, car in enumerate(cars):
            finish_poi_collide = car.collide(finish_mask, *finish_pos)
            if finish_poi_collide != None:
                if finish_poi_collide[1] == 0:
                    ge[x].fitness -= 100
                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    checkpoints.pop(x)
                else:
                    ge[x].fitness += 100
                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    checkpoints.pop(x)
                    print("finish")

        for x, car in enumerate(cars):
            checkpoint_poi1 = car.collide(checkpoint_mask1, *checkpoint_pos1)
            if checkpoint_poi1 != None:
                if checkpoints[x][0] == 0:
                    if checkpoint_poi1[1] == 0:
                        ge[x].fitness -= 10
                        cars.pop(x)
                        nets.pop(x)
                        ge.pop(x)
                        checkpoints.pop(x)
                    else:
                        ge[x].fitness += 10
                        checkpoints[x][0] = 1

        for x, car in enumerate(cars):
            checkpoint_poi2 = car.collide(checkpoint_mask2, *checkpoint_pos2)
            if checkpoint_poi2 != None:
                if checkpoints[x][1] == 0:
                    if checkpoint_poi2[1] == 0:
                        ge[x].fitness += 20
                        checkpoints[x][1] = 1
                    else:
                        ge[x].fitness -= 10
                        cars.pop(x)
                        nets.pop(x)
                        ge.pop(x)
                        checkpoints.pop(x)

        for x, car in enumerate(cars):
            checkpoint_poi3 = car.collide(checkpoint_mask3, *checkpoint_pos3)
            if checkpoint_poi3 != None:
                if checkpoints[x][2] == 0:
                    if checkpoint_poi3[1] == 0:
                        ge[x].fitness -= 10
                        cars.pop(x)
                        nets.pop(x)
                        ge.pop(x)
                        checkpoints.pop(x)
                    else:
                        ge[x].fitness += 30
                        checkpoints[x][2] = 1

        for x, car in enumerate(cars):
            checkpoint_poi4 = car.collide(checkpoint_mask4, *checkpoint_pos4)
            if checkpoint_poi4 != None:
                if checkpoints[x][3] == 0:
                    if checkpoint_poi4[1] == 0:
                        ge[x].fitness -= 10
                        cars.pop(x)
                        nets.pop(x)
                        ge.pop(x)
                        checkpoints.pop(x)
                    else:
                        ge[x].fitness += 40
                        checkpoints[x][3] = 1

        for x, car in enumerate(cars):
            checkpoint_poi5 = car.collide(checkpoint_mask5, *checkpoint_pos5)
            if checkpoint_poi5 != None:
                if checkpoints[x][4] == 0:
                    if checkpoint_poi5[1] == 0:
                        ge[x].fitness -= 10
                        cars.pop(x)
                        nets.pop(x)
                        ge.pop(x)
                        checkpoints.pop(x)
                    else:
                        ge[x].fitness += 50
                        checkpoints[x][4] = 1

        if seconds > 2:
            for x, car in enumerate(cars):
                if sum(checkpoints[x]) == 0:
                    ge[x].fitness -= 100
                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    checkpoints.pop(x)

        if seconds > 15:
            for x, car in enumerate(cars):
                if sum(checkpoints[x]) == 1:
                    ge[x].fitness -= 50
                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    checkpoints.pop(x)

        if seconds>40:
            break


def run(config_file):
    #runs the NEAT algorithm to train a neural network to play the racing game
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(main, 200)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file..
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)