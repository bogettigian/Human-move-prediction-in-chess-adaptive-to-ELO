import argparse
import json
import os
import time
import chess.engine
import numpy as np

import database
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess CSV generator script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--connection_string', default='mongodb://localhost:27017', help="Connection string")
    parser.add_argument('-d', '--database', default='chess-mongo', help="Database name")
    parser.add_argument('-t', '--collection', default='moves', help="Collection name")
    parser.add_argument('-p', '--path', default='./../data/validation/data.csv', help="Data output")

    parser.add_argument('-e', '--engine', default='./../libs/trainingdata-tool/lc0/build/lc0', help="Engine")
    parser.add_argument('-w', '--weights', default='./../data/model/mymodel.pb.gz', help="Engine weights")
    parser.add_argument('-q', '--static_elo', default=True, type=bool, help="Static elo")
    parser.add_argument('-o', '--elo', default='1000', help="Engine elo")

    parser.add_argument('-f', '--filter', default='{}', type=json.loads, help="Database query filter")
    parser.add_argument('-s', '--skip', default=0, type=int, help="Database query skip")
    parser.add_argument('-l', '--limit', default=0, type=int, help="Database query limit")
    args = vars(parser.parse_args())

    connection_string = args['connection_string']
    database_name = args['database']
    collection_name = args['collection']
    path = args['path']

    engine_path = args['engine']
    weights = args['weights']
    static_elo = args['static_elo']
    elo = args['elo']

    db_filter = args['filter']
    db_skip = args['skip']
    db_limit = args['limit']

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    num_retry = 5
    start_time = time.time()
    total_records = 0
    saved_records = 0

    collection = database.get_database(connection_string, database_name, collection_name)
    with open(path, 'w') as f:
        np.savetxt(f, [
            ['fen', 'white_elo', 'black_elo', 'real', 'predicted', 'turn', 'time', 'total_time', 'eval', 'is_end']],
                   delimiter=',', fmt='%s')

    if static_elo:
        engine = chess.engine.SimpleEngine.popen_uci([engine_path, f'--weights={weights}', f'--elo={elo}'])

    for game_dict in collection.find(db_filter).sort('$natural', 1).skip(db_skip).limit(db_limit):
        game = utils.dict_to_game(game_dict)
        board_game = game.board()

        if not static_elo:
            withe_engine = chess.engine.SimpleEngine.popen_uci(
                [engine_path, f'--weights={weights}', f'--elo={game.headers.get("WhiteElo")}'])
            black_engine = chess.engine.SimpleEngine.popen_uci(
                [engine_path, f'--weights={weights}', f'--elo={game.headers.get("BlackElo")}'])

        records = []
        for node in game.mainline():
            for i in range(num_retry):
                if static_elo:
                    try:
                        result = engine.play(board_game, chess.engine.Limit(depth=1))
                        break
                    except Exception as ex:
                        engine = chess.engine.SimpleEngine.popen_uci(
                            [engine_path, f'--weights={weights}', f'--elo={elo}'])
                elif not static_elo and board_game.turn == chess.WHITE:
                    try:
                        result = withe_engine.play(board_game, chess.engine.Limit(depth=1))
                        break
                    except Exception as ex:
                        withe_engine = chess.engine.SimpleEngine.popen_uci(
                            [engine_path, f'--weights={weights}', f'--elo={game.headers.get("WhiteElo")}'])
                else:
                    try:
                        result = black_engine.play(board_game, chess.engine.Limit(depth=1))
                        break
                    except Exception as ex:
                        black_engine = chess.engine.SimpleEngine.popen_uci(
                            [engine_path, f'--weights={weights}', f'--elo={game.headers.get("BlackElo")}'])

            if result is None:
                raise ex

            eval_escore = '#'
            if node.eval() is not None and node.eval().is_mate():
                eval_escore = f'#{node.eval().pov(node.turn()).mate()}'
            elif node.eval() is not None and not node.eval().is_mate():
                eval_escore = f'{node.eval().pov(node.turn()).score()}'

            records.append([
                board_game.fen(),
                game.headers.get("WhiteElo"),
                game.headers.get("BlackElo"),
                node.move,
                result.move,
                node.turn(),
                node.clock(),
                game.headers.get("TimeControl"),
                eval_escore,
                node.is_end()
            ])
            board_game.push(node.move)
            saved_records += 1

        if not static_elo:
            withe_engine.quit()
            black_engine.quit()

        with open(path, 'a') as f:
            np.savetxt(f, records, delimiter=',', fmt='%s')
        total_records += 1

    if static_elo:
        engine.quit()

    print(f'Total games read: {total_records}')
    print(f'Total moves saved: {saved_records}')
    print(f'Time taken in seconds: {time.time() - start_time}')
