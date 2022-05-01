from main import *
import unittest


class testing(unittest.TestCase):

    def test_Get_All_Moves(self):
        board = TicTacToeBoard()

        board.set(0,0, GameBoardPlayer.X)
        board.set(0, 1, GameBoardPlayer.X)
        board.set(0, 2, GameBoardPlayer.X)

        move_list = [(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

        moves = board.get_all_moves()

        self.assertEqual(moves, move_list)

    #Clearly my AI is not that smart; however, this is how I would test it.
    def test_Ai_Player(self):
        board = TicTacToeBoard()
        board.set(0, 0, GameBoardPlayer.O)
        board.set(0, 1, GameBoardPlayer.O)
        play = AiPlayer(GameBoardPlayer.X)
        row, col = play.get_move(board)
        self.assertEqual((0,2), (row,col))

    def test_Ai_Player2(self):
        board = TicTacToeBoard()
        board.set(0, 0, GameBoardPlayer.O)
        board.set(1, 1, GameBoardPlayer.O)
        play = AiPlayer(GameBoardPlayer.X)
        row, col = play.get_move(board)
        self.assertEqual((2, 2), (row, col))

    def test_Ai_vs_Ai(self):

        game_list = [ttt_game(player_x=AiPlayer(GameBoardPlayer.X), player_o=AiPlayer(GameBoardPlayer.O)), ttt_game(player_x=AiPlayer(GameBoardPlayer.X),
                                  player_o=AiPlayer(GameBoardPlayer.O)), ttt_game(player_x=AiPlayer(GameBoardPlayer.X),
                                  player_o=AiPlayer(GameBoardPlayer.O))]

        for game in game_list:
            self.assertEqual(game, GameBoardPlayer.DRAW)
