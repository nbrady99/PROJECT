# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 21:47:33 2024

@author: ebrad
"""

from graphics import *
import time


class Paddle:
    def __init__(self, win, x, y): # Creates the paddle specs, and draws it
        self.win = win
        self.x = x
        self.y = y
        self.width = 10
        self.height = 60
        self.paddle = Rectangle(Point(self.x, self.y), Point(self.x + self.width, self.y + self.height))
        self.paddle.setFill("white")
        self.paddle.draw(win)
        
    def moveUp(self): # Up when key is pressed, until it hits the top
      if self.y > 0:
          self.y -= 10
          self.paddle.move(0, -10)

    def moveDown(self): # Down when key is pressed, until it hits the bottom
      if self.y < 290:
          self.y += 10
          self.paddle.move(0, 10)
          
    def getPos(self): # Returs the position of ball
        return self.x, self.x + self.width, self.y, self.y + self.height
        
class Ball:
    def __init__(self, win, x, y): # Creates ball specs, and prints the ball
        self.win = win
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 2
        self.ball = Circle(Point(self.x, self.y), 10)
        self.ball.setFill("white")
        self.ball.draw(win)
        
    def moveBall(self): # Move function with set speed
        self.x += self.dx
        self.y += self.dy
        self.ball.move(self.dx, self.dy)
        
    def wallBounce(self): # Checks if the ball is hitting wall and forces to opposite direction
        if self.x <= 10 or self.x >= 590:
                self.dx = -self.dx
        if self.y <= 10 or self.y >= 340:
                self.dy = -self.dy
                
    def paddleBounce(self, paddle): # Checks if the ball hits the paddle and bounces off
        paddle_pos = paddle.getPos()
        
        if (self.ball.getP1().getX() <= paddle_pos[1] and self.ball.getP2().getX() >= paddle_pos[0]):
            if (paddle_pos[2] <= self.y + 10 <= paddle_pos[3]):
                self.dx = -self.dx
            
    def ballReset(self): # Sets ball to middle and makes it move
        self.ball.move(-self.x, -self.y)
        self.x = 300
        self.y = 125
        self.ball.move(self.x, self.y)

            
def main():
    # Draw functions, declaring objects
    win = GraphWin("Pong", 600, 350)
    win.setBackground("black")
    
    ball = Ball(win, 300, 125)
    paddle = Paddle(win, 40, 125)
    paddle2 = Paddle(win, 560, 125
                     )
    while True: # Main loop
    
        # Call ball functions
        ball.moveBall()
        ball.wallBounce()
        ball.paddleBounce(paddle)
        ball.paddleBounce(paddle2)
        
        time.sleep(0.005) # Pause for ball speed
        
        key = win.checkKey() # Get pressed key
       
        if key == "w":
            paddle.moveUp() #  UP if w
        elif key == "s":
            paddle.moveDown() # DOWN if s
            
        if key == "Up":
            paddle2.moveUp() # UP if arrow up
        elif key == "Down":
            paddle2.moveDown() # DOWN if arrow down
            
            # Checks if the ball went past paddles
        if (ball.x - 10 <= 0):
            ball.ballReset()
        if (ball.x + 10 >= 600):
            ball.ballReset()
    
    win.getMouse()
    win.close()
    
if __name__ == "__main__":
    main()