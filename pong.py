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
mode = 2
clickPoint = 0

win = GraphWin("Pong", WIDTH, HEIGHT)
win.setBackground("black")


class Paddle:
    def __init__(self, win, x, y):  # Creates the paddle specs, and draws it
        self.win = win
        self.x = x
        self.y = y
        self.width = 10
        self.height = 80
        self.paddle = Rectangle(Point(self.x, self.y), Point(
            self.x + self.width, self.y + self.height))
        self.paddle.setFill("white")
        self.paddle.draw(win)

    def moveUp(self):  # Up when key is pressed, until it hits the top
        if self.y > 0:
            self.y -= 10
            self.paddle.move(0, -10)

    def moveDown(self):  # Down when key is pressed, until it hits the bottom
        if self.y < 320:
            self.y += 10
            self.paddle.move(0, 10)

    def getPos(self):  # Returs the position of ball
        return self.x, self.x + self.width, self.y, self.y + self.height
    
    def clearPaddle(self):
        self.paddle.undraw()


class Ball:
    def __init__(self, win, x, y):  # Creates ball specs, and prints the ball
        self.win = win
        self.x = x
        self.y = y
        angle = math.radians(23)
        self.dx = 1.3 * math.cos(angle) * (mode/1.5)
        self.dy = 2 * math.sin(angle) * (mode/1.5)
        self.ball = Circle(Point(self.x, self.y), 10)
        self.ball.setFill("white")
        self.ball.draw(win)

    def moveBall(self):  # Move function with set speed
        self.x += self.dx
        self.y += self.dy
        self.ball.move(self.dx, self.dy)
        time.sleep(0.005)

    def wallBounce(self):  # Checks if the ball is hitting wall and forces to opposite direction
        if self.x <= -10 or self.x >= WIDTH + 10:
            self.dx = -self.dx
        if self.y <= 10 or self.y >= HEIGHT - 10:
            self.dy = -self.dy

    def paddleBounce(self, paddle):  # Checks if the ball hits the paddle and bounces off
        paddlePos = paddle.getPos()
        if (self.ball.getP1().getX() <= paddlePos[1] and self.ball.getP2().getX() >= paddlePos[0]):
            if (paddlePos[2] <= self.y + 10 <= paddlePos[3]):
                self.dx = -self.dx   

    def ballReset(self):  # Sets ball to middle and makes it move
        time.sleep(0.1)
        self.ball.move(-self.x, -self.y)
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.ball.move(self.x, self.y)

    def outtaBounds(self, x): # Checks if ball goes past paddle
        if (x <= -10):
            self.ballReset()
            return False
        if (x >= WIDTH + 10):
            self.ballReset()
            return True
        
    def clearBall(self): # Remove ball
        self.ball.undraw()
        

class Score:
    def __init__(self, win): # Draw score, starts at 0
        self.win = win
        self.score = Text(Point((WIDTH/4)*3, 50), "0")
        self.score.setFill("grey")
        self.score.setSize(36)
        self.score.draw(win)

        self.score2 = Text(Point(WIDTH/4, 50), "0")
        self.score2.setFill("grey")
        self.score2.setSize(36)
        self.score2.draw(win)

    def getScore(ball, ballx): # Checks if went past paddle and adds a point
        global P1
        global P2

        if (ball.outtaBounds(ballx) == False):
            P1 += 1
            print("P1:", P1)
        if (ball.outtaBounds(ballx) == True):
            P2 += 1
            print("P2:", P2)

    def updateScore(self): # Update the score displayed
        self.score.setText(P1)
        self.score2.setText(P2)
    
    def printWinner(self): # Print GAME OVER when a player hits 11 pts
        if (P1 == 11 or P2 == 11):
            self.winner = Text(Point(350, 200), "GAME OVER")
            self.winner.setTextColor("White")
            self.winner.setSize(15)
            self.winner.draw(win)
        else: return
        return True
        
    def clearScore(self): # Undraw the scores
        self.score.undraw()
        self.score2.undraw()
        
    def clearWinner(self): # undraw Game Over text
        self.winner.undraw()
        

class gameBoard: # draw in game
    def __init__(self, win):
        self.win = win
        self.middleLines = [ ]
        y = 10
        
        while y < HEIGHT: # Loops to draw middle lines, stops when hits max height
            self.middleLine = Circle(Point(WIDTH / 2, y), 5)
            self.middleLine.setFill("grey")
            self.middleLine.draw(win)
            self.middleLines.append(self.middleLine)
            y += 20
        
        # Exit Rectangle
        self.rExit = Rectangle(Point(650, 0), Point(700, 23))
        self.rExit.setFill('Black')
        self.rExit.setOutline(("Black"))
        self.rExit.draw(win)

        # Exit Text
        self.tExit = Text(Point(675, 10), "EXIT")
        self.tExit.setTextColor("White")
        self.tExit.setSize(15)
        self.tExit.draw(win)

    def checkExit(self): # Check if user clicked exit
        clickPoint = self.win.checkMouse() # Check where they clicked

        if (clickPoint is not None and self.rExit.getP1().getX() <= clickPoint.getX() <= self.rExit.getP2().getX()
                and self.rExit.getP1().getY() <= clickPoint.getY() <= self.rExit.getP2().getY()):
            return True
        
    def clearGame(self): # Undraw game board, exit/lines
        self.tExit.undraw()
        self.rExit.undraw()
        
        for self.middleLine in self.middleLines:
            self.middleLine.undraw()
            

class mainMenu:
    def __init__(self, win):

        # Draw PLAY
        self.win = win
        self.rPlay = Rectangle(Point(275, 170), Point(426, 218))
        self.rPlay.setFill("Black")
        self.rPlay.draw(win)

        self.tPlay = Text(Point(349, 195), "PLAY")
        self.tPlay.setTextColor("White")
        self.tPlay.setSize(45)
        self.tPlay.draw(win)

        # Draw SETTING
        self.rSetting = Rectangle(Point(198, 230), Point(498, 278))
        self.rSetting.setFill('Black')
        self.rSetting.draw(win)

        self.tSetting = Text(Point(349, 255), "SETTINGS")
        self.tSetting.setTextColor("White")
        self.tSetting.setSize(45)
        self.tSetting.draw(win)

        # Draw LOGO
        self.p = Text(Point(350, 45), "PONG")
        self.p.setTextColor("White")
        self.p.setSize(60)
        self.p.draw(win)

        self.r = Text(Point(350, 90), "REMASTERED")
        self.r.setTextColor("White")
        self.r.setSize(18)
        self.r.draw(win)

    def checkPlay(self): # Check if user clicked PLAY
        if (self.rPlay.getP1().getX() <= clickPoint.getX() <= self.rPlay.getP2().getX()
                and self.rPlay.getP1().getY() <= clickPoint.getY() <= self.rPlay.getP2().getY()):
            return True

    def checkSettings(self): # Check if user clicked SETTINGS
        if (self.rSetting.getP1().getX() <= clickPoint.getX() <= self.rSetting.getP2().getX()
                and self.rSetting.getP1().getY() <= clickPoint.getY() <= self.rSetting.getP2().getY()):
            return True

    def clearMenu(self): # Undraw main menu for settings or in game
        self.tPlay.undraw()
        self.rPlay.undraw()
        self.tSetting.undraw()
        self.rSetting.undraw()
        self.p.undraw()
        self.r.undraw()

        time.sleep(0.6)
        

class settingMenu: # Draw the setting options
    def __init__(self, win):
        self.win = win
        
        # Difficulty label
        self.tDiff = Text(Point(349, 110), "DIFFICULTY MODE:")
        self.tDiff.setTextColor("White")
        self.tDiff.setSize(25)
        self.tDiff.draw(win)

        # EASY BUTTON
        self.rEasy = Rectangle(Point(155, 127), Point(263, 160))
        self.rEasy.setFill('Black')
        self.rEasy.setOutline(("Black"))
        self.rEasy.draw(win)

        self.tEasy = Text(Point(208, 145), "EASY")
        self.tEasy.setTextColor("White")
        self.tEasy.setSize(30)
        self.tEasy.draw(win)
        
        # MEDIUM BUTTON
        self.rMed = Rectangle(Point(269, 127), Point(429, 160))
        self.rMed.setFill('Black')
        self.rMed.setOutline(("Black"))
        self.rMed.draw(win)

        self.tMed = Text(Point(349, 145), "MEDIUM")
        self.tMed.setTextColor("White")
        self.tMed.setSize(30)
        self.tMed.draw(win)

        # HARD BUTTON
        self.rHard = Rectangle(Point(439, 127), Point(552, 160))
        self.rHard.setFill('Black')
        self.rHard.setOutline(("Black"))
        self.rHard.draw(win)

        self.tHard = Text(Point(495, 145), "HARD")
        self.tHard.setTextColor("White")
        self.tHard.setSize(30)
        self.tHard.draw(win)

        # BACK BUTTON
        self.rBack = Rectangle(Point(3, 2), Point(77, 27))
        self.rBack.setFill('Black')
        self.rBack.setOutline(("Black"))
        self.rBack.draw(win)

        self.tBack = Text(Point(40, 15), "BACK")
        self.tBack.setTextColor("White")
        self.tBack.setSize(20)
        self.tBack.draw(win)

        if (mode == 1): # Set the selected mode to grey to shows it's selected
            self.tEasy.setTextColor("Grey")
        elif (mode == 2):
            self.tMed.setTextColor("Grey")
        elif (mode == 3):
            self.tHard.setTextColor("Grey")

    def checkBack(self): # Check if user clicked back
        clickPoint = self.win.getMouse()
        if (self.rBack.getP1().getX() <= clickPoint.getX() <= self.rBack.getP2().getX()
                and self.rBack.getP1().getY() <= clickPoint.getY() <= self.rBack.getP2().getY()):
            return True

    def checkOption(self): # Check what option was selected and changes the color to grey
        clickPoint = self.win.getMouse()
        global mode

            # HARD SELECTION
        if (self.rHard.getP1().getX() <= clickPoint.getX() <= self.rHard.getP2().getX()
                and self.rHard.getP1().getY() <= clickPoint.getY() <= self.rHard.getP2().getY()):
            self.tHard.setTextColor("Grey")
            self.tEasy.setTextColor("White")
            self.tMed.setTextColor("White")

            mode = 3
            
            # MEDIUM SELECTION
        if (self.rMed.getP1().getX() <= clickPoint.getX() <= self.rMed.getP2().getX()
                and self.rMed.getP1().getY() <= clickPoint.getY() <= self.rMed.getP2().getY()):
            self.tMed.setTextColor("Grey")
            self.tHard.setTextColor("White")
            self.tEasy.setTextColor("White")

            mode = 2
            
            # EASY SELECTION
        if (self.rEasy.getP1().getX() <= clickPoint.getX() <= self.rEasy.getP2().getX()
                and self.rEasy.getP1().getY() <= clickPoint.getY() <= self.rEasy.getP2().getY()):
            self.tEasy.setTextColor("Grey")
            self.tHard.setTextColor("White")
            self.tMed.setTextColor("White")

            mode = 1

    def clearSettings(self): # UNDRAW all settings for when user goes back to main menu
        self.tDiff.undraw()
        self.rBack.undraw()
        self.tBack.undraw()
        self.rEasy.undraw()
        self.tEasy.undraw()
        self.rMed.undraw()
        self.tMed.undraw()
        self.tHard.undraw()
        self.rHard.undraw()

        time.sleep(0.6) # Quick pause
        

def main():
    # Draw functions, declaring objects
    menu = mainMenu(win)
    switch = True
    inSettings = False
    global gSettings
    global clickPoint
    global P1, P2

    while switch:
        clickPoint = win.getMouse()
        if (menu.checkPlay() == True and inSettings == False):
            switch = False
            break
        if (menu.checkSettings() == True):
            menu.clearMenu()
            gSettings = settingMenu(win)
            while (gSettings.checkBack() != True):
                gSettings.checkOption()
            gSettings.clearSettings()
            menu = mainMenu(win)
            inSettings = False

    menu.clearMenu()
    game = gameBoard(win)
    score = Score(win)
    ball = Ball(win, WIDTH / 2, HEIGHT / 2)
    paddle = Paddle(win, 20, HEIGHT / 2)
    paddle2 = Paddle(win, 670, HEIGHT / 2)

    while True:  # Main loop
        winner = score.printWinner()
        
        if (game.checkExit() == True or winner == True): # Undraw game board if someone won or if EXIT
            
            paddle.clearPaddle()
            paddle2.clearPaddle()
            ball.clearBall()
            score.clearScore()
            game.clearGame()
            
            # Set score back to 0
            P1 = 0
            P2 = 0
            
            if (winner):
                time.sleep(3)
                score.clearWinner()
            else:
                time.sleep(0.6)
            main()

        # Call and update ball/score functions
        ball.moveBall()
        ball.wallBounce()
        ball.paddleBounce(paddle)
        ball.paddleBounce(paddle2)
        Score.getScore(ball, ball.x)
        score.updateScore()
        ball.outtaBounds(ball.x)

        key = win.checkKey()  # Get pressed key

        if key == "w":
            paddle.moveUp()  # UP if w
        elif key == "s":
            paddle.moveDown()  # DOWN if s

        if key == "Up":
            paddle2.moveUp()  # UP if arrow up
        elif key == "Down":
            paddle2.moveDown()  # DOWN if arrow down

    win.getMouse()
    

if __name__ == "__main__":
    main()