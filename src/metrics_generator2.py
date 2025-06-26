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
    for index, row in data.iterrows():
        if row['clock'] < time:
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
        files.append(f'{args["validation_path"]}results_{file_name}.csv')

    for i in range(len(files)):
        df = pd.read_csv(files[i])

        result_df = split_in_matches(df)

        f1_results = []
        acc_results = []
        elo = []
        model = []
        new_df = None
        for game in result_df:
            game = game.reset_index(drop=True)
            end = move_play_time(game, 30.0)
            if new_df is None:
                new_df = game[10:end+1]
            else:
                new_df = pd.concat([new_df, game[10:end+1]])

        fixed_elos = []
        for index, row in new_df.iterrows():
            e = row['white_elo'] if not row['turn'] else row['black_elo']
            fixed_elos.append((e // 10) * 10)
        new_df['fixed_elo'] = fixed_elos

        for e in list(new_df['fixed_elo'].unique()):
            filtered_df = new_df[new_df['fixed_elo'] == e]
            f1_results.append(metrics.f1_score(filtered_df['real'], filtered_df['predicted'], average='weighted'))
            acc_results.append(metrics.f1_score(filtered_df['real'], filtered_df['predicted'], average='micro'))
            elo.append(e)
            model.append(names[i])

        metric_df = pd.DataFrame({'accuracy': acc_results, 'f1_weighted': f1_results, 'elo': elo, 'model': model})
        metric_df.to_csv(f'{args["validation_path"]}metrics2_{names[i]}.csv')
