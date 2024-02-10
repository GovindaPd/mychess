from .chessbase import ChessBase
from .chessmixin import ChessMixin
from .chessman_moves import *
from copy import deepcopy

class Chess(ChessBase,ChessMixin):
    def __init__(self,turn='W',board=None,castle=None,flag=False):
        self.for_who, self.for_opp = ('W','B') if turn=='W' else ('B','W')
        self.chessboard = self.board.copy() if board==None else board.copy()
        self.castle = self.CASTLE.copy() if castle==None else castle.copy()
        self.my,self.opp = self.get_both_data(self.for_who,self.chessboard,self.castle,flag)
        # self.count()

    @classmethod
    def count(cls):
        cls.loopcount +=1

    @classmethod
    def play(cls,chessboard=None, castle=None, turn=None, cur_depth=3, alpha=-900, beta=900, best_move=None, pr=1, maximiser=True):
        try:
            if not cls.is_valid(chessboard):return (None,0);

            obj = cls(turn,chessboard,castle) if cur_depth !=0 else cls(turn,chessboard,castle,True)
            if cur_depth ==0 or obj.is_checkmate() or obj.is_stalemate():
                if obj.is_checkmate():
                    return (None,-900+10*pr) if maximiser else (None,900-10*pr)
                elif obj.is_stalemate():
                    return (None,-900+10*pr) if maximiser else (None,900-10*pr)
                else:
                    return (None,+(obj.statistics())) if maximiser else (None,-(obj.statistics()))
            else:
                all_moves = [(man,obj.my['chessmans_positions'][man],move) for man,moves in obj.my['legal_moves'].items() for move in moves]
                
                if maximiser==False:  #minimiser
                    mineval = 900
                    for man,cur_box_id,next_box_id in all_moves:
                        
                        boardcopy=obj.chessboard.copy()
                        castlecopy=obj.castle.copy()
                        Chess.push(obj.for_who,boardcopy,castlecopy,cur_box_id,next_box_id,man)
                        m,points=cls.play(boardcopy,castlecopy,obj.for_opp,cur_depth-1,alpha,beta,pr+1,maximiser=True,)
                        
                        if points<mineval:
                            mineval = points
                            best_move = (man,cur_box_id,next_box_id,)
                        
                        beta = min(beta,mineval)
                        if beta<=alpha:
                            break
                    return best_move,mineval
                
                else:   #maximiser
                    maxeval = -900
                    for man,cur_box_id,next_box_id in all_moves:

                        boardcopy=obj.chessboard.copy()
                        castlecopy=obj.castle.copy()
                        Chess.push(obj.for_who,boardcopy,castlecopy,cur_box_id,next_box_id,man)
                        m,points = cls.play(boardcopy,castlecopy,obj.for_opp,cur_depth-1,alpha,beta,pr+1,maximiser=False,)
                        
                        if points>maxeval:
                            maxeval = points
                            best_move = (man,cur_box_id,next_box_id,)
                        
                        alpha = max(alpha,maxeval)
                        if beta<=alpha:
                            break
                    return best_move,maxeval
        except Exception as error:
            print(error)
        return  (None,0)

# if __name__ == '__main__':
    # print(play(turn='B'))