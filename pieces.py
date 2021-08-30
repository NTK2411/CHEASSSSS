import pygame
import legal
def pieces_init(p):
    p['wp'] = []
    for i in range(8):
        p['wp'].append(chr(97 + i) + str(2))
    p["wr"] = ['a1', 'h1']
    p["wn"] = ['b1', 'g1']
    p["wb"] = ['c1', 'f1']
    p["wq"] = ['d1']
    p["wk"] = ['e1']
    # p[key]= value(can be anything int, char, list, array dictionary)

    # BLACK PIECES INITIALIZE
    p['bp'] = []
    for i in range(8):
        p['bp'].append(chr(97 + i) + str(7))
    p["br"] = ['a8', 'h8']
    p["bn"] = ['b8', 'g8']
    p["bb"] = ['c8', 'f8']
    p["bq"] = ['d8']
    p["bk"] = ['e8']

def nota2pos(p_dict,p): #notation to ordinate for a list from dictionary
    pos = []
    nota = p_dict[p]
    for i in nota:
        pos.append((int(ord(i[0])-97),int(8-int(i[1]))))
    return pos

def nota2pos_single(p):
    return int(ord(p[0]) - 97), int(8 - int(p[1]))

def pos2nota(i,j):
    nota = chr(97 + i) + str(8-j)
    return nota

#['Pawn_W', 'Rook_W', 'Knight_W', 'Bishop_W', 'Queen_W', 'King_W', 'Pawn_B', 'Rook_B', 'Knight_B', 'Bishop_B', 'Queen_B', 'King_B']
#pygame.transform.scale(img,(witdh,height)) #bekar scaling
def loadPiecesImages(edge):
    edge_sq = edge // 8
    rescaled2 = (edge_sq, edge_sq)
    name = ['bb.png', 'bk.png', 'bn.png', 'bp.png', 'bq.png', 'br.png',
            'wb.png', 'wk.png', 'wn.png', 'wp.png', 'wq.png', 'wr.png']
    PiecesImageArray = {}
    for p in name:

        img = pygame.image.load(p).convert_alpha()
        img2 = pygame.transform.smoothscale(img, rescaled2)
        PiecesImageArray[p] = img2

    return PiecesImageArray

#make all drawing functions in main.py
def drawPiece(screen,p,pix_pos,PiecesImageArray):
    img = PiecesImageArray[p + '.png']
    screen.blit(img, pix_pos)

def empty(mxi,myj,p):
    pos = pos2nota(mxi,myj)
    flag = 0
    if (mxi != -1 and myj != -1):
        for key, value in p.items():
            if pos in value:
                flag = 1
        if flag == 0:
            # print("EMPTY")
            return True
        if flag == 1:
            # print("NOT EMPTY")
            return False

def pieceSelected(mxi,myj,p):
    pos = pos2nota(mxi, myj)
    if (mxi != -1 and myj != -1):
        for key, value in p.items():
            if pos in value:
                return key,pos
    else:
        return None,None

def movePiece(selected,p,x,y):#pass mxi and myj
    #called under protection x and y are not equal to -1

    successfulMove = ('0', '0')

    if selected == (x, y):
        selected = None
        # print("unselected")
    #capture
    elif selected != None and pieceSelected(x, y, p) != None:
        peece, pos = pieceSelected(selected[0], selected[1], p)
        newpeece, newpos = pieceSelected(x, y, p)

        if selected != None:
            #Piece lifted
            for key, value in p.items():
                if peece == key:
                    if pos in value:
                        z = value.index(pos)
                        value.pop(z)
            #capture
            for key, value in p.items():
                if newpeece == key:
                    if newpos in value:
                        z = value.index(newpos)
                        value.pop(z)
            #Piece Kept
            for key, value in p.items():
                if peece == key:
                    value.append(newpos)
            selected = None
            successfulMove = (pos, newpos)

    elif selected != None and pieceSelected(x, y, p) == None:
        peece, pos = pieceSelected(selected[0], selected[1], p)
        newpos = pos2nota(x,y)
        if selected != None:
            # Piece lifted
            for key, value in p.items():
                if peece == key:
                    if pos in value:
                        z = value.index(pos)
                        value.pop(z)
            # Piece Kept
            for key, value in p.items():
                if peece == key:
                    value.append(newpos)
            selected = None
            successfulMove = (pos,newpos)


    elif selected == None:
        if empty(x,y,p) == False:
            selected = (x, y)
            # print(selected)
    return selected,successfulMove

def boardHistory(p,move,hist_list):
    if move != ('0', '0'):
        for key, value in p.items():
            if move[1] in value:
                current_move_info = (key,move[1])
        hist_list.append(current_move_info)