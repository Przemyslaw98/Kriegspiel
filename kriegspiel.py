import arcade
import socket
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import datetime

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Kriegspiel")
arcade.set_background_color(arcade.color.WHITE)



       

class Square:
    def __init__(self,f,r):
        self.rank=r
        self.file=f
        self.piece="none"
    def put(self,p):
        p.file=self.file
        p.rank=self.rank
        self.piece=p
    def take(self):
        self.piece="none"
class Piece:
    def __init__(self,c):
        self.color=c
        self.pinned="no"
        self.attemptedMoves=[]
    def draw(self):
        if board.side=="white":    
            self.sprite.center_x=50+self.file*60
            self.sprite.center_y=30+self.rank*60
        else:
            self.sprite.center_x=590-self.file*60
            self.sprite.center_y=570-self.rank*60
        self.sprite.draw()
    def move(self,square):
##        if self.type!="pawn": moveData=self.letter
##        else: moveData="P"
##        moveData+=str(self.file)+str(self.rank)+str(square.file)+str(square.rank)
        board.enPassant="none"
        if self.type=="pawn":
            if self.rank==2 and square.rank==4:
                board.enPassant=board.getSquare(self.file,3)
            elif self.rank==7 and square.rank==5:
                board.enPassant=board.getSquare(self.file,6)
        if self.type=="king":
            if self.file==5:
                if self.castling[0]=="yes" and square.file==3:
                    board.getSquare(1,self.rank).piece.move(board.getSquare(4,self.rank))
                elif self.castling[1]=="yes" and square.file==7:
                    board.getSquare(8,self.rank).piece.move(board.getSquare(6,self.rank))
            self.castling=["no","no"]
        if self.type=="rook":
            if self.color=="white" and self.rank==1:
                if self.file==1:
                    board.whiteKing.castling[0]="no"
                elif self.file==8:
                    board.whiteKing.castling[1]="no"
            elif self.color=="black" and self.rank==8:
                if self.file==1:
                    board.blackKing.castling[0]="no"
                elif self.file==8:
                    board.blackKing.castling[1]="no"
        board.getSquare(self.file,self.rank).take()
        board.getSquare(square.file,square.rank).put(self)
        
    
                
class Pawn(Piece):
    def __init__(self,c):
        super().__init__(c)
        self.type="pawn"
        self.letter="P"
        if self.color=="white":
            self.sprite=arcade.Sprite("pw.png",1)
        else: self.sprite=arcade.Sprite("pb.png",1)
    def showMoves(self):
        legalMoves=[]
        if self.pinned=="hor" or len(board.attackingPieces)>1:
            return legalMoves
        if self.color=="white":
            i=1
            s=2
        else:
            i=-1
            s=7
        for j in [-1,1]:
            if self.pinned=="ver":
                break
            if (i==j and self.pinned=="uldr")or(i!=j and self.pinned=="urdl"):
                continue
            if (board.getSquare(self.file+j,self.rank+i)!="offboard"
            and (len(board.attackingPieces)==0 or board.getSquare(self.file+j,self.rank+i) in board.attackingPieces)
            and ((board.getSquare(self.file+j,self.rank+i).piece!="none"
            and board.getSquare(self.file+j,self.rank+i).piece.color!=self.color)
            or (board.getSquare(self.file+j,self.rank+i)==board.enPassant and self.pinned!="forep"))):
                legalMoves.append(board.getSquare(self.file+j,self.rank+i))
        if board.getSquare(self.file,self.rank+i).piece=="none" and self.pinned!="uldr" and self.pinned!="urdl":
            if len(board.attackingPieces)==0 or board.getSquare(self.file,self.rank+i) in board.inbetweenSquares:
                legalMoves.append(board.getSquare(self.file,self.rank+i))
            if  self.rank==s and (board.getSquare(self.file,self.rank+i*2).piece=="none"
            and (len(board.attackingPieces)==0 or board.getSquare(self.file,self.rank+i*2) in board.inbetweenSquares)):
                legalMoves.append(board.getSquare(self.file,self.rank+i*2))
        return legalMoves
    def highlightAll(self):
        highlighted=[]
        if self.color=="white":
            i=1
            s=2
        else:
            i=-1
            s=7
        for j in [-1,1]:
            if board.getSquare(self.file+j,self.rank+i)=="offboard":
                continue
            if (board.getSquare(self.file+j,self.rank+i).piece=="none"
            or board.getSquare(self.file+j,self.rank+i).piece.color!=self.color):
                highlighted.append(board.getSquare(self.file+j,self.rank+i))
        if (board.getSquare(self.file,self.rank+i).piece=="none"
        or board.getSquare(self.file,self.rank+i).piece.color!=self.color):
            highlighted.append(board.getSquare(self.file,self.rank+i))
            if (self.rank==s and(board.getSquare(self.file,self.rank+i*2).piece=="none"
            or board.getSquare(self.file,self.rank+i*2).piece.color!=self.color)):
                highlighted.append(board.getSquare(self.file,self.rank+i*2))
        return highlighted
class Knight(Piece):    
    def __init__(self,c):
        super().__init__(c)
        self.type="knight"
        self.letter="N"
        if self.color=="white":
            self.sprite=arcade.Sprite("nw.png",1)
        else: self.sprite=arcade.Sprite("nb.png",1)
    def showMoves(self):
        legalMoves=[]
        if self.pinned=="no" and len(board.attackingPieces)<2:
            for i in [-2,-1,1,2]:
                for j in [-2,-1,1,2]:
                    if (abs(i)!=abs(j) and board.getSquare(self.file+i,self.rank+j)!="offboard"
                    and (board.getSquare(self.file+i,self.rank+j).piece=="none"
                    or board.getSquare(self.file+i,self.rank+j).piece.color!=self.color)
                    and (len(board.attackingPieces)==0 or (board.getSquare(self.file+i,self.rank+j) in board.attackingPieces
                    or board.getSquare(self.file+i,self.rank+j) in board.inbetweenSquares))):
                        legalMoves.append(board.getSquare(self.file+i,self.rank+j))
        return legalMoves
    def highlightAll(self):
        highlighted=[]
        for i in [-2,-1,1,2]:
            for j in [-2,-1,1,2]:
                if (abs(i)!=abs(j) and  board.getSquare(self.file+i,self.rank+j)!="offboard"
                and (board.getSquare(self.file+i,self.rank+j).piece=="none"
                or board.getSquare(self.file+i,self.rank+j).piece.color!=self.color)):
                    highlighted.append(board.getSquare(self.file+i,self.rank+j))
        return highlighted
class Bishop(Piece):    
    def __init__(self,c):
        super().__init__(c)
        self.type="bishop"
        self.letter="B"
        if self.color=="white":
            self.sprite=arcade.Sprite("bw.png",1)
        else: self.sprite=arcade.Sprite("bb.png",1)
    def showMoves(self):
        legalMoves=[]
        if self.pinned=="hor" or self.pinned=="ver" or len(board.attackingPieces)>1:
            return legalMoves
        for i in [-1,1]:
            for j in [-1,1]:
                if (i==j and self.pinned=="uldr")or(i!=j and self.pinned=="urdl"):
                    continue
                f=self.file
                r=self.rank
                while f+i>0 and f+i<9 and r+j>0 and r+j<9:
                    f+=i
                    r+=j
                    if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                            break
                    if (len(board.attackingPieces)==0 or (board.getSquare(f,r) in board.attackingPieces
                    or board.getSquare(f,r) in board.inbetweenSquares)):
                        legalMoves.append(board.getSquare(f,r))
                    if board.getSquare(f,r).piece!="none":
                        break
        return legalMoves
    def highlightAll(self):
        highlighted=[]
        for i in [-1,1]:
            for j in [-1,1]:
                f=self.file
                r=self.rank
                while f+i>0 and f+i<9 and r+j>0 and r+j<9:
                    f+=i
                    r+=j
                    if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                        break
                    highlighted.append(board.getSquare(f,r))
        return highlighted
class Rook(Piece):
    def __init__(self,c):
        super().__init__(c)
        self.type="rook"
        self.letter="R"
        self.castling="yes"
        if self.color=="white":
            self.sprite=arcade.Sprite("rw.png",1)
        else: self.sprite=arcade.Sprite("rb.png",1)
    def showMoves(self):
        legalMoves=[]
        if self.pinned=="uldr" or self.pinned=="urdl" or len(board.attackingPieces)>1:
            return legalMoves
        for i in [-1,1]:
            f=self.file
            r=self.rank
            while f+i>0 and f+i<9:
                if self.pinned=="ver":
                    break
                f+=i
                if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                    break
                if (len(board.attackingPieces)==0 or (board.getSquare(f,r) in board.attackingPieces
                or board.getSquare(f,r) in board.inbetweenSquares)):
                    legalMoves.append(board.getSquare(f,r))
                if board.getSquare(f,r).piece!="none":
                    break
            f=self.file
            while r+i>0 and r+i<9:
                if self.pinned=="hor":
                    break
                r+=i
                if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                    break
                if (len(board.attackingPieces)==0 or (board.getSquare(f,r) in board.attackingPieces
                or board.getSquare(f,r) in board.inbetweenSquares)):
                    legalMoves.append(board.getSquare(f,r))
                if board.getSquare(f,r).piece!="none":
                    break
        return legalMoves
    def highlightAll(self):
        highlighted=[]
        for i in [-1,1]:
            f=self.file
            r=self.rank
            while f+i>0 and f+i<9:
                f+=i
                if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                    break
                highlighted.append(board.getSquare(f,r))
            f=self.file
            while r+i>0 and r+i<9:
                r+=i
                if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                    break
                highlighted.append(board.getSquare(f,r))
        return highlighted
class Queen(Piece):
    def __init__(self,c):
        super().__init__(c)
        self.type="queen"
        self.letter="Q"
        if self.color=="white":
            self.sprite=arcade.Sprite("qw.png",1)
        else: self.sprite=arcade.Sprite("qb.png",1)
    def showMoves(self):
        legalMoves=[]
        if len(board.attackingPieces)>1:
            return legalMoves
        if self.pinned!="uldr" and self.pinned!="urdl":
             for i in [-1,1]:
                f=self.file
                r=self.rank
                while f+i>0 and f+i<9:
                    if self.pinned=="ver":
                        break
                    f+=i
                    if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                        break
                    if (len(board.attackingPieces)==0 or (board.getSquare(f,r) in board.attackingPieces
                    or board.getSquare(f,r) in board.inbetweenSquares)):
                        legalMoves.append(board.getSquare(f,r))
                    if board.getSquare(f,r).piece!="none":
                        break
                f=self.file
                while r+i>0 and r+i<9:
                    if self.pinned=="hor":
                        break
                    r+=i
                    if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                        break
                    if (len(board.attackingPieces)==0 or (board.getSquare(f,r) in board.attackingPieces
                    or board.getSquare(f,r) in board.inbetweenSquares)):
                        legalMoves.append(board.getSquare(f,r))
                    if board.getSquare(f,r).piece!="none":
                        break
        if self.pinned!="hor" and self.pinned!="ver":
            for i in [-1,1]:
                for j in [-1,1]:
                    if (i==j and self.pinned=="uldr")or(i!=j and self.pinned=="urdl"):
                        continue
                    f=self.file
                    r=self.rank
                    while f+i>0 and f+i<9 and r+j>0 and r+j<9:
                        f+=i
                        r+=j
                        if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                            break
                        if (len(board.attackingPieces)==0 or (board.getSquare(f,r) in board.attackingPieces
                        or board.getSquare(f,r) in board.inbetweenSquares)):
                            legalMoves.append(board.getSquare(f,r))
                        if board.getSquare(f,r).piece!="none":
                            break
        return legalMoves
    def highlightAll(self):
        highlighted=[]
        for i in [-1,1]:
            f=self.file
            r=self.rank
            while f+i>0 and f+i<9:
                f+=i
                if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                    break
                highlighted.append(board.getSquare(f,r))
            f=self.file
            while r+i>0 and r+i<9:
                r+=i
                if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                    break
                highlighted.append(board.getSquare(f,r))
        for i in [-1,1]:
            for j in [-1,1]:
                f=self.file
                r=self.rank
                while f+i>0 and f+i<9 and r+j>0 and r+j<9:
                    f+=i
                    r+=j
                    if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color:
                        break
                    highlighted.append(board.getSquare(f,r))
        return highlighted
class King(Piece):
    def __init__(self,c):
        super().__init__(c)
        self.type="king"
        self.letter="K"
        self.castling=["yes","yes"]
        if self.color=="white":
            self.sprite=arcade.Sprite("kw.png",1)
        else: self.sprite=arcade.Sprite("kb.png",1)
    def showMoves(self):
        legalMoves=[]
        for i in [-1,-0,1]:
            for j in [-1,-0,1]:
                if ((i!=0 or j!=0) and board.getSquare(self.file+i,self.rank+j)!="offboard"
                and (board.getSquare(self.file+i,self.rank+j).piece=="none"
                or board.getSquare(self.file+i,self.rank+j).piece.color!=self.color)
                and len(self.checkForCheck(board.getSquare(self.file+i,self.rank+j),"false")[0])==0):
                    legalMoves.append(board.getSquare(self.file+i,self.rank+j))
        if len(board.attackingPieces)==0:
            if (self.castling[0]=="yes" and board.getSquare(2,self.rank).piece=="none"
            and board.getSquare(3,self.rank).piece=="none" and board.getSquare(4,self.rank).piece=="none"
            and len(self.checkForCheck(board.getSquare(3,self.rank),"false")[0])==0
            and len(self.checkForCheck(board.getSquare(4,self.rank),"false")[0])==0):
                legalMoves.append(board.getSquare(3,self.rank))
            if (self.castling[1]=="yes" and board.getSquare(6,self.rank).piece=="none"
            and board.getSquare(7,self.rank).piece=="none"
            and len(self.checkForCheck(board.getSquare(6,self.rank),"false")[0])==0
            and len(self.checkForCheck(board.getSquare(7,self.rank),"false")[0])==0):
                legalMoves.append(board.getSquare(7,self.rank))
        return legalMoves
    def highlightAll(self):
        highlighted=[]
        for i in [-1,-0,1]:
            for j in [-1,-0,1]:
                if ((i!=0 or j!=0) and board.getSquare(self.file+i,self.rank+j)!="offboard"
                and (board.getSquare(self.file+i,self.rank+j).piece=="none"
                or  board.getSquare(self.file+i,self.rank+j).piece.color!=self.color)):
                    highlighted.append(board.getSquare(self.file+i,self.rank+j))
        if (self.castling[0]=="yes" and board.getSquare(2,self.rank).piece=="none"
        and board.getSquare(3,self.rank).piece=="none" and board.getSquare(4,self.rank).piece=="none"):
            highlighted.append(board.getSquare(3,self.rank))
        if (self.castling[1]=="yes" and board.getSquare(6,self.rank).piece=="none"
        and board.getSquare(7,self.rank).piece=="none"):
            highlighted.append(board.getSquare(7,self.rank))
        return highlighted
    def checkForCheck(self,square,b):
        attacked=[]
        inbetween=[]
        direction=[]
        for i in [-1,-0,1]:
            for j in [-1,-0,1]:
                if ((i!=0 or j!=0) and board.getSquare(square.file+i,square.rank+j)!="offboard"
                and board.getSquare(square.file+i,square.rank+j).piece!="none"
                and board.getSquare(square.file+i,square.rank+j).piece.color!=self.color
                and board.getSquare(square.file+i,square.rank+j).piece.type=="king"):
                    attacked.append(board.getSquare(square.file+i,square.rank+j))
        for i in [-2,-1,1,2]:
            for j in [-2,-1,1,2]:
                if (abs(i)!=abs(j) and board.getSquare(square.file+i,square.rank+j)!="offboard"
                and board.getSquare(square.file+i,square.rank+j).piece!="none"
                and board.getSquare(square.file+i,square.rank+j).piece.color!=self.color
                and board.getSquare(square.file+i,square.rank+j).piece.type=="knight"):
                    attacked.append(board.getSquare(square.file+i,square.rank+j))
                    direction.append("knight")
        for i in [-1,1]:
            if self.color=="white":
                j=1
            else: j=-1
            if (board.getSquare(square.file+i,square.rank+j)!="offboard"
            and board.getSquare(square.file+i,square.rank+j).piece!="none"
            and board.getSquare(square.file+i,square.rank+j).piece.color!=self.color
            and board.getSquare(square.file+i,square.rank+j).piece.type=="pawn"):
                attacked.append(board.getSquare(square.file+i,square.rank+j))
                if i==j:
                    direction.append("urdl")
                else: direction.append("uldr")
        for i in [-1,1]:
            r=square.rank
            f=square.file
            while f+i>0 and f+i<9:
                f+=i
                if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece!=self:
                    if (board.getSquare(f,r).piece.color!=self.color
                    and (board.getSquare(f,r).piece.type=="rook" or board.getSquare(f,r).piece.type=="queen")):
                        attacked.append(board.getSquare(f,r))
                        direction.append("hor")                       
                        while f-i!=self.file and b=="true":
                            f-=i
                            inbetween.append(board.getSquare(f,r))
                    break
            f=square.file
            while r+i>0 and r+i<9:
                r+=i
                if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece!=self:
                    if (board.getSquare(f,r).piece.color!=self.color
                    and (board.getSquare(f,r).piece.type=="rook" or board.getSquare(f,r).piece.type=="queen")):
                        attacked.append(board.getSquare(f,r))
                        direction.append("ver")
                        while r-i!=self.rank and b=="true":
                            r-=i
                            inbetween.append(board.getSquare(f,r))
                    break       
        for i in [-1,1]:
            for j in [-1,1]:
                r=square.rank
                f=square.file
                while f+i>0 and f+i<9 and r+j>0 and r+j<9:
                    f+=i
                    r+=j
                    if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece!=self:
                        if (board.getSquare(f,r).piece.color!=self.color
                        and (board.getSquare(f,r).piece.type=="bishop" or board.getSquare(f,r).piece.type=="queen")):
                            attacked.append(board.getSquare(f,r))
                            if i==j:
                                direction.append("urdl")
                            else: direction.append("uldr")
                            while f-i!=self.file and b=="true":
                                r-=j
                                f-=i
                                inbetween.append(board.getSquare(f,r))
                        break
                
        
        return [attacked,inbetween,direction]
    def checkForPins(self):
        for i in [-1,-0,1]:
            for j in [-1,-0,1]:
                if i==0 and j==0:
                    continue
                f=self.file
                r=self.rank
                if self.color=="white":
                    ep=[5,6]
                else: ep=[4,3]
                while f+i>0 and f+i<9 and r+j>0 and r+j<9:
                    forep="false"
                    f+=i
                    r+=j
                    if board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color!=self.color:
                        if j==0 and self.rank==ep[0] and board.enPassant==board.getSquare(f,ep[1]):
                            forep="true"
                        else: break
                    if (board.getSquare(f,r).piece!="none" and board.getSquare(f,r).piece.color==self.color
                    and (forep=="false" or board.getSquare(f,r).piece.type=="pawn")):
                        potentialPin=board.getSquare(f,r).piece
                        while f+i>0 and f+i<9 and r+j>0 and r+j<9:
                            f+=i
                            r+=j
                            if board.getSquare(f,r).piece!="none":
                                if board.getSquare(f,r).piece.color==self.color:
                                    break
                                elif (j==0 and self.rank==ep[0] and board.enPassant==board.getSquare(f,ep[1])
                                and potentialPin.type=="pawn"):
                                    forep="true"
                                    continue
                                elif (i!=0 and j==0 and (board.getSquare(f,r).piece.type=="rook"
                                or board.getSquare(f,r).piece.type=="queen")):
                                    if forep=="true":
                                        potentialPin.pinned="forep"
                                    else: potentialPin.pinned="hor"
                                elif (i==0 and j!=0 and (board.getSquare(f,r).piece.type=="rook"
                                or board.getSquare(f,r).piece.type=="queen")):
                                    potentialPin.pinned="ver"
                                elif (i!=0 and j!=0 and i!=j and (board.getSquare(f,r).piece.type=="bishop"
                                or board.getSquare(f,r).piece.type=="queen")):
                                    potentialPin.pinned="uldr"
                                elif (i!=0 and j!=0 and i==j and (board.getSquare(f,r).piece.type=="bishop"
                                or board.getSquare(f,r).piece.type=="queen")):
                                    potentialPin.pinned="urdl"
                                break
                        break
class Board:
    def getSquare(self,f,r):
        if f>0 and r>0 and f<9 and r<9:
            return self.squares[(f-1)*8+r-1]
        else: return "offboard"
    def __init__(self,s,n,o):
        self.side=s
        self.myName=n
        self.oppName=o
        self.result="*"
        date=datetime.datetime.now()
        self.date=str(date.year) + "."
        if date.month < 10:
            self.date += "0"
        self.date += str(date.month) + "."
        if date.day < 10:
            self.date += "0"
        self.date += str(date.day)
        self.buttons=[]
        self.buttons.append(Button(180, 60, 672, 190, "is.png", "as.png"))
        self.buttons.append(Button(180, 60, 672, 130, "io.png", "ao.png"))
        self.buttons.append(Button(180, 60, 672, 130, "ic.png", "ac.png"))
        self.buttons.append(Button(60, 60, 612, 190, "il.png", "al.png"))
        self.buttons.append(Button(60, 60, 672, 190, "iv.png", "av.png"))
        self.buttons.append(Button(60, 60, 732, 190, "ir.png", "ar.png"))
        self.buttons.append(Button(180, 60, 672, 130, "ib.png", "ab.png"))
        if self.side=="white":
            self.ranks="12345678"
            self.files="abcdefgh"
            self.turnMessage ="Your move"
        else:
            self.ranks="87654321"
            self.files="hgfedcba"
            self.turnMessage ="Opponent's move"

        self.pieces=[]
        self.squares=[]
        self.captured=[]

        self.turn="white"
        self.message=" "
        self.enPassant="none"
        self.lastCaptured = "none"
        self.promotionDialog = "none"
        self.lastMove = ""
        self.hiddenMove = ""
        self.drawCondition = "no"
        self.attackingPieces = []
        self.inbetweenSquares = []

        self.sprite=arcade.Sprite("board.png",1)
        self.sprite.center_x=320
        self.sprite.center_y=300

        self.highlightedPiece="none"
        self.legalHighlight=[]
        self.allHighlight=[]
        self.lastHighlight = []
        self.checkHighlight = []
        self.redHighlight=[]

        self.turnNumber=0
        self.positionBuffer = []
        self.movesFull=[]
        self.movesPGN=[]
        self.movesToDo=[]
        self.numberList=[]
        self.moveListW = []
        self.moveListWH = []
        self.moveListB = []
        self.moveListBH = []
        self.PGNstring=""

        for i in range(8):
            for j in range(8):
                self.squares.append(Square(i+1,j+1))
        for i in range(8):
            pawn=Pawn("white")
            self.pieces.append(pawn)
            self.getSquare(i+1,2).put(pawn)
            pawn=Pawn("black")
            self.pieces.append(pawn)
            self.getSquare(i+1,7).put(pawn)
        for i in [1,8]:
            if i==1: c="white"
            elif i==8: c="black"
            piece=Rook(c)
            self.pieces.append(piece)
            self.getSquare(1,i).put(piece)
            piece=Knight(c)
            self.pieces.append(piece)
            self.getSquare(2,i).put(piece)
            piece=Bishop(c)
            self.pieces.append(piece)
            self.getSquare(3,i).put(piece)
            piece=Queen(c)
            self.pieces.append(piece)
            self.getSquare(4,i).put(piece)
            piece=Bishop(c)
            self.pieces.append(piece)
            self.getSquare(6,i).put(piece)
            piece=Knight(c)
            self.pieces.append(piece)
            self.getSquare(7,i).put(piece)
            piece=Rook(c)
            self.pieces.append(piece)
            self.getSquare(8,i).put(piece)
        self.whiteKing=King("white")
        self.pieces.append(self.whiteKing)
        self.getSquare(5,1).put(self.whiteKing)
        self.blackKing=King("black")
        self.pieces.append(self.blackKing)
        self.getSquare(5,8).put(self.blackKing)
    def setup(self,data):
        pgnReader = PGNreader(data)
        while len(self.movesToDo)>0:
            string=self.movesToDo.pop()
            moveData=self.read(self.turn,string)
            fullString=self.writeFull(moveData[0],moveData[1],moveData[2])
            self.movesFull.append(fullString)
            self.lastMove = string
            self.move(fullString)
            self.moveDone("no")
        game.state="game"
    def reverse(self):
        if self.side=="white":
            self.side="black"
        else: self.side="white"
        tmp=self.myName
        self.myName=self.oppName
        self.oppName=tmp
        if self.side=="white":
            self.ranks="12345678"
            self.files="abcdefgh"
        else:
            self.ranks="87654321"
            self.files="hgfedcba"
    def savePGN(self):
        pgn="[Event \"Casual Kriegspiel Match\"]\n[Site \"?\"]\n[Date \""+self.date+"\"]\n[Round \"-\"]\n"
        if self.side=="white":
            white=self.myName
            black=self.oppName
        else:
            black = self.myName
            white = self.oppName
        pgn+="[White \""+white+"\"]\n[Black \""+black+"\"]\n[Result \""+self.result+"\"]\n\n"
        line=""
        printCounter=0
        line+="1. "+self.movesPGN[0]
        for i in range(1,len(self.movesPGN)):
            if i%2==0:
                numberToken=str((i//2)+1)+"."
                if printCounter+len(numberToken)>=80:
                    pgn+=line+"\n"
                    line=numberToken
                    printCounter=len(numberToken)
                else:
                    line+=" "+numberToken
                    printCounter+=len(numberToken)
            moveToken=self.movesPGN[i]
            if printCounter + len(moveToken) >= 80:
                pgn += line + "\n"
                line = moveToken
                printCounter = len(moveToken)
            else:
                line += " "+moveToken
                printCounter += len(moveToken)
        if printCounter + len(self.result) >= 80:
            pgn += line + "\n"+self.result
        else: pgn +=line + " "+self.result
        return pgn

    def automoveDone(self):
        self.lastHighlight.clear()
        self.checkHighlight.clear()
        self.attackingPieces.clear()
        self.inbetweenSquares.clear()
        for i in self.pieces:
            i.pinned="no"
        if self.turn == "white":
            self.turn = "black"
            if len(self.blackKing.checkForCheck(self.getSquare(self.blackKing.file, self.blackKing.rank), "true")[0]) > 0:
                self.attackingPieces =self.blackKing.checkForCheck(self.getSquare(self.blackKing.file, self.blackKing.rank), "true")[0]
                self.inbetweenSquares=self.blackKing.checkForCheck(self.getSquare(self.blackKing.file, self.blackKing.rank), "true")[1]
                self.checkHighlight.append(self.blackKing)
                for i in self.attackingPieces:
                    self.checkHighlight.append(i)
            self.blackKing.checkForPins()
        elif self.turn == "black":
            self.turn = "white"
            if len(self.whiteKing.checkForCheck(self.getSquare(self.whiteKing.file, self.whiteKing.rank), "true")[0]) > 0:
                self.attackingPieces =self.whiteKing.checkForCheck(self.getSquare(self.whiteKing.file, self.whiteKing.rank), "true")[0]
                self.inbetweenSquares=self.whiteKing.checkForCheck(self.getSquare(self.whiteKing.file, self.whiteKing.rank), "true")[1]
                self.checkHighlight.append(self.whiteKing)
                for i in self.attackingPieces:
                    self.checkHighlight.append(i)
            self.whiteKing.checkForPins()
        self.lastHighlight.append(self.getSquare(int(self.movesFull[-1][1]), int(self.movesFull[-1][2])))
        self.lastHighlight.append(self.getSquare(int(self.movesFull[-1][3]), int(self.movesFull[-1][4])))
    def moveDone(self,drawOffer):
        self.message=" "
        self.redHighlight.clear()
        self.checkHighlight.clear()
        self.lastHighlight.clear()
        self.attackingPieces.clear()
        self.inbetweenSquares.clear()
        self.drawCondition="no"
        if self.lastCaptured!= "none":
            self.redHighlight.append(self.lastCaptured)
            self.message="Capture on " + chr(self.lastCaptured.file + 96) + str(self.lastCaptured.rank)
        self.lastHighlight.append(self.getSquare(int(self.movesFull[-1][1]), int(self.movesFull[-1][2])))
        self.lastHighlight.append(self.getSquare(int(self.movesFull[-1][3]), int(self.movesFull[-1][4])))
        for i in self.pieces:
            i.pinned="no"
            i.attemptedMoves.clear()
        if self.turn=="white":
            self.turn="black"
            if len(self.blackKing.checkForCheck(self.getSquare(self.blackKing.file,self.blackKing.rank),"true")[0])>0:
                self.attackingPieces=self.blackKing.checkForCheck(self.getSquare(self.blackKing.file,self.blackKing.rank),"true")[0]
                self.inbetweenSquares=self.blackKing.checkForCheck(self.getSquare(self.blackKing.file,self.blackKing.rank),"true")[1]
                self.highlightCheck(self.blackKing)
                self.checkHighlight.append(self.blackKing)
                for i in self.attackingPieces:
                    self.checkHighlight.append(i)
            self.blackKing.checkForPins()
        elif self.turn=="black":
            self.turn="white"
            if len(self.whiteKing.checkForCheck(self.getSquare(self.whiteKing.file,self.whiteKing.rank),"true")[0])>0:
                self.attackingPieces=self.whiteKing.checkForCheck(self.getSquare(self.whiteKing.file,self.whiteKing.rank),"true")[0]
                self.inbetweenSquares=self.whiteKing.checkForCheck(self.getSquare(self.whiteKing.file,self.whiteKing.rank),"true")[1]
                self.highlightCheck(self.whiteKing)
                self.checkHighlight.append(self.whiteKing)
                for i in self.attackingPieces:
                    self.checkHighlight.append(i)
            self.whiteKing.checkForPins()
        moveCounter=0
        for i in self.pieces:
            if i.color==self.turn:
                moveCounter+=len(i.showMoves())
        global game
        if moveCounter==0:
            game.state="finished"
            if len(self.attackingPieces)>0:
                self.message="Checkmate"
                if "#" not in self.lastMove:
                    self.lastMove+="#"
                if self.turn=="black":
                    self.result="1-0"
                else: self.result="0-1"
            else:
                self.message="Stalemate"
                self.result = "1/2-1/2"
        elif len(self.attackingPieces)>0:
            if self.message!=" ":
                self.message+=", "
            self.message+="Check"
            if "+" not in self.lastMove:
                self.lastMove+="+"
        draw="no"
        if len(self.pieces)<4:
            draw="yes"
            if len(self.pieces)==3:
                for i in self.pieces:
                    if i.type=="pawn" or i.type=="rook" or i.type=="queen":
                        draw="no"
        if len(self.pieces)==4:
            draw="no"
            tmp=""
            for i in self.pieces:
                if i.type=="bishop":
                    if tmp=="":
                        if (i.file+i.rank)%2==1:
                            tmp="odd"
                        else: tmp="even"
                    else:
                        if (((i.file+i.rank)%2==1 and tmp=="odd")
                        or ((i.file+i.rank)%2==0 and tmp=="even")):
                            draw="yes"
                elif i.type!="king":
                    break
        if draw=="yes":
            game.state="finished"
            self.message="Draw by dead position"
            self.result = "1/2-1/2"
        position=self.turn
        if self.enPassant!="none":
            position+="ep"
        if self.whiteKing.castling[0]=="yes":
            position+="qw"
        if self.whiteKing.castling[1]=="yes":
            position+="kw"
        if self.blackKing.castling[0]=="yes":
            position+="qb"
        if self.blackKing.castling[1]=="yes":
            position+="kb"
        for i in self.squares:
            if i.piece!="none":
                position+=str(i.file)+str(i.rank)+i.piece.letter
        self.positionBuffer.append(position)

        if game.state!="finished":
            if self.positionBuffer.count(position) > 2:
                self.drawCondition = "Threefold repetition"
            if self.positionBuffer.count(position)>4:
                game.state = "finished"
                self.message="Draw by repetition"
                self.result = "1/2-1/2"

            if len(self.positionBuffer) > 99:
                self.drawCondition = "Fifty moves without\ncaptures and pawn moves"
            if len(self.positionBuffer)>149:
                game.state = "finished"
                self.message = "Draw by 75-move-rule"
                self.result = "1/2-1/2"

        self.movesPGN.append(self.lastMove)
        if drawOffer=="yes":
            if  self.drawCondition=="no":
                self.drawCondition = "Opponent offers a draw.\nMake a move to reject"
            else:
                game.state="finished"
                self.result = "1/2-1/2"
                if self.drawCondition == "Threefold repetition":
                    self.message = "Draw by repetition"
                elif self.drawCondition == "Fifty moves without\ncaptures and pawn moves":
                    self.message = "Draw by fifty-move-rule"
                socketManager.sendMove(board.message)
                self.turnMessage = " "
        if game.state!="finished" :
            if self.turn==self.side:
                self.turnMessage ="Your move"
            else: self.turnMessage ="Opponent's move"
        else: self.turnMessage=" "
        if self.turn == "black":
            self.turnNumber += 1
            self.numberList.append(str(self.turnNumber)+".")
            self.moveListW.append(self.lastMove)
            if self.side=="white":
                self.moveListWH.append(self.lastMove)
            else: self.moveListWH.append(self.hide(self.lastMove))
        else:
            self.moveListB.append(self.lastMove)
            if self.side=="black":
                self.moveListBH.append(self.lastMove)
            else: self.moveListBH.append(self.hide(self.lastMove))
    def undo(self):
        self.movesToDo.append(self.movesPGN.pop())
        string=self.movesFull.pop()
        if string[0]=="K" and string[1]=="5":
            if string[3]=="7":
                self.getSquare(6, int(string[4])).piece.move(self.getSquare(8, int(string[2])))
            elif string[3]=="3":
                self.getSquare(4, int(string[4])).piece.move(self.getSquare(1, int(string[2])))
        if string[14]!=".":
            self.pieces.remove(self.getSquare(int(string[3]),int(string[4])).piece)
            self.getSquare(int(string[3]),int(string[4])).take()
            for p in self.captured:
                if p.file==int(string[1]) and p.rank==int(string[2]) and p.color!=self.turn and p.letter==string[0]:
                    self.captured.remove(p)
                    self.pieces.append(p)
                    self.getSquare(int(string[1]), int(string[2])).put(p)
                    break
        else:self.getSquare(int(string[3]), int(string[4])).piece.move(self.getSquare(int(string[1]), int(string[2])))
        if string[7] != ".":
            for p in self.captured:
                if p.file == int(string[8]) and p.rank == int(string[9]) and p.color == self.turn and p.letter ==string[7]:
                    self.captured.remove(p)
                    self.pieces.append(p)
                    self.getSquare(int(string[8]), int(string[9])).put(p)
                    break
        if string[5]!=".":
            self.enPassant=self.getSquare(int(string[5]),int(string[6]))
        if string[10] == "y":
            self.whiteKing.castling[0] = "yes"
        if string[11] == "y":
            self.whiteKing.castling[1] = "yes"
        if string[12] == "y":
            self.blackKing.castling[0] = "yes"
        if string[13] == "y":
            self.blackKing.castling[1] = "yes"

        self.checkHighlight.clear()
        self.lastHighlight.clear()
        self.attackingPieces.clear()
        self.inbetweenSquares.clear()
        for i in self.pieces:
            i.pinned="no"
        if self.turn=="white":
            self.turn="black"
            if len(self.blackKing.checkForCheck(self.getSquare(self.blackKing.file,self.blackKing.rank),"true")[0])>0:
                self.attackingPieces=self.blackKing.checkForCheck(self.getSquare(self.blackKing.file,self.blackKing.rank),"true")[0]
                self.checkHighlight.append(self.blackKing)
                for i in self.attackingPieces:
                    self.checkHighlight.append(i)
            self.blackKing.checkForPins()
        elif self.turn=="black":
            self.turn="white"
            if len(self.whiteKing.checkForCheck(self.getSquare(self.whiteKing.file,self.whiteKing.rank),"true")[0])>0:
                self.attackingPieces=self.whiteKing.checkForCheck(self.getSquare(self.whiteKing.file,self.whiteKing.rank),"true")[0]
                self.checkHighlight.append(self.blackKing)
                for i in self.attackingPieces:
                    self.checkHighlight.append(i)
            self.whiteKing.checkForPins()
        if len(self.movesFull)>0:
            self.lastHighlight.append(self.getSquare(int(self.movesFull[-1][1]), int(self.movesFull[-1][2])))
            self.lastHighlight.append(self.getSquare(int(self.movesFull[-1][3]), int(self.movesFull[-1][4])))
    def move(self,string):
        #0-typ bierki
        #1,2-Pole wyjściowe
        #3,4-Pole docelowe
        #5,6-pole ewentualnego bicia w przelocie
        #7,8,9-typ i lokalizacja zbitej bierki
        #10-13-prawa do roszad
        #14-promocja
        if string[0]=="P":
            self.positionBuffer.clear()
        if string[7]==".":
            self.lastCaptured ="none"
        else:
            self.captured.append(self.getSquare(int(string[8]),int(string[9])).piece)
            self.pieces.remove(self.getSquare(int(string[8]),int(string[9])).piece)
            self.lastCaptured = self.getSquare(int(string[8]), int(string[9])).piece
            self.getSquare(int(string[8]), int(string[9])).take()
            self.positionBuffer.clear()
        if string[14] == ".":
            self.getSquare(int(string[1]),int(string[2])).piece.move(self.getSquare(int(string[3]),int(string[4])))
        else:
            color=self.getSquare(int(string[1]), int(string[2])).piece.color
            self.captured.append(self.getSquare(int(string[1]), int(string[2])).piece)
            self.pieces.remove(self.getSquare(int(string[1]), int(string[2])).piece)
            self.getSquare(int(string[1]), int(string[2])).take()
            if string[14] == "N":
                piece = Knight(color)
            elif string[14] == "B":
                piece = Bishop(color)
            elif string[14] == "R":
                piece = Rook(color)
            elif string[14] == "Q":
                piece = Queen(color)
            self.pieces.append(piece)
            self.getSquare(int(string[3]),int(string[4])).put(piece)


    def read(self,color,string):
        if string=="O-O":
            if color=="white": r=1
            else: r=8
            return [self.getSquare(5,r).piece,self.getSquare(7,r),"none"]
        if string=="O-O-O":
            if color=="white": r=1
            else: r=8
            return [self.getSquare(5,r).piece,self.getSquare(3,r),"none"]
        if string[0]=="K":
            pieceType="king"
        elif string[0]=="Q":
            pieceType="queen"
        elif string[0]=="R":
            pieceType="rook"
        elif string[0]=="B":
            pieceType="bishop"
        elif string[0]=="N":
            pieceType="knight"
        else: pieceType="pawn"
        oFile="u"
        oRank="u"
        dFile="u"
        dRank="u"
        for i in reversed(string):
            if i in "abcdefgh":
                if dFile=="u": dFile=ord(i)-96
                else: oFile=ord(i)-96
            if i in "12345678":
                if dRank=="u": dRank=ord(i)-48
                else: oRank=ord(i)-48
        for i in self.pieces:
            if oFile!="u" and oRank!="u":
                break
            if (i.color==color and pieceType==i.type and self.getSquare(dFile,dRank) in i.showMoves()
            and (oFile=="u" or oFile==i.file) and (oRank=="u" or oRank==i.rank)):
                oFile=i.file
                oRank=i.rank
        if string.find("=")!=-1:
            promoted=string[string.find("=")+1]
        else: promoted="none"
        return [self.getSquare(oFile,oRank).piece,self.getSquare(dFile,dRank),promoted]
    def writeFull(self,piece,dSquare,promotion):
        #0-typ bierki
        #1,2-Pole wyjściowe
        #3,4-Pole docelowe
        #5,6-pole ewentualnego bicia w przelocie
        #7,8,9-typ i lokalizacja zbitej bierki
        #10-13-prawa do roszad
        #14-promocja
        string = piece.letter
        string+=str(piece.file)+str(piece.rank)+str(dSquare.file)+str(dSquare.rank)
        if self.enPassant != "none":
            string +=str(self.enPassant.file)+str(self.enPassant.rank)
        else: string+=".."
        if dSquare.piece!="none":
            string+=dSquare.piece.letter+str(dSquare.file)+str(dSquare.rank)
        elif dSquare==self.enPassant and piece.type=="pawn":
            string += "P" + str(dSquare.file)
            if self.enPassant.rank==3:
                string +="4"
            else: string+="5"
        else: string+="..."
        if self.whiteKing.castling[0]=="yes":
            string+="y"
        else:string+="n"
        if self.whiteKing.castling[1]=="yes":
            string+="y"
        else:string+="n"
        if self.blackKing.castling[0]=="yes":
            string+="y"
        else:string+="n"
        if self.blackKing.castling[1]=="yes":
            string+="y"
        else:string+="n"
        if promotion!="none":
            string+=promotion
        else: string+="."
        return string
    #def moveRight(self):
    #def moveLeft(self):
    def write(self,moveString):
        # 0-typ bierki
        # 1,2-Pole wyjściowe
        # 3,4-Pole docelowe
        # 5,6-pole ewentualnego bicia w przelocie
        # 7,8,9-typ i lokalizacja zbitej bierki
        # 10-13-prawa do roszad
        # 14-promocja
        color=self.getSquare(int(moveString[1]),int(moveString[2]))
        string = ""
        if moveString[0]!="P": string+=moveString[0]
        elif moveString[1]!=moveString[3]:
            string+=chr(int(moveString[1])+96)+"x"
        if moveString[0]=="K" and moveString[1]=="5":
            if moveString[3]=="3":
                return "O-O-O"
            elif moveString[3]=="7":
                return "O-O"
        files=[]
        ranks=[]
        for i in self.pieces:
            if i.color==color and i.letter==moveString[0] and self.getSquare(int(moveString[3]),int(moveString[4])) in i.showMoves():
                files.append(i.file)
                ranks.append(i.rank)
        if len(files)>1:
            if files.count(int(moveString[1]))==1:
                string+=chr(int(moveString[1])+96)
            elif ranks.count(int(moveString[2]))==1:
                string+=str(int(moveString[2]))
            else: string+=chr(int(moveString[1])+96)+str(int(moveString[2]))
        if moveString[7]!="." and moveString[0]!="P": string+="x"
        string+=chr(int(moveString[3])+96)+str(int(moveString[4]))
        if moveString[14]!=".":
            string+="="+moveString[14]
        return string
    def hide(self,string):
        rewrittenOne="?"
        for c in range(len(string)):
            if string[c]=="x":
                rewrittenOne+="x"+string[c+1]+string[c+2]
            if string[c] == "+": rewrittenOne+="+"
        return rewrittenOne
    def highlightCheck(self,king):
        if king.checkForCheck(self.getSquare(king.file,king.rank),"true")[2].count("hor")>0:
            for i in range(8):
                self.redHighlight.append(self.getSquare(i + 1, king.rank))
        if king.checkForCheck(self.getSquare(king.file,king.rank),"true")[2].count("ver")>0:
            for i in range(8):
                self.redHighlight.append(self.getSquare(king.file, i + 1))
        if king.checkForCheck(self.getSquare(king.file,king.rank),"true")[2].count("urdl")>0:
            self.redHighlight.append(self.getSquare(king.file, king.rank))
            for i in [-1,1]:
                f=king.file
                r=king.rank
                while f+i>0 and f+i<9 and r+i>0 and r+i<9:
                    f+=i
                    r+=i
                    self.redHighlight.append(self.getSquare(f, r))
        if king.checkForCheck(self.getSquare(king.file,king.rank),"true")[2].count("uldr")>0:
            self.redHighlight.append(self.getSquare(king.file, king.rank))
            for i in [-1,1]:
                f=king.file
                r=king.rank
                while f+i>0 and f+i<9 and r-i>0 and r-i<9:
                    f+=i
                    r-=i
                    self.redHighlight.append(self.getSquare(f, r))
        if king.checkForCheck(self.getSquare(king.file,king.rank),"true")[2].count("knight")>0:
            if board.side==board.turn:
                self.redHighlight.append(self.getSquare(king.file, king.rank))
                for i in [-2,-1,1,2]:
                    for j in [-2,-1,1,2]:
                        if abs(i)!=abs(j) and self.getSquare(king.file+i,king.rank+j)!="offboard":
                            self.redHighlight.append(self.getSquare(king.file + i, king.rank + j))
            else:
                for n in self.attackingPieces:
                    if n.piece.type=="knight":
                        self.redHighlight.append(self.getSquare(n.file, n.rank))
                        for i in [-2,-1,1,2]:
                            for j in [-2,-1,1,2]:
                                if abs(i)!=abs(j) and self.getSquare(n.file+i,n.rank+j)!="offboard":
                                    self.redHighlight.append(self.getSquare(n.file + i, n.rank + j))

board=""
socketManager=""
game=""
class Button:
    def __init__(self,width,height,x,y,inactive,active):
        self.base=arcade.Sprite(inactive,1,center_x=x,center_y=y)
        self.highlighted=arcade.Sprite(active,1,center_x=x,center_y=y)
        self.left=x-width/2
        self.right=x+width/2
        self.top=y+height/2
        self.bottom=y-height/2
        self.active="no"
    def checkMouse(self,x,y):
        if x>=self.left and x<self.right and y>=self.bottom and y<self.top:
            self.active="yes"
        else: self.active="no"
    def draw(self):
        if self.active=="no":
            self.base.draw()
        else: self.highlighted.draw()
class MainMenu:
    def __init__(self):
        self.board=arcade.Sprite("board.png",1)
        #self.buttons=arcade.Sprite("btns.png",1)
        self.buttons=[]
        self.buttons.append(Button(480, 60, 320, 390, "ip.png", "ap.png"))
        self.buttons.append(Button(480, 60, 320, 330, "iw.png", "aw.png"))
        self.buttons.append(Button(480, 60, 320, 210, "ie.png", "ae.png"))
        self.submenu=0
    def draw(self):
        self.board.center_x=320
        self.board.center_y=300
        self.board.draw()
#        if self.submenu==0:
        for i in self.buttons:
            i.draw()
class PromotionDialog:
    def __init__(self,p):
        self.color=p.color
        self.piece=p
        if self.color=="white":
            self.buttonN=arcade.Sprite("nw.png",1)
            self.buttonB=arcade.Sprite("bw.png",1)
            self.buttonR=arcade.Sprite("rw.png",1)
            self.buttonQ=arcade.Sprite("qw.png",1)
        else:
            self.buttonN=arcade.Sprite("nb.png",1)
            self.buttonB=arcade.Sprite("bb.png",1)
            self.buttonR=arcade.Sprite("rb.png",1)
            self.buttonQ=arcade.Sprite("qb.png",1)
        self.buttonN.center_x=230
        self.buttonB.center_x=290
        self.buttonR.center_x=350
        self.buttonQ.center_x=410
        self.buttonN.center_y=570
        self.buttonB.center_y=570
        self.buttonR.center_y=570
        self.buttonQ.center_y=570
    def draw(self):
        self.buttonN.draw()
        self.buttonB.draw()
        self.buttonR.draw()
        self.buttonQ.draw()

class RedHighlight:
    def __init__(self,square):
        self.sprite=arcade.Sprite("rhl.png",1)
        if board.side=="white":    
            self.sprite.center_x=50+square.file*60
            self.sprite.center_y=30+square.rank*60
        else:    
            self.sprite.center_x=590-square.file*60
            self.sprite.center_y=570-square.rank*60
class MoveHighlight:
    def __init__(self,square):
        self.sprite=arcade.Sprite("yhl.png",1)
        if board.side=="white":    
            self.sprite.center_x=50+square.file*60
            self.sprite.center_y=30+square.rank*60
        else:    
            self.sprite.center_x=590-square.file*60
            self.sprite.center_y=570-square.rank*60
class CrossHighlight:
    def __init__(self,square):
        self.sprite=arcade.Sprite("wr.png",1)
        if board.side=="white":
            self.sprite.center_x=50+square.file*60
            self.sprite.center_y=30+square.rank*60
        else:
            self.sprite.center_x=590-square.file*60
            self.sprite.center_y=570-square.rank*60

class Socket:
    def __init__(self,mode,data,game,name,file):
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.mode=mode
        global board
        if mode=="server":
            if data==3:
                date=datetime.datetime.now()
                data=(date.microsecond%2)+1
            if data==1:
                colorS="white"
                colorC="black"
            if data==2:
                colorS="black"
                colorC="white"    
            self.server.bind(('',12345))
            self.server.listen(1)
            
            self.con,addr=self.server.accept()
            data=colorC+name
            self.con.send(data.encode())
            oppName=self.con.recv(1024).decode()
            if file!="":
                file = open(file, "r")
                data = file.readlines()
                file.close()
                for l in data:
                    self.con.send(l.encode())
            l="done"
            self.con.send(l.encode())
            board=Board(colorS,name,oppName)
            if len(data)>0:
                board.state="setup"
                board.setup(data)
        elif mode=="client":
            self.server.connect((data,12345))
            data=self.server.recv(1024).decode()
            self.server.send(name.encode())
            color=data[:5]
            oppName=data[5:]
            data=[]
            while True:
                get = self.server.recv(1024).decode()
                if get=="done":
                    break
                else: data.append(get)
            board=Board(color,name,oppName)
            if len(data) > 0:
                board.state = "setup"
                board.setup(data)
        game.state="game"
    def sendMove(self,move):
        if self.mode=="server":
            self.con.send(move.encode())
        elif self.mode=="client":
            self.server.send(move.encode())
    def getMove(self):
        if self.mode=="server":
            oppMove=self.con.recv(1024)
        elif self.mode=="client":
            oppMove=self.server.recv(1024)
        return oppMove
class Submenu:
    def __init__(self,game):
        self.config = tkinter.Tk()
        self.mode = tkinter.IntVar()
        self.color=tkinter.IntVar()
        self.address=tkinter.StringVar()
        self.name=tkinter.StringVar()
        self.file=""
        self.color.set(0)
        self.address.set("")
        def callback():
            global socketManager
            if self.mode.get()==1 and self.color.get()>0 and len(self.name.get())>0:
                socketManager=Socket("server",self.color.get(),game,self.name.get(),self.file)
                self.config.destroy()
            if self.mode.get()==2 and len(self.address.get())>0 and len(self.name.get())>0:
                socketManager=Socket("client",self.address.get(),game,self.name.get(),"")
                self.config.destroy()
        def gray():
            if self.mode.get()==1:
                col1.config(state="normal")
                col2.config(state="normal")
                col3.config(state="normal")
                button.config(state="normal")
                ipBox.config(state="disabled")
            if self.mode.get()==2:
                col1.config(state="disabled")
                col2.config(state="disabled")
                col3.config(state="disabled")
                button.config(state="disabled")
                ipBox.config(state="normal")
        def posSelect():
            root = tkinter.Tk()
            root.withdraw()
            root.filename = filedialog.askopenfilename(initialdir="./", title="Select file",filetypes=(("PGN files", "*.pgn"), ("all files", "*.*")))
            fileBox.config(text=root.filename)
            self.file=root.filename
            root.destroy()
        tkinter.Entry(self.config,textvariable=self.name).grid(row=0,column=1)
        tkinter.Label(self.config,text="Name").grid(row=0,column=0)
        tkinter.Radiobutton(self.config, text="Server", variable=self.mode, value=1,command=gray).grid(row=1,column=0)
        tkinter.Radiobutton(self.config, text="Client", variable=self.mode, value=2,command=gray).grid(row=1,column=2)
        tkinter.Label(self.config,text="Color:").grid(row=2,column=0)                    
        col1=tkinter.Radiobutton(self.config, text="White", variable=self.color, value=1,state="disabled")
        col1.grid(row=3,column=0)
        col2=tkinter.Radiobutton(self.config, text="Black", variable=self.color, value=2,state="disabled")
        col2.grid(row=4,column=0)
        col3=tkinter.Radiobutton(self.config, text="Random", variable=self.color, value=3,state="disabled")
        col3.grid(row=5,column=0)
        button=tkinter.Button(self.config,text="Start from position:",command=posSelect, state="disabled")
        button.grid(row=6,column=0)
        fileBox=tkinter.Label(self.config, text="")
        fileBox.grid(row=6, column=1)


        tkinter.Label(self.config,text="IP:").grid(row=2,column=2)  
        ipBox=tkinter.Entry(self.config,textvariable=self.address,state="disabled")
        ipBox.grid(row=3,column=2)
        tkinter.Button(self.config,text="OK",command=callback).grid(row=7,column=1)
        tkinter.mainloop()

class PGNreader:
    def __init__(self,data):
        tagFlag=0
        tags=[]
        moves=[]
        commentFlag=0
        for i in data:
            tag=""
            move=""
            for c in i:
                if c=="[":
                    tagFlag=1
                elif c=="]":
                    tagFlag=0
                    tags.append(tag)
                    tag=""
                elif c=="{":
                    commentFlag=1
                    if move != "":
                        moves.append(move)
                        move = ""
                elif c=="}":
                    commentFlag=0
                elif tagFlag==1:
                    tag+=c
                elif commentFlag==0:
                    if c!=" " and c!="\n":
                        move+=c
                    elif move!="":
                        moves.append(move)
                        move=""
            if move!="": moves.append(move)
        validChars="abcdefgh12345678PNBRQKOx=+-#!?"
        rewrittenList=[]
        for m in moves:
            rewrittenOne=""
            for c in m:
                if c in validChars and( rewrittenOne!="" or c not in "12345678"):
                    rewrittenOne+=c
            if len(rewrittenOne)>1:
                rewrittenList.append(rewrittenOne)
        if len(rewrittenList)>0 and rewrittenList[-1][0]=="-":
            rewrittenList.remove(rewrittenList[-1])
        tagNames=[]
        tagValues=[]
        for t in tags:
            valueFlag = 0
            tag = ""
            value = ""
            for c in t:
                if c not in "[ ]\"":
                    if valueFlag==0:
                        tag+=c
                    else: value+=c
                elif c==" ":
                    valueFlag=1
            valueFlag=0
            tagNames.append(tag)
            tagValues.append(value)
        white=""
        black=""
        date=""
        result=""
        for i in range(len(tags)):
            if tagNames[i]=="White":
                white=tagValues[i]
            elif tagNames[i] == "Black":
                black = tagValues[i]
            elif tagNames[i] == "Date":
                date = tagValues[i]
            elif tagNames[i] == "Result":
                result = tagValues[i]
        global board
        if game.state=="watch":
            board=Board("white",white,black)
        board.result=result
        board.date=date
        for i in reversed(rewrittenList):
            board.movesToDo.append(i)
        turnNumber=1
        if game.state == "watch":
            for m in reversed(board.movesToDo):
                turnNumber+=1
                if turnNumber%2==0:
                    board.numberList.append(str(turnNumber//2)+".")
                    board.moveListW.append(m)
                    if game.state!="setup" or board.side=="white":
                        board.moveListWH.append(m)
                    else: board.moveListWH.append(board.hide(m))
                else:
                    board.moveListB.append(m)
                    if game.state != "setup" or board.side == "black":
                        board.moveListBH.append(m)
                    else: board.moveListBH.append(board.hide(m))

class Game(arcade.Window):
    def __init__(self,width,height):
        super().__init__(width,height)
        arcade.set_background_color(arcade.color.WHITE)
        self.state="menu"
        self.menu=MainMenu()
        self.endFlag=1
        self.threadFlag=0
    def on_draw(self):
        if self.state=="menu":
            arcade.start_render()
            self.menu.draw()
        else:
            arcade.start_render()
            board.sprite.draw()
            x=70
            y=30
            for i in board.ranks:
                y+=60
                arcade.draw_text(i,x, y, arcade.color.BLACK, 18, width=60,align="center",anchor_x="center", anchor_y="center")
            x=50
            y=50
            for i in board.files:
                x+=60
                arcade.draw_text(i,x, y, arcade.color.BLACK, 18, width=60,align="center",anchor_x="center", anchor_y="center")
            if self.state=="watch":
                for i in board.lastHighlight:
                    MoveHighlight(i).sprite.draw()
                for i in board.checkHighlight:
                    RedHighlight(i).sprite.draw()
            else:
                for i in board.allHighlight:
                    if i in board.highlightedPiece.attemptedMoves:
                        CrossHighlight(i).sprite.draw()
                    else: MoveHighlight(i).sprite.draw()
                for i in board.redHighlight:
                    RedHighlight(i).sprite.draw()
            for i in board.pieces:
                if i.color==board.side or self.state!="game": i.draw()
            if board.promotionDialog!="none" and board.promotionDialog.color==board.side:
                board.promotionDialog.draw()
            if self.state=="game":
                arcade.draw_text(board.turnMessage,672, 240, arcade.color.RED, 18, width=200,align="center",anchor_x="center", anchor_y="center")
            if self.state=="game":
                board.buttons[0].draw()
                if board.drawCondition=="no" or board.drawCondition=="Draw offer will be\nsent once you move":
                    board.buttons[1].draw()
                else:
                    board.buttons[2].draw()
                if board.drawCondition != "no":
                    arcade.draw_text(board.drawCondition, 672, 50, arcade.color.RED, 18, align="center", anchor_x="center",anchor_y="center")
            elif game.state=="watch":
                board.buttons[3].draw()
                board.buttons[4].draw()
                board.buttons[5].draw()
                board.buttons[6].draw()
            numberList=""
            whiteList=""
            blackList=""
            if self.state=="game":
                number=len(board.numberList)
            else: number=max(min((((len(board.movesPGN)+1)//2)+5),len(board.numberList)),min(10,len(board.numberList)))
            for n in range(number):
                if n > number - 11:
                    numberList += board.numberList[n] + "\n"
                    if self.state=="game":
                        whiteList+=board.moveListWH[n]+"\n"
                        if n<len(board.moveListBH):
                            blackList += board.moveListBH[n] + "\n"
                    else:
                        whiteList += board.moveListW[n] + "\n"
                        if n < len(board.moveListB):
                            blackList += board.moveListB[n] + "\n"
            if numberList!="":
                arcade.draw_text(numberList, 608, 540, arcade.color.BLACK, 15, align="right", anchor_x="right",anchor_y="top")
            if whiteList!="":
                arcade.draw_text(whiteList, 615, 540, arcade.color.BLACK, 15, align="left", anchor_x="left",anchor_y="top")
            if blackList!="":
                arcade.draw_text(blackList, 700, 540, arcade.color.BLACK, 15, align="left", anchor_x="left",anchor_y="top")
            arcade.draw_text(board.myName,80, 24, arcade.color.BLACK, 18,align="left",anchor_x="left", anchor_y="center")
            arcade.draw_text(board.oppName,80, 564, arcade.color.BLACK, 18,align="left",anchor_x="left", anchor_y="center")
            arcade.draw_text(board.message,560, 24, arcade.color.RED, 18,align="right",anchor_x="right", anchor_y="center")
            arcade.finish_render()
    def on_mouse_motion(self, x, y, dx, dy):
        if self.state=="menu":
            for i in self.menu.buttons:
                i.checkMouse(x,y)
        else:
            for i in board.buttons:
                i.checkMouse(x,y)
    def on_mouse_press(self,x,y,button,modifiers):
        global board
        global socketManager
        if self.state=="menu":
            if x>=80 and x<560:
                if y>=360 and y<420 and self.menu.submenu==0:
                    self.menu.submenu=1
                    self.submenu=Submenu(self)
                    self.menu.submenu=0
                elif y >= 300 and y < 360 and self.menu.submenu == 0:
                    self.menu.submenu=1
                    root = tkinter.Tk()
                    root.withdraw()
                    root.filename = filedialog.askopenfilename(initialdir="./", title="Select file",filetypes=(("PGN files", "*.pgn"),("all files", "*.*")))
                    if root.filename!="":
                        file = open(root.filename, "r")
                        data=file.readlines()
                        file.close()
                        self.state = "watch"
                        pgnReader=PGNreader(data)
                    root.destroy()
                    self.menu.submenu=0
                elif y >= 180 and y < 240 and self.menu.submenu == 0:
                    arcade.close_window()
        elif self.state == "watch":
            if y >= 160 and y < 220:
                if x >= 582 and x < 642:
                    if len(board.movesPGN) > 0:
                        board.undo()
                elif x >= 642 and x < 702:
                    board.reverse()
                elif x >= 702 and x < 762:
                    if len(board.movesToDo)>0:
                        movePGN =board.movesToDo.pop()
                        moveData = board.read(board.turn,movePGN)
                        moveString = board.writeFull(moveData[0], moveData[1], moveData[2])
                        board.movesFull.append(moveString)
                        board.movesPGN.append(movePGN)
                        board.move(moveString)
                        board.automoveDone()
            elif y >= 100 and y < 160 and x >= 582 and x < 762:
                self.state="menu"
                board = ""
                socketManager = ""
        elif self.state=="game" and board.side==board.turn:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if board.promotionDialog=="none":
                    if x>=582 and x<762:
                        if y>=160 and y<220:
                            self.state = "finished"
                            if board.side == "black":
                                board.result = "1-0"
                            else:
                                board.result = "0-1"
                            board.message = "You surrendered"
                            socketManager.sendMove("surrender")
                            board.turnMessage = " "

                        elif y>=100 and y<160:
                            if board.drawCondition=="no":
                                board.drawCondition = "Draw offer will be\nsent once you move"
                            elif board.drawCondition!="Draw offer will be\nsent once you move":
                                self.state = "finished"
                                board.result = "1/2-1/2"
                                if board.drawCondition=="Threefold repetition":
                                    board.message = "Draw by repetition"
                                elif board.drawCondition == "Fifty moves without\ncaptures and pawn moves":
                                    board.message = "Draw by fifty-move-rule"
                                elif board.drawCondition=="Opponent offers a draw.\nMake a move to reject":
                                    board.message = "Draw by mutual aggrement"
                                socketManager.sendMove(board.message)
                                board.turnMessage = " "
                    if board.side=="black":
                        x=640-x
                        y=600-y
                    if len(board.allHighlight) > 0 and board.getSquare((x - 20) // 60,y // 60) in board.allHighlight and board.getSquare((x - 20) // 60,y // 60) not in board.legalHighlight:
                        if board.getSquare((x-20)//60,y//60) not in board.highlightedPiece.attemptedMoves:
                            board.highlightedPiece.attemptedMoves.append(board.getSquare((x-20)//60,y//60))
                    elif len(board.legalHighlight)>0 and board.getSquare((x-20)//60,y//60) in board.legalHighlight:
                        if board.getSquare((x-20)//60,y//60)!=board.getSquare(board.highlightedPiece.file,board.highlightedPiece.rank):
                            self.dSquare = board.getSquare((x - 20) // 60, y // 60)
                            if board.highlightedPiece.type == "pawn" and (board.getSquare((x-20)//60,y//60).rank==1 or board.getSquare((x-20)//60,y//60).rank==8):
                                board.promotionDialog = PromotionDialog(board.highlightedPiece)
                            else:
                                moveString=board.writeFull(board.highlightedPiece, self.dSquare, "none")
                                board.movesFull.append(moveString)
                                board.lastMove = board.write(moveString)
                                board.move(moveString)
                                if board.drawCondition == "Draw offer will be\nsent once you move":
                                    moveString += "d"
                                board.moveDone("no")
                                socketManager.sendMove(moveString)
                                board.turnMessage = "Opponent's move"
                        board.legalHighlight.clear()
                        board.allHighlight.clear()
                        board.highlightedPiece="none"
                    elif x>=80 and x<560 and y>=60 and y<540:
                        board.legalHighlight.clear()
                        board.allHighlight.clear()
                        board.highlightedPiece="none"
                        if board.getSquare((x-20)//60,y//60).piece!="none" and board.getSquare((x-20)//60,y//60).piece.color==board.turn:
                            board.legalHighlight=board.getSquare((x-20)//60,y//60).piece.showMoves()
                            board.allHighlight=board.getSquare((x-20)//60,y//60).piece.highlightAll()
                            board.legalHighlight.append(board.getSquare((x-20)//60,y//60))
                            board.allHighlight.append(board.getSquare((x-20)//60,y//60))
                            board.highlightedPiece=board.getSquare((x-20)//60,y//60).piece
                            self.highlightedPiece="none"
                elif y>=540 and y<600 and x>=200 and x<440:
                    if x>=200 and x<260:
                        promoted="N"
                    if x>=260 and x<320:
                        promoted="B"
                    if x>=320 and x<380:
                        promoted="R"
                    if x>=380 and x<440:
                        promoted="Q"
                    piece=board.promotionDialog.piece
                    board.promotionDialog="none"
                    moveString=board.writeFull(piece, self.dSquare, promoted)
                    board.movesFull.append(moveString)
                    board.lastMove = board.write(moveString)
                    board.move(moveString)
                    if board.drawCondition == "Draw offer will be\nsent once you move":
                        moveString += "d"
                    board.moveDone("no")
                    socketManager.sendMove(moveString)
                    self.turnMessage = "Opponent's move"
    def on_update(self,delta_time):
        if self.state=="game" and board.side!=board.turn:
            self.on_draw()
            self.on_draw()
            oppMove=socketManager.getMove().decode()
            board.turnMessage = " "
            if oppMove=="surrender":
                self.state = "finished"
                board.message = "Opponent surrendered"
                if board.side=="white":
                    board.result = "1-0"
                else: board.result = "0-1"
            elif oppMove[:4] == "Draw":
                self.state = "finished"
                board.result = "1/2-1/2"
                board.message = oppMove
            else:
                draw="no"
                if len(oppMove)==16:
                    oppMove=oppMove[:15]
                    draw="yes"
                if len(oppMove)==15:
                    board.movesFull.append(oppMove)
                    board.lastMove = board.write(oppMove)
                    board.move(oppMove)
                    board.moveDone(draw)
        if self.state=="finished":
            self.on_draw()
            self.on_draw()
            ask= tkinter.Tk()
            ask.withdraw()
            ask.answer=messagebox.askyesno("Game over", "Would you like to save game data?")
            if ask.answer==True:
                root = tkinter.Tk()
                root.withdraw()
                root.filename = filedialog.asksaveasfilename(initialdir="./", title="Save as...",filetypes=(("PGN files", "*.pgn"), ("all files", "*.*")))
                if root.filename != "":
                    file = open(root.filename, "w")
                    file.write(board.savePGN())
                    file.close()
                    self.state = "watch"
                root.destroy()
            ask.destroy()
            self.state="watch"
def main():
    global game
    game=Game(800,600)
    arcade.run()

if __name__ == "__main__":
    main()
