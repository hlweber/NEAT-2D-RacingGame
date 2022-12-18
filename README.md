<h1 align="center">
   <a href="#"> NEAT - 2D Racing Game </a>
</h1>

<h3 align="center">
    💻🏎️ Your computer winning a Race! 🏎️💻
</h3>

<h4 align="center"> 
	 Status: Finished
</h4>
<p align="center">
 <a href="#about">About</a> •
 <a href="#how-it-works">How it works</a> • 
 <a href="#results">Results</a> • 
 <a href="#author">Author</a> • 

</p>


## About

🏎️	2D Racing Game - NEAT

This project consists on building an 2D racing game and training a NEAT model for the computer learn how to play the game.

The whole project was written in python (pygame and neat).

There are two main python files, main_racing.py - where you can control the car by pressing directional keys | main_neat.py - where you can see the evolution of the model generations

---

## How it works

This project is divided into two parts:
1. Game Building
2. Model Training

### 1. Game Building

**The rules**:

On this game the player controls the movement of a car, the objective is complete a lap as fast as possible.

If the car hits the track 'walls' he bounces back, so avoiding hitting the walls is a good strategy.
 
--

**Mechanics**:

The game is built so the car can move forward and backward and it can rotate, to make left and right turns.

When the player chooses to move forward, the car will accelerate until he hits his max speed and the same its valid while moving backwards.

--

**Objects**:

There is only one object in this game, the car

--

### 2. Model Training

NEAT is a model that mutates and evolves given a fitness value - in this case, the greatest the fitness, the better.

In this model, the fitness increases when the car hits a checkpoint or finishes a lap.

And the fitness reduces when the car moves backwards or hits a wall.

For every car in each frame the model receives six inputs:

1. Car Angle
2. Distance to the wall if the angle was decreased by -90°
3. Distance to the wall if the angle was decreased by -45°
4. Distance to the wall if the angle was kept the same
5. Distance to the wall if the angle was increased by 45°
6. Distance to the wall if the angle was increased by 90°

And the model gives two outputs either the car should move forward, backward or do nothing. And either the car should rotate to the left, to the right or do nothing.

---

## Results

The computer was able to complete an lap after a few generations, put there are some room for improvement.

First, the best generation moves almost like an ant, changing its direction a lot, even when is not necessary, maybe implementing a mechanic that reduces the car speed when making a turn, would solve this behaviour.

Second, the increase of the fitness currently does not have relationship with time elapsed, adjusting this could make the cars goes faster

Lastly, the track is not perfect, there are some wall points that are not visual in some parts of the track that makes the car collide when it shouldn’t have.

Despite that, it's easy to perceive the evolution of the generations and the success of this model.


![](assets/evolution-racing_game.gif)

---

## Author

#### Henrique L. Weber

[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/henrique-weber/)](https://www.linkedin.com/in/henrique-weber/) 
[![Gmail Badge](https://img.shields.io/badge/-Email-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:hlweber@uol.com.br)](mailto:hlweber@uol.com.br)
