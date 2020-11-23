from graphics import *

def main():
    win = GraphWin('Floor', 500, 500)

    win.setCoords(0.0, 0.0, 10.0, 10.0)
    win.setBackground("yellow")

    # draw grid
    for x in range(10):
        for y in range(10):
            win.plotPixel(x*50, y*50, "blue")

    square = Rectangle(Point(5,5), Point(6,6))
    square.draw(win)
    square.setFill("black")

    win.getMouse()
    win.close()

main()
