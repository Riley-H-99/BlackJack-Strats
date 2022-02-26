import math

import deck
import random
import collections
import time


def draw_card(shoe):
    prob_one = shoe.one / shoe.total
    prob_two = shoe.two / shoe.total
    two_int = prob_one + prob_two
    prob_three = shoe.three / shoe.total
    three_int = two_int + prob_three
    prob_four = shoe.four / shoe.total
    four_int = three_int + prob_four
    prob_five = shoe.five / shoe.total
    five_int = four_int + prob_five
    prob_six = shoe.six / shoe.total
    six_int = five_int + prob_six
    prob_seven = shoe.seven / shoe.total
    seven_int = six_int + prob_seven
    prob_eight = shoe.eight / shoe.total
    eight_int = seven_int + prob_eight
    prob_nine = shoe.nine / shoe.total
    nine_int = eight_int + prob_nine
    prob_ten = shoe.ten / shoe.total
    r = random.random()
    if r < prob_one:
        card = 11
    elif r < two_int:
        card = 2
    elif r < three_int:
        card = 3
    elif r < four_int:
        card = 4
    elif r < five_int:
        card = 5
    elif r < six_int:
        card = 6
    elif r < seven_int:
        card = 7
    elif r < eight_int:
        card = 8
    elif r < nine_int:
        card = 9
    else:
        card = 10
    shoe.update_card(card)
    return card


def new_hand(shoe):
    player_hand = [draw_card(shoe), draw_card(shoe)]
    dealer_hand = [draw_card(shoe)]
    return player_hand, dealer_hand


def stand_calc(player_hand, dealer_card, shoe):
    #print('stand calc')
    win_odds = 0
    tie_odds = 0
    if sum(player_hand) > 21:
        player_hand = ace_change(player_hand)
    if sum(player_hand) > 21:
        return -1, 0, 0
    win_low = sum(player_hand) - 1
    combinations = []
    tie_comb = []
    cont_comb = []
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    i = 0
    j = 9
    while dealer_card + cards[i] < 17:
        if shoe.cards_left(cards[i]) > 0:
            cont_comb.append([cards[i]])
        i += 1
        if i == 10:
            break
    while dealer_card + cards[j] >= 17:
        if dealer_card + cards[j] == sum(player_hand):
            tie_comb.append([cards[j]])
        if dealer_card + cards[j] <= win_low and shoe.cards_left(cards[j]) > 0:
            combinations.append([cards[j]])
        j -= 1
        if j < 0:
            break
    next_comb = cont_comb
    for index in range(8):
        temp_comb = next_comb
        next_comb = []
        for current_comb in temp_comb:
            k = 0
            j = 9
            current_sum = dealer_card + sum(current_comb)
            while current_sum + cards[k] < 17:
                if cards[k] == 11 or cards[k] == 1:
                    cards_used = current_comb.count(1) + current_comb.count(11) + 1
                else:
                    cards_used = current_comb.count(cards[k]) + 1
                if cards_used <= shoe.cards_left(cards[k]):
                    next_comb.append(current_comb + [cards[k]])
                k += 1
                if k == 10:
                    break
            while current_sum + cards[j] >= 17:
                if cards[j] == 11 or cards[j] == 1:
                    cards_used = current_comb.count(1) + current_comb.count(11) + 1
                else:
                    cards_used = current_comb.count(cards[j]) + 1
                if cards_used <= shoe.cards_left(cards[j]):
                    card = cards[j]
                    if current_sum + card > 21 and card == 11:
                        card = 1
                        if current_sum + card < 17:
                            next_comb.append(current_comb + [card])
                    elif 11 in current_comb and current_sum + card > 21:
                        new_comb = ace_change(current_comb)
                        next_comb.append(new_comb + [card])
                    elif current_sum + card >= 17:
                        if current_sum + card == sum(player_hand):
                            tie_comb.append(current_comb + [card])
                        elif current_sum + card <= win_low or current_sum + card > 21:
                            combinations.append(current_comb + [card])
                j -= 1
                if j < 0:
                    break

    for i in range(len(combinations)):
        top = 1
        bottom = 1
        occurrences = collections.Counter(combinations[i])
        for card in occurrences:
            top *= factorial(shoe.cards_left(card), shoe.cards_left(card) - occurrences[card] + 1)

        bottom *= factorial(shoe.total, shoe.total - len(combinations[i]) + 1)
        prob = top / bottom

        win_odds += prob

    for i in range(len(tie_comb)):
        top = 1
        bottom = 1
        occurrences = collections.Counter(tie_comb[i])
        for card in occurrences:
            top *= factorial(shoe.cards_left(card), shoe.cards_left(card) - occurrences[card] + 1)

        bottom *= factorial(shoe.total, shoe.total - len(tie_comb[i]) + 1)
        prob = top / bottom

        tie_odds += prob
    #print(tie_odds)

    return 2 * win_odds + tie_odds - 1, win_odds, tie_odds


def hit_calc(player, dealer, shoe):
    if sum(player) <= 8:
        return 1, 1, 0
    #print('hit calc')
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    available = []
    win_prob = 0
    tie_prob = 0

    for card in cards:
        if sum(player) + card <= 21:
            available.append([card])

        elif card == 11 and sum(player) + 1 <= 21:
            available.append([1])

        elif 11 in player and sum(player) - (10 * player.count(11)) + card <= 21:
            available.append([card])

    start = -1
    for j in range(2):
        stop = len(available)
        start += 1
        for i in range(start, stop):
            comb = available[i]
            for card in cards:
                if sum(player) + sum(comb) + card <= 21:
                    available.append(comb + [card])

                elif card == 11 and sum(player) + sum(comb) + 1 <= 21:
                    available.append(comb + [1])

                elif 11 in player and sum(player) + sum(comb) - (10 * player.count(11)) + card <= 21:
                    available.append(comb + [card])
            start += 1

    #print(available)

    for cards in available:
        stand = stand_calc(player + cards, dealer, shoe)
        occurrences = collections.Counter(cards)
        card_prob = 1
        for card in occurrences:
            card_prob *= factorial(shoe.cards_left(card), shoe.cards_left(card) - occurrences[card] + 1)
        win_prob += card_prob * stand[1] / factorial(shoe.total, shoe.total - len(cards) + 1)
        tie_prob += card_prob * stand[2] / factorial(shoe.total, shoe.total - len(cards) + 1)

        #print(cards, card_prob / factorial(shoe.total, shoe.total - len(cards) + 1), '       ', stand[1], stand[2])
        #print('        ', card_prob * stand[1] / factorial(shoe.total, shoe.total - len(cards) + 1),
              #card_prob * stand[2] / factorial(shoe.total, shoe.total - len(cards) + 1))

    return 2 * win_prob + tie_prob - 1, win_prob, tie_prob


def double_check(player, dealer, shoe):
    #print('double calc')
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    available = []
    win_prob = 0
    tie_prob = 0
    for card in cards:
        if sum(player) + card <= 21:
            available.append([card])
        elif card == 11 and sum(player) + 1 <= 21:
            available.append([1])
        elif 11 in player and sum(player) - (10 * player.count(11)) + card <= 21:
            available.append([card])

    for cards in available:
        stand = stand_calc(player + cards, dealer, shoe)
        occurrences = collections.Counter(cards)
        win_top = 1
        tie_top = 1
        for card in occurrences:
            win_top *= factorial(shoe.cards_left(card), shoe.cards_left(card) - occurrences[card] + 1)
            tie_top *= factorial(shoe.cards_left(card), shoe.cards_left(card) - occurrences[card] + 1)
        win_prob += win_top * stand[1] / factorial(shoe.total, shoe.total - len(cards) + 1)
        tie_prob += tie_top * stand[2] / factorial(shoe.total, shoe.total - len(cards) + 1)
        #print(card, prob)
    #print(player, dealer, win_prob)
    return 2 * win_prob + tie_prob - 1


def factorial(a, b):
    while a > b:
        return a * factorial(a - 1, b)
    else:
        return b


def black_jack(n, decks):
    total_games = 0
    player_wins = 0
    games = 0
    player_bank = 1000
    avg_time = 0
    max_time = 0
    ties = 0
    for i in range(n):
        shoe = deck.Shoe(decks)
        while shoe.total > 52 * decks / 2:
            true_count = ((shoe.ten + shoe.one) - (shoe.two + shoe.three + shoe.four + shoe.five + shoe.six)) / \
                         (shoe.total / 52)
            if true_count > 1:
                bet = 5 + math.floor(.004 * player_bank * math.floor(true_count))
            elif true_count > -1:
                bet = 5
            else:
                bet = 1
            hand = new_hand(shoe)
            player = hand[0]
            dealer = hand[1]
            print(player_bank)
            true_count = ((shoe.ten + shoe.one) - (shoe.two + shoe.three + shoe.four + shoe.five + shoe.six)) / \
                         (shoe.total / 52)
            if true_count >= 2:

                if sum(player) == 21:
                    while sum(dealer) < 17:
                        draw = draw_card(shoe)
                        dealer.append(draw)
                        if sum(dealer) > 21 and 11 in dealer:
                            dealer = ace_change(dealer)
                    if dealer[0] + dealer[1] != 21:
                        games += 1
                        player_wins += 1
                        player_bank += 3 * bet / 2
                        print('win', player, dealer)
                        print(player_bank)
                        total_games += 1
                    else:
                        print('tie', player, dealer)
                        print(player_bank)
                        ties += 1
                        total_games += 1

                else:

                    start = time.time()

                    if player[0] == player[1] and calc_split(player, sum(dealer), shoe):
                        total_games += 1
                        player1 = [player[0], draw_card(shoe)]
                        player2 = [player[1], draw_card(shoe)]
                        print('split', player, dealer, player1, player2)
                        print(player_bank)

                        while stand_calc(player1, sum(dealer), shoe)[0] < hit_calc(player1, sum(dealer), shoe)[0]:
                            draw = draw_card(shoe)
                            player1.append(draw)
                            if sum(player1) > 21 and 11 in player1:
                                player1 = ace_change(player1)

                        while stand_calc(player2, sum(dealer), shoe)[0] < hit_calc(player2, sum(dealer), shoe)[0]:
                            draw = draw_card(shoe)
                            player2.append(draw)
                            if sum(player2) > 21 and 11 in player2:
                                player2 = ace_change(player2)

                        while sum(dealer) < 17:
                            draw = draw_card(shoe)
                            dealer.append(draw)
                            if sum(dealer) > 21 and 11 in dealer:
                                dealer = ace_change(dealer)

                        if sum(player1) < 22:
                            if sum(dealer) > 21:
                                print('      win', player1, dealer)
                                player_wins += 1
                                player_bank += bet
                                print(player_bank)
                                games += 1
                            elif sum(player1) > sum(dealer):
                                print('      win', player1, dealer)
                                player_wins += 1
                                player_bank += bet
                                print(player_bank)
                                games += 1
                            elif sum(player1) == sum(dealer) and dealer[0] + dealer[1] != 21:
                                print('      tie', player1, dealer)
                                print(player_bank)
                                ties += 1
                            else:
                                print('      lose', player1, dealer)
                                games += 1
                                player_bank -= bet
                        else:
                            print('      lose', player1, dealer)
                            games += 1
                            player_bank -= bet

                        if sum(player2) < 22:
                            if sum(dealer) > 21:
                                print('      win', player2, dealer)
                                player_wins += 1
                                player_bank += bet
                                print(player_bank)
                                games += 1
                            elif sum(player2) > sum(dealer):
                                print('      win', player2, dealer)
                                player_wins += 1
                                player_bank += bet
                                print(player_bank)
                                games += 1
                            elif sum(player2) == sum(dealer) and dealer[0] + dealer[1] != 21:
                                print('      tie', player2, dealer)
                                print(player_bank)
                                ties += 1
                            else:
                                print('      lose', player2, dealer)
                                games += 1
                                player_bank -= bet
                        else:
                            print('      lose', player2, dealer)
                            games += 1
                            player_bank -= bet

                    elif 2 * double_check(player, sum(dealer), shoe) > stand_calc(player, sum(dealer), shoe)[0] \
                            and 2 * double_check(player, sum(dealer), shoe) > hit_calc(player, sum(dealer), shoe)[0]:
                        draw = draw_card(shoe)
                        print('double', player, dealer)
                        player.append(draw)
                        print(player_bank)

                        if sum(player) > 21 and 11 in player:
                            player = ace_change(player)

                        while sum(dealer) < 17:
                            draw = draw_card(shoe)
                            dealer.append(draw)
                            if sum(dealer) > 21 and 11 in dealer:
                                dealer = ace_change(dealer)

                        if sum(player) < 22:
                            if sum(dealer) > 21:
                                print('      win', player, dealer)
                                player_wins += 1
                                player_bank += 2 * bet
                                print(player_bank)
                                games += 1
                            elif sum(player) > sum(dealer):
                                print('      win', player, dealer)
                                player_wins += 1
                                player_bank += 2 * bet
                                print(player_bank)
                                games += 1
                            elif sum(player) == sum(dealer) and dealer[0] + dealer[1] != 21:
                                print('      tie', player, dealer)
                                print(player_bank)
                                ties += 1
                            else:
                                print('      lose', player, dealer)
                                games += 1
                                player_bank -= 2 * bet
                        else:
                            print('      lose', player, dealer)
                            games += 1
                            player_bank -= 2 * bet

                    else:
                        while stand_calc(player, sum(dealer), shoe)[0] < hit_calc(player, sum(dealer), shoe)[0]:
                            draw = draw_card(shoe)
                            player.append(draw)
                            if sum(player) > 21 and 11 in player:
                                player = ace_change(player)
                        print('stand', player, dealer)
                        while sum(dealer) < 17:
                            draw = draw_card(shoe)
                            dealer.append(draw)
                            if sum(dealer) > 21 and 11 in dealer:
                                dealer = ace_change(dealer)

                        if sum(player) < 22:
                            if sum(dealer) > 21:
                                print('      win', player, dealer)
                                player_wins += 1
                                player_bank += bet
                                print(player_bank)
                                games += 1
                            elif sum(player) > sum(dealer):
                                print('      win', player, dealer)
                                player_wins += 1
                                player_bank += bet
                                print(player_bank)
                                games += 1
                            elif sum(player) == sum(dealer) and dealer[0] + dealer[1] != 21:
                                print('      tie', player, dealer)
                                print(player_bank)
                                ties += 1
                            else:
                                print('      lose', player, dealer)
                                games += 1
                                player_bank -= bet
                        else:
                            print('      lose', player, dealer)
                            games += 1
                            player_bank -= bet

                    total_games += 1
                    end_time = time.time()
                    avg_time = (avg_time * (total_games - 1) + end_time - start) / total_games
                    if end_time - start > max_time:
                        max_time = end_time - start
                        max_player = player
                        max_dealer = dealer

        print('current win percent', player_wins / total_games, '   current tie percent', ties / total_games,
              '   current loss percent', 1 - player_wins / total_games - ties / total_games, '   games', total_games)
        print('current bank', player_bank)
    print('total games', total_games)
    print('end bank', player_bank)
    print('end win rate', player_wins / games)
    print('avg time per hand', avg_time)
    print('max time for hand', max_time)
    print('max time hand', max_player, max_dealer)
    return (player_wins / games), player_bank


def calc_split(player_hand, dealer_card, shoe):
    if player_hand[0] == 11:
        return 1
    elif player_hand[0] == 8:
        return 1
    #print('split calc')
    stand = stand_calc(player_hand, dealer_card, shoe)[0]
    hit = hit_calc(player_hand, dealer_card, shoe)[0]
    if stand > hit:
        initial_odds = stand
    else:
        initial_odds = hit
    split_odds = 0
    split_tie = 0
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for card in cards:
        stand_odds = stand_calc([player_hand[0]] + [card], dealer_card, shoe)
        hit_odds = hit_calc([player_hand[0]] + [card], dealer_card, shoe)
        if stand_odds[1] > hit_odds[1]:
            split_odds += shoe.cards_left(card) * stand_odds[1] / shoe.total
            split_tie += shoe.cards_left(card) * stand_odds[2] / shoe.total
        else:
            split_odds += shoe.cards_left(card) * hit_odds[1] / shoe.total
            split_tie += shoe.cards_left(card) * hit_odds[2] / shoe.total
    if 2 * (2 * split_odds + split_tie - 1) > initial_odds:
        #print('split odds', 2 * split_odds)
        return 1
    else:
        return 0


def ace_change(arr):
    result = []
    first = 1
    for card in arr:
        if card == 11 and first == 1:
            result.append(1)
            first = 0
        else:
            result.append(card)
    return result


def strat_check(player, dealer, shoe):

    if 2 * double_check(player, dealer, shoe) > stand_calc(player, dealer, shoe)[0] \
            and 2 * double_check(player, dealer, shoe) > hit_calc(player, dealer, shoe)[0]:
        return 'double'
    elif stand_calc(player, dealer, shoe)[0] > hit_calc(player, dealer, shoe)[0]:
        return 'stand'
    else:
        return 'hit'


def adv_calc(shoe):
    win_prob = 0
    tie_prob = 0
    for i in range(2, 12):
        for k in range(2, 12):
            for j in range(2, 12):
                stand = stand_calc([i, k], j, shoe)
                hit = hit_calc([i, k], j, shoe)
                top = 1
                occurrences = collections.Counter([i, k, j])
                for card in occurrences:
                    top *= factorial(shoe.cards_left(card), shoe.cards_left(card) - occurrences[card] + 1)

                if stand[0] > hit[0]:
                    win_prob += top * stand[1] / factorial(shoe.total, shoe.total - 3 + 1)
                    tie_prob += top * stand[2] / factorial(shoe.total, shoe.total - 3 + 1)
                else:
                    win_prob += top * hit[1] / factorial(shoe.total, shoe.total - 3 + 1)
                    tie_prob += top * hit[2] / factorial(shoe.total, shoe.total - 3 + 1)
    return 2 * win_prob + tie_prob - 1, win_prob, tie_prob
