import pygame
import os
from cars import Car
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


def draw_window(win, cars, seconds, laps):
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

    time_label = STAT_FONT.render("Laps: " + str(laps), 1, (255, 255, 255))
    win.blit(time_label, (WIDTH - time_label.get_width() - 15, 10))


    for car in cars:
        car.draw(win)

    pygame.display.update()

def main():
    global WIN, gen

    win = WIN

    cars = []
    checkpoints = []

    game_speed = 60

    cars.append(Car(180,200, 0, car_img))
    checkpoints.append([0,0,0,0,0])

    laps = 0
    clock = pygame.time.Clock()
    begin_time = pygame.time.get_ticks()
    frames = 0
    run = True
    while run and len(cars)>0:
        clock.tick(game_speed)
        millis = pygame.time.get_ticks()
        seconds = (millis - begin_time) // 1000
        frames += 1
        draw_window(win, cars, seconds, laps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break


        keys = pygame.key.get_pressed()
        for x, car in enumerate(cars):
            moved = False
            if keys[pygame.K_UP]:
                car.move_forward()
                moved = True
            if keys[pygame.K_DOWN]:
                car.move_backward()
                moved = True
            if keys[pygame.K_LEFT]:
                car.steer_left()
            if keys[pygame.K_RIGHT]:
                car.steer_right()

            if not moved:
                car.reduce_speed()

            car.move()

        for x, car in enumerate(cars):
            if car.collide(track_border_mask) != None:
                car.hit()

        for x, car in enumerate(cars):
            finish_poi_collide = car.collide(finish_mask, *finish_pos)
            if finish_poi_collide != None:
                if finish_poi_collide[1] == 0:
                    car.hit()
                else:
                    laps +=1
                    cars.pop(x)
                    cars.append(Car(180,200, 0, car_img))



if __name__ == '__main__':
    main()