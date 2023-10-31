import argparse
import os
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess Chunk generator script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--pgn_path', default='./../data/pgn/data.pgn', help="Data input")
    parser.add_argument('-c', '--chunk_path', default='./../data/chunk', help="Data output")
    parser.add_argument('-t', '--test_size', default=0.20, help="Data output")
    args = vars(parser.parse_args())

    pgn_path = args['pgn_path']
    chunk_path = args['chunk_path']
    test_size = args['test_size']

    chunk_train_path = chunk_path + '/train'
    chunk_test_path = chunk_path + '/test'

    if not os.path.exists(os.path.dirname(pgn_path)):
        raise Exception('PGN path does not exist')
    if not os.path.exists(chunk_train_path):
        os.makedirs(chunk_train_path)
    if not os.path.exists(chunk_test_path):
        os.makedirs(chunk_test_path)

    start_time = time.time()

    work_dir = os.getcwd()
    os.chdir(chunk_train_path)

    result = os.system(f'trainingdata-tool -v -files-per-dir 5000 ./../../../src/{pgn_path}')
    if result != 0:
        raise Exception('Error: trainingdata-tool call failed')

    os.chdir(work_dir)

    for folder in os.listdir(chunk_train_path):
        if os.path.isdir(chunk_train_path + '/' + folder):
            for file in os.listdir(chunk_train_path + '/' + folder):
                os.rename(chunk_train_path + '/' + folder + '/' + file, chunk_train_path + '/' + file)
            os.rmdir(chunk_train_path + '/' + folder)

    files_to_move = int(len(os.listdir(chunk_train_path)) * test_size)
    for file in os.listdir(chunk_train_path)[:files_to_move]:
        os.rename(chunk_train_path + '/' + file, chunk_test_path + '/' + file)

    print(f'Train chunks files: {len(os.listdir(chunk_train_path))}')
    print(f'Test chunks files: {len(os.listdir(chunk_test_path))}')
    print(f'Time taken in seconds: {time.time() - start_time}')
