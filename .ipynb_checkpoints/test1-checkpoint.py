{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# A guide to how to create graphical things"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "from graphics import *\n",
    "\n",
    "def main():\n",
    "    win = GraphWin('Floor', 500, 500)\n",
    "\n",
    "    win.setCoords(0.0, 0.0, 10.0, 10.0)\n",
    "    win.setBackground(\"yellow\")\n",
    "\n",
    "    # draw grid\n",
    "    for x in range(10):\n",
    "        for y in range(10):\n",
    "            win.plotPixel(x*50, y*50, \"blue\")\n",
    "\n",
    "    square = Rectangle(Point(5,5), Point(6,6))\n",
    "    square.draw(win)\n",
    "    square.setFill(\"black\")\n",
    "\n",
    "    win.getMouse()\n",
    "    win.close()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
