import argparse
import os
import time
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

    # columns = ['board', 'color', 'elo', 'time', 'time_left', 'castling', 'en_passant',
    # 'from_square', 'to_square', 'valuation']
    columns = ['board', 'elo', 'time', 'time_left', 'from_square', 'to_square', 'valuation']
    data = []

    filter = {}
    result = collection.find(filter)
    for game_dict in result:
        game = utils.dict_to_game(game_dict)
        board_game = game.board()
        is_white_turn = True
        total_records += 1

        for node in game.mainline():
            row = []

            row.append(board_game.fen())
            # row.append('White' if is_white_turn else 'Black')
            row.append(game.headers['WhiteElo'] if is_white_turn else game.headers['BlackElo'])
            row.append(game.headers['TimeControl'])
            row.append(node.clock() if node.clock() is not None else node.emt())
            # row.append(board_game.has_castling_rights(is_white_turn))
            # row.append(board_game.has_legal_en_passant())
            row.append(node.move.from_square)
            row.append(node.move.to_square)

            board_game.push(node.move)
            if board_game.is_checkmate():
                row.append('+1000')
            elif node.eval() is not None:
                row.append(node.eval().pov(is_white_turn))
            else:
                # The following movements are not analyzed.
                break

            is_white_turn = not is_white_turn
            saved_records += 1
            data.append(row)

    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv(path)

    print(f'Total games read: {total_records}')
    print(f'Total games saved: {saved_records}')
    print(f'Time taken in seconds: {time.time() - start_time}')
