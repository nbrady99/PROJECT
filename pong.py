# -*- coding: utf-8 -*-
"""

@author: nbrady
"""

from graphics import *
import time
import math

WIDTH = 700
HEIGHT = 400
P1 = 0
P2 = 0
 
class Paddle:
    def __init__(self, win, x, y): # Creates the paddle specs, and draws it
        self.win = win
        self.x = x
        self.y = y
        self.width = 10
        self.height = 80
        self.paddle = Rectangle(Point(self.x, self.y), Point(self.x + self.width, self.y + self.height))
        self.paddle.setFill("white")
        self.paddle.draw(win)
        
    def moveUp(self): # Up when key is pressed, until it hits the top
      if self.y > 0:
          self.y -= 10
          self.paddle.move(0, -10)

    def moveDown(self): # Down when key is pressed, until it hits the bottom
      if self.y < 320:
          self.y += 10
          self.paddle.move(0, 10)
          
    def getPos(self): # Returs the position of ball
        return self.x, self.x + self.width, self.y, self.y + self.height
        
class Ball:
    def __init__(self, win, x, y): # Creates ball specs, and prints the ball
        self.win = win
        self.x = x
        self.y = y
        angle = math.radians(23)
        self.dx = 1.3 * math.cos(angle)
        self.dy = 2 * math.sin(angle)
        self.ball = Circle(Point(self.x, self.y), 10)
        self.ball.setFill("white")
        self.ball.draw(win)
        
    def moveBall(self): # Move function with set speed
        self.x += self.dx
        self.y += self.dy
        self.ball.move(self.dx, self.dy)
        time.sleep(0.005)
        
    def wallBounce(self): # Checks if the ball is hitting wall and forces to opposite direction
        if self.x <= -10 or self.x >= WIDTH + 10:
                self.dx = -self.dx
        if self.y <= 10 or self.y >= HEIGHT - 10:
                self.dy = -self.dy
                
    def paddleBounce(self, paddle): # Checks if the ball hits the paddle and bounces off
        paddle_pos = paddle.getPos()
        if (self.ball.getP1().getX() <= paddle_pos[1] and self.ball.getP2().getX() >= paddle_pos[0]):
            if (paddle_pos[2] <= self.y + 10 <= paddle_pos[3]):
                self.dx = -self.dx
                
    def ballReset(self): # Sets ball to middle and makes it move
        time.sleep(0.1)
        self.ball.move(-self.x, -self.y)
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.ball.move(self.x, self.y)
        
    def outtaBounds(self, x):
        if (x <= -10):
            self.ballReset()
            return False
        if (x >= WIDTH + 10):
            self.ballReset()
            return True
      
class Score:
    def __init__(self, win):
        self.win = win
        self.score = Text(Point((WIDTH/4)*3, 50), "0")
        self.score.setFill("grey")
        self.score.setSize(36)
        self.score.draw(win)
        
        self.score2 = Text(Point(WIDTH/4, 50), "0")
        self.score2.setFill("grey")
        self.score2.setSize(36)
        self.score2.draw(win)
        
    def getScore(ball, ballx): 
        global P1
        global P2
        
        if (ball.outtaBounds(ballx) == False):
            P1 += 1
            print("P1:", P1)
        if (ball.outtaBounds(ballx) == True):
            P2 += 1
            print("P2:", P2)
            
    def updateScore(self):
        self.score.setText(P1)
        self.score2.setText(P2)

class gameBoard:
    def __init__(self, win):
        self.win = win
        y = 10
        
        while y < HEIGHT:
            middleLine = Circle(Point(WIDTH / 2, y), 5)
            middleLine.setFill("grey")
            middleLine.draw(win)
            y += 20
            
class mainMenu:
    def __init__(self, win):
        self.win = win
        self.play = Text(Point((WIDTH/2), 100), "PLAY")
            
def main():
    # Draw functions, declaring objects
    win = GraphWin("Pong", WIDTH, HEIGHT)
    win.setBackground("black")
    
    ball = Ball(win, WIDTH / 2, HEIGHT / 2)
    paddle = Paddle(win, 20, HEIGHT / 2)
    paddle2 = Paddle(win, 670, HEIGHT / 2)
    score = Score(win)
    gameBoard(win)
    
    while True: # Main loop
    
        # Call ball functions
        ball.moveBall()
        ball.wallBounce()
        ball.paddleBounce(paddle)
        ball.paddleBounce(paddle2)
        Score.getScore(ball, ball.x)
        score.updateScore()
        ball.outtaBounds(ball.x)
        
        key = win.checkKey() # Get pressed key
       
        if key == "w":
            paddle.moveUp() #  UP if w
        elif key == "s":
            paddle.moveDown() # DOWN if s
            
        if key == "Up":
            paddle2.moveUp() # UP if arrow up
        elif key == "Down":
            paddle2.moveDown() # DOWN if arrow down
    
    win.getMouse()
    win.close()
    
if __name__ == "__main__":
    main()