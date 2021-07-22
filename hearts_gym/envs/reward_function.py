"""
The reward function an agent optimizes to win at Hearts.
"""

import numpy as np

from hearts_gym.utils.typing import Reward
from .hearts_env import HeartsEnv


class RewardFunction:
    """
    The reward function an agent optimizes to win at Hearts.

    Calling this returns the reward.
    """

    def __init__(self, env: HeartsEnv):
        self.env = env
        self.game = env.game

    def __call__(self, *args, **kwargs) -> Reward:
        return self.compute_reward(*args, **kwargs)

    def compute_reward(
            self,
            player_index: int,
            prev_active_player_index: int,
            trick_is_over: bool,
    ) -> Reward:
        """Return the reward for the player with the given index.

        It is important to keep in mind that most of the time, the
        arguments are unrelated to the player getting their reward. This
        is because agents receive their reward only when it is their
        next turn, not right after their turn. Due to this peculiarity,
        it is encouraged to use `self.game.prev_played_cards`,
        `self.game.prev_was_illegals`, and others.

        Args:
            player_index (int): Index of the player to return the reward
                for. This is most of the time _not_ the player that took
                the action (which is given by `prev_active_player_index`).
            prev_active_player_index (int): Index of the previously
                active player that took the action. In other words, the
                active player index before the action was taken.
            trick_is_over (bool): Whether the action ended the trick.

        Returns:
            Reward: Reward for the player with the given index.
        """
        score = 0

        card = self.game.prev_played_cards[player_index]
        hand = self.game.prev_hands[player_index]
        table = self.game.prev_table_cards


        if card is None:
            return 0

        if hand is None:
            return 0

        if table is None:
            return 0

        empty_bonus = 0

        #### ILLEGAL MOVES RULE
        if self.game.prev_was_illegals[player_index]:
            return -self.game.max_penalty * self.game.max_num_cards_on_hand

        #### DETERMINE IF THE HAND LACKS A SUIT AND GIVES BONUSES TO EACH RULE ON EMPTY SUITS
        hearts = []
        spades = []
        clubs = []
        diamonds = []

        for c in hand:
            if c.suit == 0:
                clubs.append(c)
            elif c.suit == 1:
                diamonds.append(c)
            elif c.suit == 2:
                hearts.append(c)
            elif c.suit == 3:
                spades.append(c)

        if not hearts:
           empty_bonus += 5
        if not spades:
           empty_bonus += 5
        if not clubs:
           empty_bonus += 5
        if not diamonds:
           empty_bonus += 5


        #1 # If i played a high card i get a bonus, 
        #### but only if it didn't lead to a penalty in the round

        if card.rank > 8:
            if self.game.prev_trick_winner_index == player_index:
                assert self.game.prev_trick_penalty is not None
                score += -self.game.prev_trick_penalty + empty_bonus
            else:
                score += 1 + empty_bonus

        #2 # If i play a Queen of Spades:
        #### and take the trick: max penalty
        #### and dodge the trick: max bonus

        if card.suit == 3: #spades
            if card.rank == 10: #Queen
                if self.game.prev_trick_winner_index == player_index:
                    assert self.game.prev_trick_penalty is not None
                    score += -26 + empty_bonus
                else:
                    score += 26 + empty_bonus

        #3 # Bonus if you play a spade card > Q when trick isn't openend on spades.
        ####
        if card.suit == 3:
            if card.rank > 10:
                if table:
                    if table[0].suit != 3:
                        score += 5 + empty_bonus

        #4 # Mega bonus if you play a spade Q when trick isn't opened on spades
        if card.suit == 3:
           if card.rank == 10:
              if table[0].suit != 3:
                 score += 50 + empty_bonus

        #5 # Bonus if you play a spade when you dont have a spade card > Q
        ####
        if card.suit == 3:
            Queen = 'no'
            for c in hand:
               if c.suit == 3:
                  if c.rank == 10:
                      Queen = 'yes'
            if Queen == 'yes':
               score += -5 + empty_bonus
            elif Queen != 'yes':
               score += 5 + empty_bonus


        #6 # Penalty for getting trick with hearst/spades
        ####
        if self.game.prev_trick_winner_index == player_index:
            assert self.game.prev_trick_penalty is not None
            score += -self.game.prev_trick_penalty + empty_bonus
        else:
            score += 1 + empty_bonus
        # return -penalty

        return score
