# Name: Dots and Boxes
# Date: June 2016
# Creator: Nayely Martinez (nayely.e.martinez@gmail.com)
# A Python version of the classic two-player Dots and Boxes games.
# 	Players take turns trying to fill in as many boxes as possible.

import sys
# generally people try not to import *, since it can make it confusing
# what module variables are coming from. in your case since there's
# only one module it's relatively clear, but still something to be aware of :)
#
# a good alternative if you need a lot of things from a module is
# `import graphics as g`, and then refer to things as `g.Whatever`.
from graphics import *


class Board:

    LINE_WIDTH = 6

    def __init__(self, board_size):
        self.board_size = board_size
        self.empty_lines = []
        self.chosen_lines = []
        self.circles = []
        self.win = None
        self.create_board()

        return

    def line_is_vertical(self, line):
        return line.getP1().getX() == line.getP2().getX()

    def line_is_horizontal(self, line):
        return line.getP1().getY() == line.getP2().getY()

    def is_click_inside_line(self, click, line):
        PADDING = 4

        click_x = click.getX()
        click_y = click.getY()

        p1x = line.getP1().getX()
        p1y = line.getP1().getY()
        p2x = line.getP2().getX()
        p2y = line.getP2().getY()

        if self.line_is_vertical(line):
            x_range = click_x >= (p1x - PADDING) and click_x <= (p1x + PADDING)
            y_range = click_y >= p1y and click_y <= p2y
        elif self.line_is_horizontal(line):
            y_range = click_y >= (p1y - PADDING) and click_y <= (p1y + PADDING)
            x_range = click_x >= p1x and click_x <= p2x
        return x_range and y_range

    def get_line_from_click(self, click):
        for line in self.empty_lines:
            if self.is_click_inside_line(click, line):
                return line
        return None

    # Returns line object from array given clicked line
    #
    # I'm not going to write it out but there's probably opportunities
    # for refactoring here similar to those in get_line_from_click
    def get_line(self, clicked_line):
        x1 = clicked_line.getP1().getX()
        y1 = clicked_line.getP1().getY()
        x2 = clicked_line.getP2().getX()
        y2 = clicked_line.getP2().getY()
        x_range = False
        y_range = False

        for line in self.chosen_lines:
            if x1 == line.getP1().getX() and y1 == line.getP1().getY() and x2 == line.getP2().getX() and y2 == line.getP2().getY():
                if line.getP1().getX() == line.getP2().getX():
                    pass
                    #print("It's a match! Neighbor line matches vertical line in chosen_lines")
                elif line.getP1().getY() == line.getP2().getY():
                    pass
                    #print("It's a match! Neighbor line matches horizontal line in chosen_lines")
                return line

        #print("No line found.")
        return None

    @property
    def num_empty_lines(self):
        return len(self.empty_lines)

    def get_num_chosen_lines(self):
        return len(self.chosen_lines)

    def get_empty_lines(self):
        return self.empty_lines

    def get_chosen_liens(self):
        return self.chosen_lines

    def get_chosen_lines(self):
        return self.chosen_lines

    def get_board_size(self):
        return self.board_size

    def draw_point(self, x, y):
        current_x = self.calculate_current_coordinate(x)
        current_y = self.calculate_current_coordinate(y)
        point = Point(current_x, current_y)
        c = Circle(point, 5)
        c.setFill(color_rgb(50, 50, 50))
        self.circles.append(c)
        return point

    def draw_vertical_line(self, x, y, point_a, point_b):
        if y < self.board_size and point_b.getY() >= point_a.getY():
            v_line = Line(point_a, point_b)
            v_line.setOutline(color_rgb(225, 225, 225))
            v_line.setWidth(self.LINE_WIDTH)
            v_line.draw(self.win)
            # Add to array of empty lines
            self.empty_lines.append(v_line)

    def draw_horizontal_line(self, x, y, point_a, point_b):
        if x < self.board_size - 1 and point_b.getX() >= point_a.getX():
            h_end = Point(self.calculate_current_coordinate(
                x + 1), point_b.getY())
            h_line = Line(point_b, h_end)
            h_line.setOutline(color_rgb(225, 225, 225))
            h_line.setWidth(self.LINE_WIDTH)
            h_line.draw(self.win)
            # Add to array of empty lines
            self.empty_lines.append(h_line)

    def create_board(self):
        self.win = GraphWin(
            "Dots and Walls", self.board_size * 60, self.board_size * 60)
        self.win.setBackground(color_rgb(255, 255, 255))
        point = Point(self.calculate_current_coordinate(0),
                      self.calculate_current_coordinate(0))
        prev_point = None
        for x in range(self.board_size):
            for y in range(self.board_size):
                prev_point = point
                point = self.draw_point(x, y)
                if prev_point:
                    self.draw_vertical_line(x, y, prev_point, point)
                    self.draw_horizontal_line(x, y, prev_point, point)

        # Draw circles on screen
        # (Keeps circle on top of lines by drawing at the end)
        for c in self.circles:
            c.draw(self.win)

        # self.print_empty_lines()
        return

    def update_board(self, clicked_line, player):
        # Update arrays
        self.chosen_lines.append(clicked_line)
        self.empty_lines.remove(clicked_line)

        # Print initial line counts
        print("# Empty lines:", self.num_empty_lines)
        chosen_line_count = self.get_num_chosen_lines()
        print("# Chosen lines", chosen_line_count)

        # Update screen
        line = Line(clicked_line.getP1(), clicked_line.getP2())
        line.setOutline(player.color_id)
        line.setWidth(self.LINE_WIDTH)
        line.draw(self.win)

        # print("\n")
        # self.print_chosen_lines()
        # print("\n")

        return

    def draw_square(self, point1, point2, player):
        square = Rectangle(point1, point2)
        square.setOutline(player.color_id)
        square.setFill(player.color_id)
        square.draw(self.win)

        # Now redraw circles on top (only for board sizes less than 6) for
        # better graphics
        if self.board_size < 6:
            for c in self.circles:
                c.undraw()
                c.draw(self.win)

    def calculate_current_coordinate(self, coordinate_point):
        return self.board_size * 10 + coordinate_point * 50

    def calculate_original_coordinate(self, graph_coordinate):
        return int((graph_coordinate - (self.board_size * 10)) / 50)


class Player:

    def __init__(self, player_id):
        self.score = 0
        self.player_id = player_id
        self.color_id = None
        self.set_color_id()

    def set_color_id(self):
        if self.player_id == 0:
            self.color_id = color_rgb(38, 181, 172)
        else:
            self.color_id = color_rgb(199, 69, 26)

    def get_player_id(self):
        return self.player_id

    def get_color_id(self):
        return self.color_id

    def get_score(self):
        return self.score

    def add_score(self, score_increment):
        self.score = self.score + score_increment


class Game:

    def __init__(self, board_size):
        self.board = Board(board_size)
        self.player1 = Player(0)
        self.player2 = Player(1)
        self.isValid = True
        self.start_game()

    def start_game(self):
        print("Let's begin!")

        active_player = self.player1
        # Begin game until all board lines chosen
        while self.board.num_empty_lines > 1:
            isSquare = self.play_turn(active_player)

            # If completed square, same player keeps next turn
            while isSquare:
                if self.board.num_empty_lines <= 1:
                    break
                isSquare = self.play_turn(active_player)

            # Switch players
            #
            # i'm a bit confuse about the need for the self.isValid
            # check here?  might be worth a comment somewhere
            # explaining what it means, or coming up with a clearer
            # name for it or way to do what it does.
            if active_player == self.player1 and self.isValid:
                active_player = self.player2
            elif active_player == self.player2 and self.isValid:
                active_player = self.player1

            score1 = self.player1.get_score()
            score2 = self.player2.get_score()
            #print("Player 1 score:", score1)
            #print("Player 2 score:", score2)

        if score1 > score2:
            print("\nPlayer 1 wins!")
        elif score1 < score2:
            print("\nPlayer 2 wins!")
        elif score1 == score2:
            print("\nIt's a tie!")
        else:
            print(
                "\nError: unable to determine winner. Cookie while we get this sorted out?")

    def play_turn(self, player):
        if player.get_player_id() == 0:
            print("\nPlayer 1: Click on an empty line.")
        elif player.get_player_id() == 1:
            print("\nPlayer 2: Click on an empty line.")

        click = self.board.win.getMouse()
        print("x, y:", click.getX(), click.getY())
        clicked_line = self.board.get_line_from_click(click)
        if clicked_line != None:
            self.isValid = self.check_chosen_lines(clicked_line)
            if self.isValid:
                print("This line has not been clicked. Proceed.")
                self.board.update_board(clicked_line, player)
                isSquare = self.check_complete_square(clicked_line, player)
                return isSquare
            else:
                print("Line has already been clicked.")
        else:
            print("Not a valid line.")
            self.isValid = False
        return False

    def check_chosen_lines(self, clicked_line):
        if clicked_line in self.board.get_chosen_lines():
            return False
        return True

    def check_complete_square(self, clicked_line, player):
        # this function is pretty gnarly and could probalby do with a
        # refactoring, similar to some of the functions in
        # `Board`. Pulling out identical / very similar pieces of code
        # into functions whose names capture what they do will
        # probably get you pretty far, try it out!
        isSquare = False

        # Grab original coordinate points for x, then
        # Recalculate to get next x/y neighbor
        this_x1 = clicked_line.getP1().getX()
        this_x2 = clicked_line.getP2().getX()
        orig_x1_coordinate = self.board.calculate_original_coordinate(this_x1)
        orig_x2_coordinate = self.board.calculate_original_coordinate(this_x2)

        #print("this_x1:", this_x1)
        #print("this_x2:", this_x2)

        #print("original_x1 coordinate:", orig_x1_coordinate)
        #print("original_x2 coordinate:", orig_x2_coordinate)
        print("\n")

        # Do same for y
        this_y1 = clicked_line.getP1().getY()
        this_y2 = clicked_line.getP2().getY()
        orig_y1_coordinate = self.board.calculate_original_coordinate(this_y1)
        orig_y2_coordinate = self.board.calculate_original_coordinate(this_y2)

        #print("this_y1:", this_y1)
        #print("this_y2:", this_y2)

        #print("original_y1 coordinate:", orig_y1_coordinate)
        #print("original_y2 coordinate:", orig_y2_coordinate)

        # If vertical line:
        if this_x1 == this_x2:
            #print("This is a VERTICAL line. Gathering neighbors...\n")

            # Left
            left_neighbor_x1 = self.board.calculate_current_coordinate(
                orig_x1_coordinate - 1)
            left_pt1 = Point(left_neighbor_x1, this_y1)
            left_pt2 = Point(left_neighbor_x1, this_y2)
            left = self.board.get_line(Line(left_pt1, left_pt2))
            #print("Left neighbor line start: ", left_neighbor_x1, this_y1, " | end: ", left_neighbor_x1, this_y2)

            # Right
            right_neighbor_x1 = self.board.calculate_current_coordinate(
                orig_x1_coordinate + 1)
            right_pt1 = Point(right_neighbor_x1, this_y1)
            right_pt2 = Point(right_neighbor_x1, this_y2)
            right = self.board.get_line(Line(right_pt1, right_pt2))
            #print("Right neighbor line start: ", right_neighbor_x1, this_y1, " | end: ", right_neighbor_x1, this_y2)

            # Top-left (a horizontal line)
            top_left_neighbor_x1 = self.board.calculate_current_coordinate(
                orig_x1_coordinate - 1)
            top_left_pt1 = Point(top_left_neighbor_x1, this_y1)
            top_left_pt2 = Point(this_x1, this_y1)
            top_left = self.board.get_line(Line(top_left_pt1, top_left_pt2))
            #print("Top-left neighbor line start: ", top_left_neighbor_x1, this_y1, " | end: ", this_x1, this_y1)

            # Top-right (a horizontal line)
            top_right_neighbor_x2 = self.board.calculate_current_coordinate(
                orig_x1_coordinate + 1)
            top_right_pt1 = Point(this_x1, this_y1)
            top_right_pt2 = Point(top_right_neighbor_x2, this_y1)
            top_right = self.board.get_line(Line(top_right_pt1, top_right_pt2))
            #print("Top-right neighbor line start: ", this_x1, this_y1, " | end: ", top_right_neighbor_x2, this_y1)

            # Bottom-left (a horizontal line)
            bottom_left_neighbor_x2 = self.board.calculate_current_coordinate(
                orig_x1_coordinate - 1)
            bottom_left_pt1 = Point(bottom_left_neighbor_x2, this_y2)
            bottom_left_pt2 = Point(this_x2, this_y2)
            bottom_left = self.board.get_line(
                Line(bottom_left_pt1, bottom_left_pt2))
            #print("Bottom-left neighbor line start: ", bottom_left_neighbor_x2, this_y2, " | end: ", this_x2, this_y2)

            # Bottom-right (a horizontal line)
            bottom_right_neighbor_x2 = self.board.calculate_current_coordinate(
                orig_x1_coordinate + 1)
            bottom_right_pt1 = Point(this_x2, this_y2)
            bottom_right_pt2 = Point(bottom_right_neighbor_x2, this_y2)
            bottom_right = self.board.get_line(
                Line(bottom_right_pt1, bottom_right_pt2))
            #print("Bottom-right neighbor line start: ", this_x2, this_y2, " | end: ", bottom_right_neighbor_x2, this_y2)

            # print("\nThe following are lines already in chosen_lines:")
            # if right in self.board.chosen_lines:
            # 	print("Vertical right")
            # if left in self.board.chosen_lines:
            # 	print("Vertical left")
            # if top_right in self.board.chosen_lines:
            # 	print("Horizontal top right")
            # if top_left in self.board.chosen_lines:
            # 	print("Horizontal top left")
            # if bottom_right in self.board.chosen_lines:
            # 	print("Horizontal bottom right")
            # if bottom_left in self.board.chosen_lines:
            # 	print("Horizontal bottom left")

            # Check for completed squares
            if right in self.board.chosen_lines and top_right in self.board.chosen_lines and bottom_right in self.board.chosen_lines:
                self.board.draw_square(
                    clicked_line.getP1(), right.getP2(), player)
                player.add_score(10)
                print("10 points for Hufflepuff!")
                isSquare = True
            if left in self.board.chosen_lines and top_left in self.board.chosen_lines and bottom_left in self.board.chosen_lines:
                self.board.draw_square(
                    left.getP1(), clicked_line.getP2(), player)
                player.add_score(10)
                print("10 points for Hufflepuff!")
                isSquare = True

        # Horizontal lines
        elif this_y1 == this_y2:
            #print("This is a HORIZONTAL line. Gathering neighbors...\n")

            # Top
            top_neighbor_y1 = self.board.calculate_current_coordinate(
                orig_y1_coordinate - 1)
            top_pt1 = Point(this_x1, top_neighbor_y1)
            top_pt2 = Point(this_x2, top_neighbor_y1)
            top = self.board.get_line(Line(top_pt1, top_pt2))
            #print("Top neighbor line start: ", this_x1, top_neighbor_y1, " | end: ", this_x2, top_neighbor_y1)

            # Bottom
            bottom_neighbor_y1 = self.board.calculate_current_coordinate(
                orig_y1_coordinate + 1)
            bottom_pt1 = Point(this_x1, bottom_neighbor_y1)
            bottom_pt2 = Point(this_x2, bottom_neighbor_y1)
            bottom = self.board.get_line(Line(bottom_pt1, bottom_pt2))
            #print("Bottom neighbor line start: ", this_x1, bottom_neighbor_y1, " | end: ", this_x2, bottom_neighbor_y1)

            # Top-left (a vertical line)
            top_left_neighbor_y1 = self.board.calculate_current_coordinate(
                orig_y1_coordinate - 1)
            top_left_pt1 = Point(this_x1, top_left_neighbor_y1)
            top_left_pt2 = Point(this_x1, this_y1)
            top_left = self.board.get_line(Line(top_left_pt1, top_left_pt2))
            #print("Top-left neighbor line start: ", this_x1, top_left_neighbor_y1, " | end: ", this_x1, this_y1)

            # Top-right (a vertical line)
            top_right_neighbor_y1 = self.board.calculate_current_coordinate(
                orig_y1_coordinate - 1)
            top_right_pt1 = Point(this_x2, top_right_neighbor_y1)
            top_right_pt2 = Point(this_x2, this_y1)
            top_right = self.board.get_line(Line(top_right_pt1, top_right_pt2))
            #print("Top-right neighbor line start: ", this_x2, top_right_neighbor_y1, " | end: ", this_x2, this_y1)

            # Bottom-left (a vertical line)
            bottom_left_neighbor_y2 = self.board.calculate_current_coordinate(
                orig_y1_coordinate + 1)
            bottom_left_pt1 = Point(this_x1, this_y1)
            bottom_left_pt2 = Point(this_x1, bottom_left_neighbor_y2)
            bottom_left = self.board.get_line(
                Line(bottom_left_pt1, bottom_left_pt2))
            #print("Bottom-left neighbor line start: ", this_x1, this_y1, " | end: ", this_x1, bottom_left_neighbor_y2)

            # Bottom-right (a vertical line)
            bottom_right_neighbor_y2 = self.board.calculate_current_coordinate(
                orig_y1_coordinate + 1)
            bottom_right_pt1 = Point(this_x2, this_y2)
            bottom_right_pt2 = Point(this_x2, bottom_right_neighbor_y2)
            bottom_right = self.board.get_line(
                Line(bottom_right_pt1, bottom_right_pt2))
            #print("Bottom-right neighbor line start: ", this_x2, this_y2, " | end: ", this_x2, bottom_right_neighbor_y2)

            # print("\nThe following are lines already in chosen_lines:")
            # if top in self.board.chosen_lines:
            # 	print("Horizontal top")
            # if bottom in self.board.chosen_lines:
            # 	print("Horizontal bottom")
            # if top_right in self.board.chosen_lines:
            # 	print("Vertical top right")
            # if top_left in self.board.chosen_lines:
            # 	print("Vertical top left")
            # if bottom_right in self.board.chosen_lines:
            # 	print("Vertical bottom right")
            # if bottom_left in self.board.chosen_lines:
            # 	print("Vertical bottom left")

            # Check for complete square
            if top in self.board.chosen_lines and top_right in self.board.chosen_lines and top_left in self.board.chosen_lines:
                self.board.draw_square(
                    top.getP1(), clicked_line.getP2(), player)
                player.add_score(10)
                print("10 points for Hufflepuff!")
                isSquare = True
            if bottom in self.board.chosen_lines and bottom_right in self.board.chosen_lines and bottom_left in self.board.chosen_lines:
                self.board.draw_square(
                    clicked_line.getP1(), bottom.getP2(), player)
                player.add_score(10)
                print("10 points for Hufflepuff!")
                isSquare = True

        return isSquare


def main():
    board_size = input("Enter board size (between 3-10):")
    while (int(board_size) <= 2) or (int(board_size) >= 10) or int(board_size) == None:
        print("Invalid number. Try again, or press 'q' to quit game.")
        board_size = input("Enter board size (between 2-10):")
        if board_size == 'q':
            exit()
    game = Game(int(board_size))

if __name__ == '__main__':
    main()
