# Name: Courtlen Olmo
# Github Username: Mango-bear
# Date: 3/2/23
# Description: Unit test for CheckersGame.py

import unittest
import CheckersGame
class TestCheckersGame(unittest.TestCase):
    '''Contains Unit Tests for the CheckersGame.py program'''

    def setUp(self):
        self.game = CheckersGame.Checkers()
        self.player1 = self.game.create_player('John', 'White')
        self.player2 = self.game.create_player('Ashley', 'Black')


    def test_basic_piece_movement(self):
        self.game.play_game('Ashley', (5,0), (4,1))
        self.assertEqual(self.game.get_checkers_details((4,1)), 'Black')

    def test_turn_exchange(self):
        self.game.play_game('Ashley', (5, 0), (4, 1))
        self.assertFalse(self.game._black_turn, False)

    def test_piece_capture(self):
        self.game.play_game('Ashley', (5, 0), (4, 1))
        self.game.play_game('John', (2, 1), (3, 2))
        self.game.play_game('Ashley', (6, 1), (5, 0))
        self.game.play_game('John', (2, 3), (3, 4))
        self.game.play_game('Ashley', (4, 1), (2, 3))
        self.assertIs(self.game.get_checkers_details((3,2)), None)
        self.assertEqual(self.game._players.get('Ashley').get_captured_pieces_count(), 1)

    def test_king_creation(self):
        self.game.play_game('Ashley', (5, 0), (4, 1))
        self.game.play_game('John', (2, 1), (3, 2))
        self.game.play_game('Ashley', (6, 1), (5, 0))
        self.game.play_game('John', (2, 3), (3, 4))
        self.game.play_game('Ashley', (4, 1), (2, 3))
        self.game.play_game('Ashley', (5, 0), (4, 1))
        self.game.play_game('John', (1, 0), (2, 1))
        self.game.play_game('Ashley', (4, 1), (3, 0))
        self.game.play_game('John', (0, 1), (1, 0))
        self.game.play_game('Ashley', (2, 3), (0, 1))
        self.assertEqual(self.game.get_checkers_details((0, 1)), 'Black_king')
        self.assertEqual(self.game._players.get('Ashley').get_king_count(), 1)

    def test_king_reverse_movement(self):
        self.game.play_game('Ashley', (5, 0), (4, 1))
        self.game.play_game('John', (2, 1), (3, 2))
        self.game.play_game('Ashley', (6, 1), (5, 0))
        self.game.play_game('John', (2, 3), (3, 4))
        self.game.play_game('Ashley', (4, 1), (2, 3))
        self.game.play_game('Ashley', (5, 0), (4, 1))
        self.game.play_game('John', (1, 0), (2, 1))
        self.game.play_game('Ashley', (4, 1), (3, 0))
        self.game.play_game('John', (0, 1), (1, 0))
        self.game.play_game('Ashley', (2, 3), (0, 1))
        self.game.play_game('Ashley', (0, 1), (1, 2))
        self.assertEqual(self.game.get_checkers_details((1, 2)), 'Black_king')