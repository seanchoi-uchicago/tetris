import player
import visual
import random
import pygame
#https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/

from adversary import RandomAdversary
from arguments import parser
from board import Board, Direction, Rotation, Action, Shape
from constants import BOARD_WIDTH, BOARD_HEIGHT, DEFAULT_SEED, INTERVAL, \
    BLOCK_LIMIT
from exceptions import BlockLimitException
from player import Player, SelectedPlayer

BLACK = (0, 0, 0)
GREY = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CELL_WIDTH = 20
CELL_HEIGHT = 20

EVENT_FORCE_DOWN = pygame.USEREVENT + 1
FRAMES_PER_SECOND = 60


class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y, shape):
        super().__init__()

        self.image = pygame.Surface([CELL_WIDTH, CELL_HEIGHT])
        if shape is Shape.B:
            pygame.draw.circle(self.image, WHITE, [CELL_WIDTH//2, CELL_HEIGHT//2],
                               CELL_WIDTH/2)
        else:
            self.image.fill(color)
            pygame.draw.rect(self.image, WHITE, [0, 0, CELL_WIDTH, CELL_HEIGHT], width=1)

        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_WIDTH
        self.rect.y = y * CELL_HEIGHT

class Discard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([CELL_WIDTH, CELL_HEIGHT])
        pygame.draw.line(self.image, RED, (0, 0), (CELL_WIDTH, CELL_HEIGHT), width=3)
        pygame.draw.line(self.image, RED, (0, CELL_HEIGHT), (CELL_WIDTH, 0), width=3)

        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_WIDTH
        self.rect.y = y * CELL_HEIGHT

txt = []
def init_text(screen):
    global txt, scorefont
    font = pygame.font.SysFont(None, 24)
    img = font.render('SCORE', True, WHITE)
    txt.append((img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, 0)))
    img = font.render('NEXT', True, WHITE)
    txt.append((img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, CELL_HEIGHT*3)))
    img = font.render('BOMBS', True, WHITE)
    txt.append((img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, CELL_HEIGHT*9)))
    img = font.render('DISCARDS', True, WHITE)
    txt.append((img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, CELL_HEIGHT*12)))

    scorefont = pygame.font.Font("Segment7-4Gml.otf", 40)

def render(screen, board):
    global scorefont, txt
    screen.fill(BLACK)
    for t,pos in txt:
        screen.blit(t, pos)    

    for i in range(0,10,2):
        pygame.draw.rect(screen, GREY,
                         [i * CELL_WIDTH, 0,
                          CELL_WIDTH, board.height * CELL_HEIGHT])

    img = scorefont.render(str(board.score), True, WHITE)
    screen.blit(img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, CELL_HEIGHT))

    sprites = pygame.sprite.Group()

    # Add the cells already on the board for drawing.
    for (x, y) in board:
        sprites.add(Block(pygame.Color(board.cellcolor[x, y]), x, y, Shape.O))

    if board.falling is not None:
        # Add the cells of the falling block for drawing.
        for (x, y) in board.falling:
            sprites.add(Block(pygame.Color(board.falling.color), x, y, board.falling.shape))

    if board.next is not None:
        # Add the cells of the next block for drawing.
        width = board.next.right - board.next.left
        for (x, y) in board.next:
            sprites.add(
                Block(pygame.Color(board.next.color),
                      x + board.width + 2.5 - width/2, y+4,
                      board.next.shape))

    for i in range(board.bombs_remaining):
        sprites.add(Block(pygame.Color(WHITE),board.width + 0.4 + i*1.1,10, Shape.B))

    for i in range(board.discards_remaining):
        sprites.add(Discard(board.width + 0.4 + (i%5)*1.1,13+(i//5)*1.1))
        
    sprites.draw(screen)

    pygame.draw.line(
        screen,
        BLUE,
        (board.width * CELL_WIDTH + 2, 0),
        (board.width * CELL_WIDTH + 2, board.height * CELL_HEIGHT)
    )

    # Update window title with score.
    pygame.display.set_caption(f'Score: {board.score}')


class UserPlayer(Player):
    """
    A simple user player that reads moves from the command line.
    """

    key_to_move = {
        pygame.K_RIGHT: Direction.Right,
        pygame.K_LEFT: Direction.Left,
        pygame.K_DOWN: Direction.Down,
        pygame.K_SPACE: Direction.Drop,
        pygame.K_UP: Rotation.Clockwise,
        pygame.K_z: Rotation.Anticlockwise,
        pygame.K_x: Rotation.Clockwise,
        pygame.K_b: Action.Bomb,
        pygame.K_d: Action.Discard
    }

    def choose_action(self, board):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYUP:
                if event.key in self.key_to_move:
                    return self.key_to_move[event.key]
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    raise SystemExit
            elif event.type == EVENT_FORCE_DOWN:
                return None


def check_stop():
    for event in pygame.event.get():
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            raise SystemExit
        elif event.type == pygame.QUIT:
            raise SystemExit


def run(sp, seed):
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
    adversary = RandomAdversary(seed, BLOCK_LIMIT)

    args = parser.parse_args()
    if args.manual:
        player = UserPlayer()
    else:
        player = sp
        player.print_heuristics()


    pygame.init()

    screen = pygame.display.set_mode([
        (BOARD_WIDTH + 6) * CELL_WIDTH,
        BOARD_HEIGHT * CELL_HEIGHT
    ])

    clock = pygame.time.Clock()

    init_text(screen)

    # Set timer to force block down when no input is given.
    pygame.time.set_timer(EVENT_FORCE_DOWN, INTERVAL)

    try:
        for move in board.run(player, adversary):
            render(screen, board)
            pygame.display.flip()

            # If we are not playing manually, clear the events.
            if not args.manual:
                check_stop()

                clock.tick(FRAMES_PER_SECOND)

        print("Score=", board.score)
        # player.print_heuristics()
        # print("Press ESC in game window to exit")
    except BlockLimitException:
        print("Out of blocks")
        print("Score=", board.score)
        # player.print_heuristics()
        # print("Press ESC in game window to exit")
        
    return board.score


#create a population of random bitstrings
def createPopulation(size):
    arr = []
    for p in range(size):
# h2=-2.965633983462173, h3=-0.28978194948487046, h4= 0.07361043379142615, h5=-3.15881315537020405087,
# h1=-0.1, h2= -2.9, h3=-0.38, h4=0.07, h5=-3.9, h6=-0.08
        cp = player.CustomPlayer(-0.1 * random.uniform(0.95, 1.05), -2.9 * random.uniform(0.95, 1.05), -0.38 * random.uniform(0.95, 1.01), 0.07 * random.uniform(0.95, 1.05), -3.9 * random.uniform(0.95, 1.05), -0.08 * random.uniform(0.95, 1.05));
        # cp = player.CustomPlayer()
        # cp.print_heuristics()
        arr.append(cp)

    print(arr)
    return arr


#get a score for any given child
#refactor for legit use
def getScore(child_player, seed):
    
    score = run(child_player, seed)
    return score

#choose best parent out of k possible parents
def selection(population, scoreList, k):

    index = random.randint(0, len(population) - 1)
    
    for a in range(k):
        newIndex = random.randint(0, len(population) - 1)
        #smaller score is more desirable - subject to change
        if (scoreList[newIndex] < scoreList[index]):
            index = newIndex

    return population[index]


def breed(parent1, parent2, pCross):
    child1 = parent1
    child2 = parent2

    if (random.random() < pCross):
        #choose point not at the end of list
      child1.set_height_heuristic(parent2.get_height_heuristic() + random.uniform(-0.01, 0.01))
      child2.set_height_heuristic(parent1.get_height_heuristic() + random.uniform(-0.01, 0.01))
    
    if (random.random() < pCross):

      child1.set_holes_heuristic(parent2.get_holes_heuristic() + random.uniform(-0.01, 0.01))
      child2.set_holes_heuristic(parent1.get_holes_heuristic() + random.uniform(-0.01, 0.01))

    if (random.random() < pCross):

      child1.set_smoothness_heuristic(parent2.get_smoothness_heuristic() + random.uniform(-0.01, 0.01))
      child2.set_smoothness_heuristic(parent1.get_smoothness_heuristic() + random.uniform(-0.01, 0.01))

    if (random.random() < pCross): 
        
      child1.set_bad_lines_heuristic(parent2.get_bad_lines_heuristic() + random.uniform(-0.01, 0.01))
      child2.set_bad_lines_heuristic(parent1.get_bad_lines_heuristic() + random.uniform(-0.01, 0.01))

    if (random.random() < pCross):

      child1.set_fourth_line_heuristic(parent2.get_fourth_line_heuristic() + random.uniform(-0.01, 0.01))
      child2.set_fourth_line_heuristic(parent1.get_fourth_line_heuristic() + random.uniform(-0.01, 0.01))


    if (random.random() < pCross):

      child1.set_right_column_height_heuristic(parent2.get_right_column_height_heuristic() + random.uniform(-0.01, 0.01))
      child2.set_right_column_height_heuristic(parent1.get_right_column_height_heuristic() + random.uniform(-0.01, 0.01))

    # if (random.random() < pCross):

    #   child1.set_trenches_heuristic(parent2.get_trenches_heuristic() + random.uniform(-0.01, 0.01))
    #   child2.set_trenches_heuristic(parent1.get_trenches_heuristic() + random.uniform(-0.01, 0.01))

    return [child1, child2]

def mutate_weight(input, pMutation):
    if (random.random() < pMutation):
        return input + random.uniform(-0.01, 0.01)
    return input

#some cool machine learning stuff different from what I've done before
#iterations:
#popSize
#k: number of comparisons in selection function

def geneticAlgorithm(iterations, popSize, k, pMutation, pCross):
    
    population = createPopulation(popSize)

    bestIndex = 0
    bestScore = 0

    for generation in range(iterations):
        scores = []
        seed = random.randint(0, 1000)
        for parent in population:
            tempScore = getScore(parent, seed)
            scores.append(tempScore)

            if (tempScore > bestScore):
                bestIndex = scores.index(tempScore)
                bestScore = tempScore
        print(scores)

        parents = []
        for parent in population:

            parents.append(selection(population, scores, k))
        

        children = []
        for i in range(0, popSize, 2):
            tempChildList = breed(parents[i], parents[i + 1], pCross)
            for child in tempChildList:
                
                height = mutate_weight(child.get_height_heuristic(), pMutation)
                holes = mutate_weight(child.get_holes_heuristic(), pMutation)
                smoothness = mutate_weight(child.get_smoothness_heuristic(), pMutation)
                fourth_line = abs(mutate_weight(child.get_fourth_line_heuristic(), pMutation))
                bad_lines = mutate_weight(child.get_bad_lines_heuristic(), pMutation)
                right_column_height = mutate_weight(child.get_right_column_height_heuristic(), pMutation)
                # trench = mutate_weight(child.get_trenches_heuristic(), pMutation)

                child = player.CustomPlayer(height, holes, smoothness, fourth_line, bad_lines, right_column_height)
                children.append(child)


        print("\nbest score for generation " + str(generation) + ": " + str(bestScore))
        parents[bestIndex].print_heuristics()
        print("\n")

        population = children
        bestScore = 0

    return bestScore


# pop = createPopulation(10)
# getScore(pop[0])
geneticAlgorithm(100, 20, 2, 0.1, 0.1)

