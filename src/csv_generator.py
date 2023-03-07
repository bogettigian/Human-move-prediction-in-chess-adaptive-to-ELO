import argparse
import os
import time
import chess
import pandas as pd

import database
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess CSV generator script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--connection_string',
                        default='mongodb://localhost:27017', help="Connection string")
    parser.add_argument('-d', '--database', default='chess_base', help="Database name")
    parser.add_argument('-t', '--collection', default='moves', help="Collection name")
    parser.add_argument('-p', '--path', default='./../data/csv/data.csv', help="Data output")
    args = vars(parser.parse_args())

    connection_string = args['connection_string']
    database_name = args['database']
    collection_name = args['collection']
    path = args['path']

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    collection = database.get_database(connection_string, database_name, collection_name)

    start_time = time.time()
    total_records = 0
    saved_records = 0

    columns = list(range(1, 65)) + [
        'active_color',
        'castling_K',
        'castling_Q',
        'castling_k',
        'castling_q',
        'en_passant',
        'half-move_clock',
        'threefold',
        'move_number',
        'elo',
        'game_time',
        'increase',
        'time_left',
        'from_square',
        'to_square',
        'checkmate_count',
        'valuation',
        'delta_valuation']

    filter = {}
    result = collection.find(filter).limit(100)

    data = []
    for game_dict in result:
        game = utils.dict_to_game(game_dict)
        board_game = game.board()
        total_records += 1
        prev_val = 0

        for node in game.mainline():
            row = utils.get_pieces_array(board_game.piece_map())

            row.append(int(board_game.turn))
            row.append(int(board_game.has_kingside_castling_rights(chess.WHITE)))
            row.append(int(board_game.has_queenside_castling_rights(chess.WHITE)))
            row.append(int(board_game.has_kingside_castling_rights(chess.BLACK)))
            row.append(int(board_game.has_kingside_castling_rights(chess.BLACK)))
            row.append(0 if not board_game.has_legal_en_passant() else
                       chess.parse_square((board_game.fen().split()[3])))
            row.append(board_game.halfmove_clock)
            row.append(int(board_game.can_claim_threefold_repetition()))
            row.append(board_game.fullmove_number)

            row.append(game.headers['WhiteElo'] if board_game.turn else game.headers['BlackElo'])
            game_time, increase = game.headers['TimeControl'].split('+')
            row.append(game_time)
            row.append(increase)
            row.append(node.clock() if node.clock() is not None else node.emt())
            row.append(node.move.from_square)
            row.append(node.move.to_square)

            board_game.push(node.move)
            if board_game.is_checkmate() and not board_game.turn:
                row.append(0)
                if not board_game.turn:
                    val = utils.CHECKMATE_VAL
                else:
                    val = - utils.CHECKMATE_VAL
            elif node.eval() is not None:
                if node.eval().pov(not board_game.turn).is_mate():
                    row.append(abs(node.eval().pov(not board_game.turn).mate()))
                    if not board_game.turn:
                        val = utils.CHECKMATE_VAL
                    else:
                        val = - utils.CHECKMATE_VAL
                else:
                    row.append(-1)
                    val = node.eval().pov(not board_game.turn).score()
            else:
                # The following movements are not analyzed.
                break

            row.append(val)
            if not board_game.turn:
                row.append(val - prev_val)
            else:
                row.append((val - prev_val) * -1)

            prev_val = val
            saved_records += 1
            data.append(row)

    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv(path)

    print(f'Total games read: {total_records}')
    print(f'Total games saved: {saved_records}')
    print(f'Time taken in seconds: {time.time() - start_time}')
