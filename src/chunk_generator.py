import argparse
import os
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess Chunk generator script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--pgn_path', default='./../data/pgn/data.pgn', help="Data output")
    parser.add_argument('-c', '--chunk_path', default='./../data/chunk', help="Data output")
    parser.add_argument('-t', '--test_size', default=0.20, help="Data output")
    args = vars(parser.parse_args())

    pgn_path = args['pgn_path']
    chunk_path = args['chunk_path']
    test_size = args['test_size']

    if not os.path.exists(os.path.dirname(pgn_path)):
        raise Exception('PGN path does not exist')
    if not os.path.exists(os.path.dirname(chunk_path + '/train')):
        os.makedirs(os.path.dirname(chunk_path + '/train'))
    if not os.path.exists(os.path.dirname(chunk_path + '/test')):
        os.makedirs(os.path.dirname(chunk_path + '/test'))

    start_time = time.time()

    work_dir = os.getcwd()
    os.chdir(chunk_path + '/train')
    training_data_tool_dir = './../../src/../libs/trainingdata-tool/trainingdata-tool'

    result = os.system(f'{training_data_tool_dir} -v -files-per-dir 5000 ./../../src/{pgn_path}')
    if result != 0:
        raise Exception('Error: trainingdata-tool call failed')

    os.chdir(work_dir)

    files_to_move = int(len(os.listdir(chunk_path + '/train')) * test_size)
    for file in os.listdir(chunk_path + '/train')[:files_to_move]:
        os.rename(chunk_path + '/train' + file, chunk_path + '/test' + file)

    print(f'Train chunks files: {len(os.listdir(chunk_path + "/train"))}')
    print(f'Test chunks files: {len(os.listdir(chunk_path + "/train"))}')
    print(f'Time taken in seconds: {time.time() - start_time}')
