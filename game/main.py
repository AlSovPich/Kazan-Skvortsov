import pygame
import random


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        self.chosen = 0
        self.colors = [[255, 0, 0], [0, 255, 255], [255, 0, 255], [0, 255, 0], [255, 255, 0], [0, 0, 255]]
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append(random.choice(self.colors))
            for l in range(self.width):
                while self.elim_matches() != 0:
                    pass

        # значения по умолчанию
        self.x = 10
        self.y = 10
        self.cell_size = 70

    def render(self, screen):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                x1 = row * self.cell_size + self.x
                y1 = col * self.cell_size + self.y
                color = self.board[row][col]
                pygame.draw.rect(screen, color, (x1, y1, self.cell_size, self.cell_size), 0)
                pygame.draw.rect(screen, (0, 0, 0), (x1, y1, self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        print(mouse_pos)
        x = (mouse_pos[0] - self.x) // self.cell_size
        y = (mouse_pos[1] - self.y) // self.cell_size
        if x >= self.width or y >= self.height:
            return None
        return (x,y)

    def get_click(self, mouse_pos):
        print("Get click " + str(mouse_pos))
        cell_coords = self.get_cell(mouse_pos)
        print("coords: " + str(cell_coords))

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.x = left
        self.y = top
        self.cell_size = cell_size

    def move(self, fromm, to):
        change = self.board[fromm[0]][fromm[1]]
        self.board[fromm[0]][fromm[1]] = self.board[to[0]][to[1]]
        self.board[to[0]][to[1]] = change

    def adjanced(self, fromm, to):
        if abs(fromm[0] - to[0]) == 1:
            return True

        elif abs(fromm[1] - to[1]):
            return True

        return False

    def elim_matches(self):
        elim_list = []
        for y in range(len(self.board)):
            streak = 1
            for x in range(1, len(self.board[y])):
                if self.board[y][x] == self.board[y][x - 1] and self.board[y][x] != [255, 255, 255]:
                    streak += 1
                else:
                    streak = 1
                if streak == 3:
                    elim_list += [[y, x - 2]]
                    elim_list += [[y, x - 1]]
                    elim_list += [[y, x]]
                elif streak > 3:
                    elim_list += [[y, x]]
        for x in range(len(self.board[0])):
            streak = 1
            for y in range(1, len(self.board)):
                if self.board[y][x] == self.board[y - 1][x] and self.board[y][x] != [255, 255, 255]:
                    streak += 1
                else:
                    streak = 1
                if streak == 3:
                    elim_list += [[y - 2, x]]
                    elim_list += [[y - 1, x]]
                    elim_list += [[y, x]]
                elif streak > 3:
                    elim_list += [[y, x]]

        for i in range(len(elim_list)):
            y = elim_list[i][0]
            x = elim_list[i][1]
            self.board[y][x] = [255, 255, 255]
        self.refill_columns()
        return len(elim_list)


    def refill_columns(self):
        for column in range(len(self.board)):
            for row in range(len(self.board)):
                if self.board[row][column] == [255, 255, 255]:
                    test = 0
                    length = 0
                    while row + test < len(self.board):
                        if self.board[row + test][column] == [255, 255, 255]:
                            length += 1
                            test += 1
                            if row + test >= len(self.board):
                                break
                        else:
                            break

                    for blankRow in range(row, len(self.board)):
                        try:
                            self.board[blankRow][column] = self.board[blankRow + length][column]
                        except:
                            self.board[blankRow][column] = random.choice(self.colors)


if __name__ == '__main__':
    pygame.init()
    # размеры окна:
    size = width, height = 580, 580
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    bd = Board(8, 8)
    running = True
    fromm = False
    rounds = 20
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or rounds == 0:
                if rounds == 0:
                    print("Time exceeded")
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not fromm:
                    fromm = bd.get_cell(event.pos)
                else:
                    to = bd.get_cell(event.pos)
                    if bd.adjanced(fromm, to):
                        bd.move(fromm, to)
                        if bd.elim_matches() == 0:
                            bd.move(fromm, to)
                        else:
                            while bd.elim_matches() != 0:
                                pass
                            rounds -= 1
                    fromm, to = False, False
        screen.fill((0, 0, 0))
        bd.render(screen)
        pygame.display.flip()

    pygame.quit()