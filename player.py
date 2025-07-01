from board import Direction, Rotation, Action, Shape
from random import Random
import time
import random


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
              
    def choose_action(self, board):
        self.print_board(board)
        time.sleep(0.5)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])


# height_heuristic:  -0.10257716479597982
# holes_heuristic:  -3.0651561335142046
# smoothness_heuristic:  -0.28978194948487046
# complete_lines_heuristic:  0.07361043379142615
# right_column_height_heuristic:  -0.0031315537020405087

# 52241
# height_heuristic:  -0.09789382383733526
# holes_heuristic:  -3.069383910252422
# smoothness_heuristic:  -0.29930391189001637
# fourth_line_heuristic:  0.07786318053753641
# bad_lines_heuristic:  -3.263746840219707

#new ones

# height:  -0.10321922110407288 holes:  -2.9835072705641634 smoothness:  -0.28093611183764805 fourth_line:  0.07246921446121234 bad_lines:  -3.2906873184324814


#high score (55813)
# height:  -0.09789803631530343 holes:  -3.049741170914307 smoothness:  -0.27701118715929096 fourth_line:  0.07049651091365529 bad_lines:  -3.1019403345563314

# height:  -0.09948284122613539 holes:  -2.9308686108846707 smoothness:  -0.2829227486955199 fourth_line:  0.0657277972946419 bad_lines:  -3.1466950232933724 right_column_height_heuristic:  -0.18604911162025584

# height:  -0.11141541264125474 holes:  -2.9203423433050473 smoothness:  -0.28248882441129985 fourth_line:  0.0671757669410414 bad_lines:  -3.154147189139492 right_column_height_heuristic:  -0.18604911162025584

# height:  -0.09705389852653028 holes:  -2.9427245669128848 smoothness:  -0.2915077273630645 fourth_line:  0.0740057366646071 bad_lines:  -3.143044868058973 right_column_height_heuristic:  -0.18406219681726044

# height:  -0.10124220207003434 holes:  -2.7790431272416494 smoothness:  -0.37821473032836367 fourth_line:  0.071758488165273 bad_lines:  -3.965725372752254

class CustomPlayer(Player):
  def __init__(self, h1= -0.10321922110407288, h2=-2.9835072705641634, h3=-0.28093611183764805, h4= 0.07246921446121234, h5=-3.2906873184324814, h6=-0.18190404782225794):

    self.height_heuristic = h1
    self.holes_heuristic = h2
    self.smoothness_heuristic = h3
    self.fourth_line_heuristic = h4
    self.bad_lines_heuristic = h5
    self.right_column_height_heuristic = 0
    # self.empty_columns_heuristic = 0
    # self.trenches_heuristic = 0
  

    # self.height_heuristic = random.random()
    # self.holes_heuristic = random.random()
    # self.smoothness_heuristic = random.random()
    # self.complete_lines_heuristic = random.random()
    # self.right_column_height_heuristic = random.random()
    # self.left_column_height_heuristic = 0
    # self.trenches_heuristic = random.random()

    
  def set_height_heuristic(self, height):
    self.height_heuristic = -1 * abs(height)
  
  def set_holes_heuristic(self, holes):
    self.holes_heuristic = -1 * abs(holes)
  
  def set_smoothness_heuristic(self, smoothness_heuristic):
    self.smoothness_heuristic = -1 * abs(smoothness_heuristic)

  def set_bad_lines_heuristic(self, bad_lines_heuristic):
    self.complete_lines_heuristic = -1 * abs(bad_lines_heuristic)

  def set_right_column_height_heuristic(self, right_column_height_heuristic):
    self.right_column_height_heuristic = -1 * abs(right_column_height_heuristic)

  def set_trenches_heuristic(self, trenches_heuristic):
    self.trenches_heuristic = -1 * abs(trenches_heuristic)

  def set_fourth_line_heuristic(self, fourth_line_heuristic):
    self.fourth_line_heuristic = fourth_line_heuristic

  def get_trenches_heuristic(self):
    return self.trenches_heuristic

  def get_height_heuristic(self):
    return self.height_heuristic

  def get_holes_heuristic(self):
    return self.holes_heuristic

  def get_smoothness_heuristic(self):
    return self.smoothness_heuristic

  def get_fourth_line_heuristic(self):
    return self.fourth_line_heuristic

  def get_right_column_height_heuristic(self):
    return self.right_column_height_heuristic

  def get_bad_lines_heuristic(self):
    return self.bad_lines_heuristic
  
  def set_heuristics(self, height, holes, smoothness, fourth_line_cleared, bad_lines_cleared, right_column_height):
    self.height_heuristic = height
    self.holes_heuristic = holes
    self.smoothness_heuristic = smoothness
    self.fourth_line_heuristic = fourth_line_cleared
    self.bad_lines_heuristic = bad_lines_cleared
    self.right_column_height_heuristic = right_column_height
   
    # self.right_column_height_heuristic = right_column_height

  def print_heuristics(self):
    print("height: ", self.height_heuristic, "holes: ", self.holes_heuristic, "smoothness: ", self.smoothness_heuristic, "fourth_line: ", self.fourth_line_heuristic, "bad_lines: ", self.bad_lines_heuristic, "right_column_height_heuristic: ", self.right_column_height_heuristic)
    # print("trenches_heuristic: ", self.trenches_heuristic)

  def print_board(self, new_board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in new_board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)

  # move the block to any desired position and rotation
  def move_block(self, board, x, rotation):

    move_list = []

    if self.get_max_height(board) > 19 and board.bombs_remaining > 0:
      move_list.append(Action.Bomb)
      move_list.append(Direction.Drop)
      return move_list
    for k in range(rotation):
      if not board.next:
        break
      board.rotate(Rotation.Clockwise);
      move_list.append(Rotation.Clockwise)
    if (board.next and x > board.falling.left):
      for i in range(x - board.falling.left):
        if not board.falling:
          break
        board.move(Direction.Right)
        move_list.append(Direction.Right)
    elif (board.next):
      for i in range(board.falling.left - x):
        if not board.next:
          break
        board.move(Direction.Left);
        move_list.append(Direction.Left)
    # while (board.next):
    #   board.move(Direction.Down)
    #   move_list.append(Direction.Down)
    if (board.next):
      board.move(Direction.Drop)
      move_list.append(Direction.Drop)

    return move_list

  #create a list of all potential next boards
  def create_all_potential_boards(self, board):
    
    potential_boards = []

    r = 4
    if (board.falling):
      if (board.falling.shape == Shape.O):
        r = 1
      elif (board.falling.shape == Shape.I or board.falling.shape == Shape.S or board.falling.shape == Shape.Z):
        r = 2


    for rotation in range(r):
      for x in range(10):

        new_board = board.clone()
        move_list = self.move_block(new_board, x, rotation) 
        potential_boards.append([new_board, move_list])

        # self.print_board(new_board)
        # time.sleep(0.1)

    return potential_boards


  def move_block_2(self, board, x, rotation):

    move_list = []

    if self.get_max_height(board) > 19 and board.bombs_remaining > 0:
      move_list.append(Action.Bomb)
      move_list.append(Direction.Drop)
      return move_list

    for k in range(rotation):
      if not board.falling:
        break
      board.rotate(Rotation.Clockwise);
      move_list.append(Rotation.Clockwise)

    if (board.falling and x > board.falling.left):
      for i in range(x - board.falling.left):
        if not board.falling:
          break
        board.move(Direction.Right)
        move_list.append(Direction.Right)
    elif (board.falling):
      for i in range(board.falling.left - x):
        if not board.falling:
          break
        board.move(Direction.Left);
        move_list.append(Direction.Left)

    # while (board.falling):
    #   board.move(Direction.Down)
    #   move_list.append(Direction.Down)

    if (board.falling):
      board.move(Direction.Drop)
      move_list.append(Direction.Drop)

    return move_list

  def create_all_potential_subboards(self, test_board):
    
    potential_boards_2 = []
    
    r = 4
    if (test_board.falling):
      if (test_board.falling.shape == Shape.O):
        r = 1
      elif (test_board.falling.shape == Shape.I or test_board.falling.shape == Shape.S or test_board.falling.shape == Shape.Z):
        r = 2
    
    for rotation in range(r):
      for x in range(10):
        new_board_2 = test_board.clone()
        move_list = self.move_block_2(new_board_2, x, rotation) 
        potential_boards_2.append([new_board_2, move_list])
        # self.print_board(new_board_2)
        # time.sleep(0.1)

    return potential_boards_2

  #get col height
  def get_col_height(self, board, col):
    height = 0
    for y in range(24):
      if (col,y) in board.cells:
        height += 1

    return height

  #get the maximum column height
  def get_max_height(self, board):
    max_height = 0
    for x in range(10):
      height = self.get_col_height(board, x)
      if (height > max_height):
        max_height = height

    return max_height

  #calculate sum of all column heights
  def aggregate_height(self, board):
    aggregate_height = 0
    for x in range(10):
      aggregate_height += self.get_col_height(board, x)
    return aggregate_height

  #count the number of holes in the board
  def count_holes(self, board):
    holes = 0
    for x in range(10):
      above = False
      for y in range(24):
        if (x,y) in board.cells:
          above = True
        if above and (x,y) not in board.cells:
          holes += 1

    return holes

  #cells left of a column where the topmost cell is at the same height or above the empty cell
  def count_left_trenches(self, board):
    holes = 0
    for x in range(9):
      if (self.get_col_height(board, x) < self.get_col_height(board, x + 1)):
        for y in range(self.get_col_height(board, x), self.get_col_height(board, x + 1)):
          if (x, y + 1) in board.cells:
            break
          if (x, y) not in board.cells:
            holes += 1
    
    return holes

  def count_right_trenches(self, board):
    holes = 0
    for x in reversed(range(9)):
      if (self.get_col_height(board, x + 1) < self.get_col_height(board, x)):
        for y in range(self.get_col_height(board, x + 1), self.get_col_height(board, x)):
          if (x, y + 1) in board.cells:
            break
          if (x, y) not in board.cells:
            holes += 1
  
    return holes

  #calculate the smoothness of the board
  def smoothness(self, board):
    smoothness = 0
    for x in range(9):
      smoothness += abs(self.get_col_height(board, x) - self.get_col_height(board, x+1))

    return smoothness


  def get_max_column_height_difference(self, board):
    max_height_dif = 0
    for x in range(9):
      height = abs(self.get_col_height(board, x) - self.get_col_height(board, x+1))
      if (height > max_height_dif):
        max_height_dif = height

    return max_height_dif

  #count the number of lines cleared by this piece
  def is_fourth_line_cleared(self, true_board, test_board):

    cell_change = len(test_board.cells) - len(true_board.cells)
    if (cell_change == 4):
      return 0
    elif (cell_change == -36):
      return 4
    else:
      return 0

  def count_bad_lines_cleared(self, true_board, test_board):
    cell_change = len(test_board.cells) - len(true_board.cells)
    if (cell_change == 4):
      return 0
    elif (cell_change == -6):
      return 1
    elif (cell_change == -16):
      return 2
    elif (cell_change == -26):
      return 3
    else:
      return 0

  def count_empty_columns(self, board):
    result = 0
    for x in range(9):
      height_dif = abs(self.get_col_height(board, x) - self.get_col_height(board, x+1))
      if (height_dif > 5):
        result += 1

    return result - 1

  def right_column_height(self, board):
    return self.get_col_height(board, 9)

  def left_column_height(self, board):
    return self.get_col_height(board, 0)

  #score the desirability of the next board
  def score_board(self, board, true_board):

      
    score = self.smoothness_heuristic * self.smoothness(board[0]) + self.height_heuristic * self.aggregate_height(board[0]) + self.holes_heuristic * self.count_holes(board[0]) + self.bad_lines_heuristic * self.count_bad_lines_cleared(true_board, board[0]) + self.fourth_line_heuristic * self.is_fourth_line_cleared(true_board, board[0]) + self.right_column_height_heuristic * self.right_column_height(board[0])
    # + self.empty_columns_heuristic * self.count_empty_columns(board[0])
    # + self.complete_lines_heuristic * self.count_lines_cleared(true_board, board[0])
    # + self.trenches_heuristic * (self.count_left_trenches(board[0]) + self.count_right_trenches(board[0]))

    return score

  #best score is highest
  def find_best_board(self, test_boards, true_board):
    
    best_board = test_boards[0]
    move_2 = self.find_best_move_2(best_board[0])
    move_2_score = self.score_board(move_2, best_board[0])
    best_score = self.score_board(best_board, true_board) + move_2_score
    
    for i in range(1, len(test_boards)):
      
      current_score = self.score_board(test_boards[i], true_board)
      board_2 = self.find_best_move_2(test_boards[i][0])
      board_2_score = self.score_board(board_2, test_boards[i][0])
      total_score = current_score + board_2_score
        
      if (total_score > best_score):
        best_board = test_boards[i]
        best_score = total_score

    change_in_holes = self.count_holes(best_board[0]) - self.count_holes(true_board)
    if (change_in_holes > 0 and true_board.discards_remaining):
      return [None, Action.Discard] 

    return best_board

  def find_best_move_2(self, test_board):

    test_boards_2 = self.create_all_potential_subboards(test_board)
    result = test_boards_2[0]

    for board_2 in test_boards_2:
      current_score = self.score_board(board_2, test_board)
      if (current_score > self.score_board(result, test_board)):
        result = board_2
    
    return result

  def choose_action(self, board):

    potential_boards = self.create_all_potential_boards(board)    
    chosen_board = self.find_best_board(potential_boards, board)

    #print(chosen_board[0])

    return chosen_board[1]
      

SelectedPlayer = CustomPlayer


#heuristics: penalize high blocks, penalize holes, reward line clears, prefer smooth board
#measure score: fitness value, survival time, score
#eliminate bottom 50%

#17426 is passing score (70%)