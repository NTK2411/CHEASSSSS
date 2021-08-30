import pygame,sys
import pieces

clock = pygame.time.Clock()

pygame.init()
WIDTH = 1200
HEIGHT = 600
BG_Color = (243,218,178)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("CHESS#69.420")


def draw_lines():
    pass

def poscirc():
    for i in range(0,WIDTH,100):
        for j in range(0, HEIGHT+1,100):
            pygame.draw.circle(screen, (0,0,0),(i,j), 2)

def emptyboard(x,y,edge,mx,my):  #default ->>20,20,560
    #edgelength = 560 default
    # edge = 560
    edge_sq = edge//8
    edge = edge_sq * 8

    light = (255,214,0)
    dark = (245,127,23)
    HoverColorLight = (100, 187, 103)
    HoverColorDark = (76,175,80)

    pygame.draw.rect(screen,light,(x,y,edge,edge))
    for i in range(x,x+edge,edge_sq*2):
        for j in range(y,y+edge, edge_sq):
            pygame.draw.rect(screen, dark, (i+((((j+edge_sq)//edge_sq)%2)*edge_sq),j, edge_sq,edge_sq))
    # board squares printed

    #HOVER SELECTION
    selected_tile_x = -1
    selected_tile_y = -1
    if((x<mx<x+edge) and (y<my<y+edge)):
        selected_tile_x = (mx - x) // edge_sq
        selected_tile_y = (my - y) // edge_sq
        if (selected_tile_x + selected_tile_y) % 2 == 0:
            pygame.draw.rect(screen, HoverColorLight, (x + (selected_tile_x * edge_sq),
                                         y + (selected_tile_y * edge_sq), edge_sq, edge_sq))
        if (selected_tile_x + selected_tile_y) % 2 == 1:
            pygame.draw.rect(screen, HoverColorDark, (x + (selected_tile_x * edge_sq),
                                         y + (selected_tile_y * edge_sq), edge_sq, edge_sq))

    #PRINTING NOTATIONS
    font_size =  int((15/560)*edge)
    font_notations = pygame.font.Font('aargh.ttf',font_size)
    #HORIZONTAL
    notations = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for i in range(0,8,2):
        nota = font_notations.render(notations[i],True,light)
        screen.blit(nota, ((i*edge_sq)+x+3,edge-font_size-4+y))
    for i in range(1,8,2):
        nota = font_notations.render(notations[i],True,dark)
        screen.blit(nota, ((i*edge_sq)+x+3,edge-font_size-4+y))

    #VERTICAL
    for i in range(0,8,2):
        nota = font_notations.render(str(8-i),True,light)
        screen.blit(nota, (x+edge-font_size+5,(i*edge_sq)+y+3))
    for i in range(1,8,2):
        nota = font_notations.render(str(8-i),True,dark)
        screen.blit(nota, (x+edge-font_size+5,(i*edge_sq)+y+3))

    return selected_tile_x,selected_tile_y


pieces_loc ={}  #EMPTY DECLARATION of location of pieces

pieces.pieces_init(pieces_loc) #default declaration of pieces of position----> equivalent to reset board

def drawAllPieces(x,y,edge, Image_pieces):
    edge_sq = edge // 8
    edge = edge_sq * 8

    pieces_list = list(pieces_loc.keys())
    # pieces_list = ['bb', 'bk', 'bn', 'bp', 'bq', 'br',
    #                 'wb', 'wk', 'wn', 'wp', 'wq', 'wr']

    for p in pieces_list:   #p --bole to-->> pawn, rook, knight, and etc
        pos = pieces.nota2pos(pieces_loc, p)
        pos = [[(x + a * edge_sq), (y + b * edge_sq)] for a, b in pos]
        for pix_pos in pos:
            # pieces.drawPiece(screen, p, pix_pos,Image_pieces)
            img = Image_pieces[p + '.png']
            screen.blit(img, pix_pos)


def drawSelectedandMove(x,y,edge,selected,move):
    edge_sq = edge // 8
    edge = edge_sq * 8

    if selected != None:
        SelectedColorLight = (206, 147, 216)#(114, 211, 213)#(255, 64, 129)
        SelectedColorDark = (188, 108, 202)


        selected_tile_x = selected[0]
        selected_tile_y = selected[1]
        if (selected_tile_x + selected_tile_y) % 2 == 0:
            pygame.draw.rect(screen, SelectedColorLight, (x + (selected_tile_x * edge_sq),
                                                      y + (selected_tile_y * edge_sq), edge_sq, edge_sq))
        if (selected_tile_x + selected_tile_y) % 2 == 1:
            pygame.draw.rect(screen, SelectedColorDark, (x + (selected_tile_x * edge_sq),
                                                     y + (selected_tile_y * edge_sq), edge_sq, edge_sq))

    if move != ('0', '0'):
        MoveColorLight = (195, 195, 213)#(51, 51, 72)#(255, 87, 34)
        MoveColorDark = (168, 168, 194)
        MoveColorDark = (135, 204, 0)
        MoveColorLight = (164,237,18)#(203,255,102)#(169, 255, 0)
        for i in range(2):
            pos = pieces.nota2pos_single(move[i])
            selected_tile_x = pos[0]
            selected_tile_y = pos[1]
            if (selected_tile_x+selected_tile_y)%2 == 0:
                pygame.draw.rect(screen, MoveColorLight, (x + (selected_tile_x * edge_sq),
                                                     y + (selected_tile_y * edge_sq), edge_sq, edge_sq))
            if (selected_tile_x+selected_tile_y)%2 == 1:
                pygame.draw.rect(screen, MoveColorDark, (x + (selected_tile_x * edge_sq),
                                                     y + (selected_tile_y * edge_sq), edge_sq, edge_sq))




offsetx = 20
offsety = 20
edge = 560  #offsetx,offsety,edge
boardHistory = []
clicking = False
selected = None
move = ('0', '0')
Image_pieces = pieces.loadPiecesImages(edge)
#main loop
while(1):
    # mouse position
    mx, my = pygame.mouse.get_pos()

    # drawing screen
    screen.fill(BG_Color)
    mxi, myj = emptyboard(offsetx,offsety,edge, mx, my)  # default ->>20,20,560 #dont go below 240 if you are sane
    pieces.empty(mxi, myj, pieces_loc)
    drawSelectedandMove(offsetx,offsety,edge,selected,move)
    drawAllPieces(offsetx,offsety,edge, Image_pieces)
    # poscirc()

    #buttons
    # clicking = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
                if (mxi != -1 and myj != -1):
                    selected,move = pieces.movePiece(selected,pieces_loc,mxi, myj)
                    pieces.boardHistory(pieces_loc,move,boardHistory)
                    print(boardHistory)
            if event.button == 3:
                right_clicking = True
            if event.button == 2:
                middle_click = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False


    #showing screen
    # mx, my = pygame.mouse.get_pos()

    pygame.draw.circle(screen, (0, 0, 0), (mx, my), 2)
    pygame.display.update()
    clock.tick() #easy 144 fps
    print(int(clock.get_fps()))