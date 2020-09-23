import os
import numpy as np

if 'AI' in os.getcwd():
    from src.utils import *
else:
    from AI2019.src.utils import *


class TwoOpt:

    @staticmethod
    def step2opt(solution, matrix_dist, distance):
        seq_length = len(solution) - 1
        tsp_sequence = np.array(solution)
        uncrosses = 0
        for i in range(1, seq_length):
            for j in range(i + 1, seq_length):
                new_tsp_sequence = TwoOpt.swap2opt(tsp_sequence, i, j)
                new_distance = distance + TwoOpt.gain(i, j, tsp_sequence, matrix_dist)
                if new_distance < distance:
                    uncrosses += 1
                    tsp_sequence = np.copy(new_tsp_sequence)
                    distance = new_distance
        return tsp_sequence, distance, uncrosses

    @staticmethod
    def swap2opt(tsp_sequence, i, j):
        new_tsp_sequence = np.copy(tsp_sequence)
        new_tsp_sequence[i:j + 1] = np.flip(tsp_sequence[i:j + 1], axis=0)  # flip or swap ?
        return new_tsp_sequence

    @staticmethod
    def gain(i, j, tsp_sequence, matrix_dist):
        old_link_len = (matrix_dist[tsp_sequence[i], tsp_sequence[i - 1]] + matrix_dist[
            tsp_sequence[j], tsp_sequence[j + 1]])
        changed_links_len = (matrix_dist[tsp_sequence[j], tsp_sequence[i - 1]] + matrix_dist[
            tsp_sequence[i], tsp_sequence[j + 1]])
        return - old_link_len + changed_links_len

    @staticmethod
    def loop2opt(solution, instance, max_num_of_uncrosses=10000):
        matrix_dist = instance.dist_matrix
        new_len = compute_lenght(solution, matrix_dist)
        new_tsp_sequence = np.copy(np.array(solution))
        uncross = 0
        while uncross < max_num_of_uncrosses:
            new_tsp_sequence, new_reward, uncr_ = TwoOpt.step2opt(new_tsp_sequence, matrix_dist, new_len)
            uncross += uncr_
            if new_reward < new_len:
                new_len = new_reward
            else:
                return new_tsp_sequence.tolist()

        # return new_tsp_sequence.tolist(), new_len, uncross
        return new_tsp_sequence.tolist()


class TwoDotFiveOpt:

    @staticmethod
    def step2dot5opt(solution, matrix_dist, distance):
        seq_length = len(solution) - 2
        tsp_sequence = np.array(solution)
        uncrosses = 0
        for i in range(1, seq_length - 1):
            for j in range(i + 1, seq_length):
                # 2opt swap
                twoOpt_tsp_sequence = TwoOpt.swap2opt(tsp_sequence, i, j)
                twoOpt_len = distance + TwoOpt.gain(i, j, tsp_sequence, matrix_dist)
                # node shift 1
                first_shift_tsp_sequence = TwoDotFiveOpt.shift1(tsp_sequence, i, j)
                first_shift_len = distance + TwoDotFiveOpt.shift_gain1(i, j, tsp_sequence, matrix_dist)
                # node shift 2
                second_shift_tsp_sequence = TwoDotFiveOpt.shift2(tsp_sequence, i, j)
                second_shift_len = distance + TwoDotFiveOpt.shift_gain2(i, j, tsp_sequence, matrix_dist)

                best_len, best_method = min([twoOpt_len, first_shift_len, second_shift_len]), np.argmin(
                    [twoOpt_len, first_shift_len, second_shift_len])
                sequences = [twoOpt_tsp_sequence, first_shift_tsp_sequence, second_shift_tsp_sequence]
                if best_len < distance:
                    uncrosses += 1
                    tsp_sequence = sequences[best_method]
                    distance = best_len
                    # print(distance, best_method, [twoOpt_len, first_shift_len, second_shift_len])
        return tsp_sequence, distance, uncrosses

    @staticmethod
    def shift1(tsp_sequence, i, j):
        new_tsp_sequence = np.concatenate(
            [tsp_sequence[:i], tsp_sequence[i + 1: j + 1], [tsp_sequence[i]], tsp_sequence[j + 1:]])
        return new_tsp_sequence

    @staticmethod
    def shift_gain1(i, j, tsp_sequence, matrix_dist):
        old_link_len = (matrix_dist[tsp_sequence[i], tsp_sequence[i - 1]] +
                        matrix_dist[tsp_sequence[i], tsp_sequence[i + 1]] +
                        matrix_dist[tsp_sequence[j], tsp_sequence[j + 1]])
        changed_links_len = (matrix_dist[tsp_sequence[i - 1], tsp_sequence[i + 1]] +
                             matrix_dist[tsp_sequence[i], tsp_sequence[j]]
                             + matrix_dist[tsp_sequence[i], tsp_sequence[j + 1]])
        return - old_link_len + changed_links_len

    @staticmethod
    def shift2(tsp_sequence, i, j):
        new_tsp_sequence = np.concatenate(
            [tsp_sequence[:i], [tsp_sequence[j]], tsp_sequence[i: j], tsp_sequence[j + 1:]])
        return new_tsp_sequence

    @staticmethod
    def shift_gain2(i, j, tsp_sequence, matrix_dist):
        old_link_len = (matrix_dist[tsp_sequence[i], tsp_sequence[i - 1]] + matrix_dist[
            tsp_sequence[j], tsp_sequence[j - 1]] + matrix_dist[tsp_sequence[j], tsp_sequence[j + 1]])
        changed_links_len = (
                matrix_dist[tsp_sequence[j], tsp_sequence[i - 1]] + matrix_dist[tsp_sequence[i], tsp_sequence[j]] +
                matrix_dist[tsp_sequence[j - 1], tsp_sequence[j + 1]])
        return - old_link_len + changed_links_len

    @staticmethod
    def loop2dot5opt(solution, instance, max_num_of_changes=10000):
        matrix_dist = instance.dist_matrix
        actual_len = compute_lenght(solution, matrix_dist)
        new_tsp_sequence = np.copy(np.array(solution))
        uncross = 0
        while uncross < max_num_of_changes:
            new_tsp_sequence, new_len, uncr_ = TwoDotFiveOpt.step2dot5opt(new_tsp_sequence, matrix_dist, actual_len)
            uncross += uncr_
            # print(new_len, uncross)
            if new_len < actual_len:
                actual_len = new_len
            else:
                return new_tsp_sequence.tolist()

        return new_tsp_sequence.tolist()