import argparse
import pandas as pd
from sklearn import metrics


def split_in_matches(data):
    data.reset_index(drop=True)
    df_result = []
    init = 0
    for index in data.index:
        if data.iloc[index]['is_end']:
            if index > init + 10:
                df_result.append(data.iloc[init:index + 1])
            init = index + 1
    return df_result


def move_play_time(data, time):
    for index in data.index:
        if data.iloc[index]['time'] < time:
            return index
    return index


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess result generator script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--validation_path', default='./../data/validation/', help="Validation path")
    parser.add_argument('-o', '--output_path', default='./../data/validation/', help="Output path")
    parser.add_argument('-f', '--file_names', action='append', required=True, help="File names")
    args = vars(parser.parse_args())

    names = args['file_names']
    files = []

    for file_name in names:
        files.append(f'results_{args["validation_path"]}{file_name}.csv')

    for i in range(len(files)):
        df = pd.read_csv(files[i])
        df['model'] = names[i]

        result_df = split_in_matches(df)

        f1_results = []
        acc_results = []
        elo = []
        model = []
        for game in result_df:
            game = game.reset_index(drop=True)
            end = move_play_time(game, 30.0)
            f1_results.append(metrics.f1_score(game['real'][10:end+1], game['predicted'][10:end+1], average='weighted'))
            acc_results.append(metrics.f1_score(game['real'][10:end+1], game['predicted'][10:end+1], average='micro'))
            elo.append((game.iloc[0]['white_elo'] + game.iloc[0]['black_elo']) / 2)
            model.append(game.iloc[0]['model'])

        metric_df = pd.DataFrame({'accuracy': acc_results, 'f1_weighted': f1_results, 'elo': elo, 'model': model})
        metric_df.to_csv(f'{args["validation_path"]}metrics_{names[i]}.csv')
