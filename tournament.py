import random
import sys

def simulate_tournament(C, T, p, allow_self_play=True):
    """
    Simulate the tournament for given parameters C, T, p, and allow_self_play flag.
    Returns scores_matrix, total_scores, winners.
    """
    def angel_strategy(round_num, my_history, opp_history):
        return 'C'
    
    def diablo_strategy(round_num, my_history, opp_history):
        return 'D'
    
    def tito_strategy(round_num, my_history, opp_history):
        if round_num == 1:
            return 'C'
        else:
            return opp_history[-1] if opp_history else 'C'
    
    def loco_strategy(round_num, my_history, opp_history):
        return 'C' if random.random() < 0.5 else 'D'
    
    def resentido_strategy(round_num, my_history, opp_history):
        if 'D' in opp_history:
            return 'D'
        return 'C'
    
    players = {
        'Angel': angel_strategy,
        'Diablo': diablo_strategy,
        'Tito': tito_strategy,
        'Loco': loco_strategy,
        'Resentido': resentido_strategy
    }

    player_list = list(players.keys())
    ROUNDS = 20

    scores_matrix = {pl: {opp: 0 for opp in player_list} for pl in player_list}

    def simulate_match(p1_name, p2_name, C, T, p):
        p1_strategy = players[p1_name]
        p2_strategy = players[p2_name]

        p1_history = []
        p2_history = []

        p1_score = 0
        p2_score = 0

        for r in range(1, ROUNDS+1):
            p1_action = p1_strategy(r, p1_history, p2_history)
            p2_action = p2_strategy(r, p2_history, p1_history)

            if random.random() < p:
                p1_action = 'C' if p1_action == 'D' else 'D'
            if random.random() < p:
                p2_action = 'C' if p2_action == 'D' else 'D'

            if p1_action == 'C' and p2_action == 'C':
                p1_score += C
                p2_score += C
            elif p1_action == 'D' and p2_action == 'D':
                p1_score += 0
                p2_score += 0
            elif p1_action == 'C' and p2_action == 'D':
                p2_score += T
            elif p1_action == 'D' and p2_action == 'C':
                p1_score += T

            p1_history.append(p1_action)
            p2_history.append(p2_action)

        return p1_score, p2_score

    for i in range(len(player_list)):
        for j in range(len(player_list)):
            # Skip self-play if allowed is turned off
            if not allow_self_play and player_list[i] == player_list[j]:
                continue

            p1_score, p2_score = simulate_match(player_list[i], player_list[j], C, T, p)
            scores_matrix[player_list[i]][player_list[j]] = p1_score

    total_scores = {pl: sum(scores_matrix[pl].values()) for pl in player_list}
    max_score = max(total_scores.values())
    winners = [pl for pl, sc in total_scores.items() if sc == max_score]

    return scores_matrix, total_scores, winners

if __name__ == '__main__':
    if len(sys.argv) > 1:
        C = float(sys.argv[1])
        T = float(sys.argv[2])
        p = float(sys.argv[3])
    else:
        # Default values for demonstration
        C = 1
        T = 2
        p = 0.0
    allow_self_play = True  # Set True to allow self-play by default
    simulations = 1000  # number of simulations to run

    players = ['Angel', 'Diablo', 'Tito', 'Loco', 'Resentido']
    # To accumulate results over multiple simulations
    accumulated_scores_matrix = {pl: {opp: 0 for opp in players} for pl in players}
    accumulated_total_scores = {pl: 0 for pl in players}

    # Run multiple simulations
    for _ in range(simulations):
        scores_matrix, total_scores, winners = simulate_tournament(C, T, p, allow_self_play)
        # Accumulate results
        for pl in players:
            for opp in players:
                accumulated_scores_matrix[pl][opp] += scores_matrix[pl][opp]
            accumulated_total_scores[pl] += total_scores[pl]

    # Compute averages
    avg_scores_matrix = {pl: {} for pl in players}
    for pl in players:
        for opp in players:
            avg_scores_matrix[pl][opp] = accumulated_scores_matrix[pl][opp] / simulations

    avg_total_scores = {pl: accumulated_total_scores[pl] / simulations for pl in players}

    # Determine winner(s) based on average total scores
    max_avg_score = max(avg_total_scores.values())
    avg_winners = [pl for pl, sc in avg_total_scores.items() if sc == max_avg_score]

    # Print results
    print(f"Parameters: C = {C}, T = {T}, p = {p}, allow_self_play = {allow_self_play}")
    print(f"Number of simulations: {simulations}")
    print("Average Final Payoff Matrix (rows: player, columns: opponent):")
    header = ["{:>10}".format("")] + ["{:>10}".format(p) for p in players]
    print("".join(header))
    for pl in players:
        row = ["{:>10}".format(pl)]
        for opp in players:
            row.append("{:>10.2f}".format(avg_scores_matrix[pl][opp]))
        print("".join(row))

    print("\nAverage Total scores (from highest to lowest):")
    sorted_avg_scores = sorted(avg_total_scores.items(), key=lambda x: x[1], reverse=True)
    for pl, score in sorted_avg_scores:
        print(f"{pl}: {score:.2f}")

    print("\nWinner(s) based on average results:", avg_winners)
    print("Winner details (average scores against others):")
    for w in avg_winners:
        print("Winner:", w)
        print("Scores against others:")
        for opp in players:
            if opp != w:
                print(f"  vs {opp}: {avg_scores_matrix[w][opp]:.2f}")

    # ADICIONAL: Encontrar la mayor y menor ganancia individual
    max_individual_score = -float('inf')
    min_individual_score = float('inf')
    max_player = None
    max_opponent = None
    min_player = None
    min_opponent = None

    for pl in players:
        for opp in players:
            if pl != opp:
                score = avg_scores_matrix[pl][opp]
                if score > max_individual_score:
                    max_individual_score = score
                    max_player = pl
                    max_opponent = opp
                if score < min_individual_score:
                    min_individual_score = score
                    min_player = pl
                    min_opponent = opp

    print(f"\nMaximum average individual gain: {max_individual_score:.2f} (Player: {max_player} vs {max_opponent})")
    print(f"Minimum average individual gain: {min_individual_score:.2f} (Player: {min_player} vs {min_opponent})")
