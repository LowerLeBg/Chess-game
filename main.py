import pygame
from piece import *
import copy

def print_board () :
    """
    this function just print the grid (white and black square)
    """    
    
    axis_value = [0,75,150,225,300,375,450,525] #those value are the limit of each square in x and y axis
    color_value = 0 #this value is need to set a variable color
    for y in axis_value :
        for x in axis_value :
            if color_value == 0 :
                pygame.draw.rect(screen,"white",[x,y,75,75]) #75,75 is the height and length of each square
                if x != 525 :# at the last rectangle we are not changing the color because otherwise it wouldnt be a real chess board
                    color_value = 1
            elif color_value== 1 :
                pygame.draw.rect(screen,"black",[x,y,75,75]) #75,75 is the height and length of each square
                if x != 525:
                    color_value = 0# at the last rectangle we are not changing the color because otherwise it wouldnt be a real chess board

def where_am_i (mouse_pos:list):
    """
    we are transforming the mouse_pos in a place in our grid who is readable

    Args:
        mouse_pos (list): our mouse position [x,y]

    Returns:
        list: the position of our mouse in the grid
    """    
    
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    x = -1
    y= -1
    while mouse_x >= 0:
        x += 1
        mouse_x -= 75
    while mouse_y >= 0 : 
        y += 1
        mouse_y -= 75
    return [y,x]

def print_piece (grid:list) :
    """
    this function is adding the piece on the board
    Args:
        grid (list): it's the list who contain all our piece
    """    
    
    axis_value = [0,75,150,225,300,375,450,525]#those value are the limit of each square in x and y axis
    for row in grid:
        for piece in row :
            if piece != None:
                piece_surf = piece.sprite.get_rect(center = (axis_value[piece.position[1]]+37.5,axis_value[piece.position[0]]+37.5)) # 37.5 is the half of 37.5 by using this value we are placing our piece in the middle of each square
                screen.blit(piece.sprite,piece_surf)

def display_possibility (movement_list:list) :
    """
    this grid show the movement possible if you click on a piece

    Args:
        movement_list (list): _description_
    """    
    axis_value = [0,75,150,225,300,375,450,525]
    for move in movement_list :
        pygame.draw.rect(screen,"yellow",[axis_value[move[1]],axis_value[move[0]],75,75])

def screen_update(board:list,movement_list:list):
    print_board()
    display_possibility(movement_list)
    print_piece(board)
    pygame.display.flip() # we actualize the screen with all the modification

def move_piece(piece:object,board1:list,position:list,list_of_move:list) :
    """
        move the piece 
    Args:
        piece (object): the piece we are mooving
        board1 (list): the board1 
        position (list): the position we are mooving the piece to
        list_of_move (list) : the list who stock all the move
    """
    if board1[position[0]][position[1]] != None :
        if board1[position[0]][position[1]].color == piece.color :
            if piece.color == "B" :
                if piece.position ==[0,0]:
                    board1[0][3] = piece
                    board1[0][3].position = [0,3]
                    board1[0][2] = board1[0][4]
                    board1[0][2].position = [0,2]
                elif piece.position == [0,7] :
                    board1[0][5] = piece
                    board1[0][5].position = [0,5]
                    board1[0][6] = board1[0][4]
                    board1[0][6].position = [0,6]
            else:
                if piece.position == [7,0] :
                    board1[7][3] = piece
                    board1[7][3].position = [7,3]
                    board1[7][2] = board1[7][4]
                    board1[7][2].position = [7,2]
                elif piece.position == [7,7] :
                    board1[7][5] = piece
                    board1[7][5].position = [7,5]
                    board1[7][6] = board1[7][4]
                    board1[7][6].position = [7,6]
        else :
            board1[position[0]][position[1]] = piece
            board1[piece.position[0]][piece.position[1]] = None
            board1[position[0]][position[1]].position = position
    else :
        if piece.name == "P" and (position[1]-1 == piece.position[1] or position[1]+1 == piece.position[1]) :
            if piece.color == "W":
                board1[position[0]+1][position[1]] = None
            else:
                board1[position[0]-1][position[1]] = None
        board1[position[0]][position[1]] = piece
        board1[piece.position[0]][piece.position[1]] = None
        board1[position[0]][position[1]].position = position
    if piece.name == "P" and position[0] == 0 :
        board1[position[0]][position[1]] = Queen("W",position,"piece\\dame_blanc.png")
    elif piece.name == "P" and position[0] == 7 :
        board1[position[0]][position[1]] = Queen("W",position,"piece\\dame_noir.png")

    board1[position[0]][position[1]].move_counter +=1
    list_of_move.append([piece.name,position])
    

def update_movement ( board:list,turn:str,list_of_move :list) -> None :
    """
    update the movement of all the piece
    Args:
        board (list): the board
        turn (str): who's turn
        list_of_move (list) :list of all the plays
    """
    for line in board :
        for piece in line :
            if piece != None :
                piece.move(board,turn,list_of_move)

def check(position:list,board:list,piece_selected:object,turn:str,list_of_move:list)->None:
    """
        return false if there is a check 
    Args:
        position (list): the move we are trying to do
        board (list): our current grid
    """

    move_piece(piece_selected,board,position,list_of_move)
    if turn == "W" :
        update_movement(board,"B",list_of_move)
        for line in board :
            for piece in line:
                if piece != None:
                    if piece.color == "B" :
                        for move_of_piece in piece.movement_list:
                            if board[move_of_piece[0]][move_of_piece[1]] != None and board[move_of_piece[0]][move_of_piece[1]].name == "K" and board[move_of_piece[0]][move_of_piece[1]].color == "W" :
                                return False
    else:
        update_movement(board,"W",list_of_move)
        for line in board :
            for piece in line:
                if piece != None:
                    if piece.color == "W":
                        for move_of_piece in piece.movement_list:
                            if board[move_of_piece[0]][move_of_piece[1]] != None and board[move_of_piece[0]][move_of_piece[1]].name == "K" and board[move_of_piece[0]][move_of_piece[1]].color == "B" :
                                return False
    return True

pygame.init() #initalize pygame 
screen = pygame.display.set_mode((600,600)) # set the size of the window
pygame.display.set_caption("echec") # set the name 

board = [ # set the grid to the correct start position
        [Rook("B",[0,0],"piece\\tour_noir.png",0),Knight("B",[0,1],"piece\\cavalier_noir.png",0),Bishop("B",[0,2],"piece\\fou_noir.png",0),Queen("B",[0,3],"piece\\dame_noir.png",0),King("B",[0,4],"piece\\roi_noir.png",0),Bishop("B",[0,5],"piece\\fou_noir.png",0),Knight("B",[0,6],"piece\\cavalier_noir.png",0),Rook("B",[0,7],"piece\\tour_noir.png",0)],
        [Pawn("B",[1,0],"piece\\pion_noir.png",0),Pawn("B",[1,1],"piece\\pion_noir.png",0),Pawn("B",[1,2],"piece\\pion_noir.png",0),Pawn("B",[1,3],"piece\\pion_noir.png",0),Pawn("B",[1,4],"piece\\pion_noir.png",0),Pawn("B",[1,5],"piece\\pion_noir.png",0),Pawn("B",[1,6],"piece\\pion_noir.png",0),Pawn("B",[1,7],"piece\\pion_noir.png",0)],
        [None,None,None,None,None,None,None,None], 
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [Pawn("W",[6,0],"piece\\pion_blanc.png",0),Pawn("W",[6,1],"piece\\pion_blanc.png",0),Pawn("W",[6,2],"piece\\pion_blanc.png",0),Pawn("W",[6,3],"piece\\pion_blanc.png",0),Pawn("W",[6,4],"piece\\pion_blanc.png",0),Pawn("W",[6,5],"piece\\pion_blanc.png",0),Pawn("W",[6,6],"piece\\pion_blanc.png",0),Pawn("W",[6,7],"piece\\pion_blanc.png",0)],
        [Rook("W",[7,0],"piece\\tour_blanc.png",0),Knight("W",[7,1],"piece\\cavalier_blanc.png",0),Bishop("W",[7,2],"piece\\fou_blanc.png",0),Queen("W",[7,3],"piece\\dame_blanc.png",0),King("W",[7,4],"piece\\roi_blanc.png",0),Bishop("W",[7,5],"piece\\fou_blanc.png",0),Knight("W",[7,6],"piece\\cavalier_blanc.png",0),Rook("W",[7,7],"piece\\tour_blanc.png",0)]
        ]
second_board = [ # set the grid to the correct start position
        [Rook("B",[0,0],"piece\\tour_noir.png",0),Knight("B",[0,1],"piece\\cavalier_noir.png",0),Bishop("B",[0,2],"piece\\fou_noir.png",0),Queen("B",[0,3],"piece\\dame_noir.png",0),King("B",[0,4],"piece\\roi_noir.png",0),Bishop("B",[0,5],"piece\\fou_noir.png",0),Knight("B",[0,6],"piece\\cavalier_noir.png",0),Rook("B",[0,7],"piece\\tour_noir.png",0)],
        [Pawn("B",[1,0],"piece\\pion_noir.png",0),Pawn("B",[1,1],"piece\\pion_noir.png",0),Pawn("B",[1,2],"piece\\pion_noir.png",0),Pawn("B",[1,3],"piece\\pion_noir.png",0),Pawn("B",[1,4],"piece\\pion_noir.png",0),Pawn("B",[1,5],"piece\\pion_noir.png",0),Pawn("B",[1,6],"piece\\pion_noir.png",0),Pawn("B",[1,7],"piece\\pion_noir.png",0)],
        [None,None,None,None,None,None,None,None], 
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [Pawn("W",[6,0],"piece\\pion_blanc.png",0),Pawn("W",[6,1],"piece\\pion_blanc.png",0),Pawn("W",[6,2],"piece\\pion_blanc.png",0),Pawn("W",[6,3],"piece\\pion_blanc.png",0),Pawn("W",[6,4],"piece\\pion_blanc.png",0),Pawn("W",[6,5],"piece\\pion_blanc.png",0),Pawn("W",[6,6],"piece\\pion_blanc.png",0),Pawn("W",[6,7],"piece\\pion_blanc.png",0)],
        [Rook("W",[7,0],"piece\\tour_blanc.png",0),Knight("W",[7,1],"piece\\cavalier_blanc.png",0),Bishop("W",[7,2],"piece\\fou_blanc.png",0),Queen("W",[7,3],"piece\\dame_blanc.png",0),King("W",[7,4],"piece\\roi_blanc.png",0),Bishop("W",[7,5],"piece\\fou_blanc.png",0),Knight("W",[7,6],"piece\\cavalier_blanc.png",0),Rook("W",[7,7],"piece\\tour_blanc.png",0)]
        ]

turn = "W"
print_board()
update_movement(board,turn,[])
print_piece(board)
pygame.display.flip() # we actualize the screen with all the modification
list_of_move = []
piece_selected = None
have_move = False

while True : 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if the user quit the game end it
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN : 
            position = where_am_i(pygame.mouse.get_pos())  # we know where on the grid the player click
            piece = board[position[0]][position[1]]
            if piece_selected != None :
                if piece_selected.color == turn :
                    for move in piece_selected.movement_list:
                        if move ==  position :
                            if check(position,board,piece_selected,turn,list_of_move) :
                                for y in range(len(board)):
                                    for x in range(len(board[y])):
                                        if board[y][x] != None and board[y][x].name == "P" :
                                            second_board[y][x] = Pawn(board[y][x].color,board[y][x].position,board[y][x].sprite_pathing,board[y][x].move_counter)
                                        elif board[y][x] != None and board[y][x].name == "K" :
                                            second_board[y][x] = King(board[y][x].color,board[y][x].position,board[y][x].sprite_pathing,board[y][x].move_counter)
                                        elif board[y][x] != None and board[y][x].name == "R" :
                                            second_board[y][x] = Rook(board[y][x].color,board[y][x].position,board[y][x].sprite_pathing,board[y][x].move_counter)
                                        elif board[y][x] != None and board[y][x].name == "Q" :
                                            second_board[y][x] = Queen(board[y][x].color,board[y][x].position,board[y][x].sprite_pathing,board[y][x].move_counter)
                                        elif board[y][x] != None and board[y][x].name == "B" :
                                            second_board[y][x] = Bishop(board[y][x].color,board[y][x].position,board[y][x].sprite_pathing,board[y][x].move_counter)
                                        elif board[y][x] != None and board[y][x].name == "N" :
                                            second_board[y][x] = Knight(board[y][x].color,board[y][x].position,board[y][x].sprite_pathing,board[y][x].move_counter)
                                        else:
                                            second_board[y][x] = None
                                if turn == "W" : 
                                    turn = "B"
                                else : 
                                    turn = "W"
                                update_movement(second_board,turn,list_of_move)
                                screen_update(board,[])
                                piece_selected = None
                                have_move = True
                                break
                            else:
                                for y in range(len(board)):
                                    for x in range(len(board[y])):
                                        if second_board[y][x] != None and second_board[y][x].name == "P" :
                                            board[y][x] = Pawn(second_board[y][x].color,second_board[y][x].position,second_board[y][x].sprite_pathing,second_board[y][x].move_counter)
                                        elif second_board[y][x] != None and second_board[y][x].name == "K" :
                                            board[y][x] = King(second_board[y][x].color,second_board[y][x].position,second_board[y][x].sprite_pathing,second_board[y][x].move_counter)
                                        elif second_board[y][x] != None and second_board[y][x].name == "R" :
                                            board[y][x] = Rook(second_board[y][x].color,second_board[y][x].position,second_board[y][x].sprite_pathing,second_board[y][x].move_counter)
                                        elif second_board[y][x] != None and second_board[y][x].name == "Q" :
                                            board[y][x] = Queen(second_board[y][x].color,second_board[y][x].position,second_board[y][x].sprite_pathing,second_board[y][x].move_counter)
                                        elif second_board[y][x] != None and second_board[y][x].name == "B" :
                                            board[y][x] = Bishop(second_board[y][x].color,second_board[y][x].position,second_board[y][x].sprite_pathing,second_board[y][x].move_counter)
                                        elif second_board[y][x] != None and second_board[y][x].name == "N" :
                                            board[y][x] = Knight(second_board[y][x].color,second_board[y][x].position,second_board[y][x].sprite_pathing,second_board[y][x].move_counter)
                                        else:
                                            board[y][x] = None
                                update_movement(board,turn,list_of_move)
                                
                                screen_update(board,[])
                                piece_selected = None
                                break
            if not have_move and piece != None and piece.color == turn:
                piece_selected = piece
                screen_update(board,piece_selected.movement_list)
            have_move = False