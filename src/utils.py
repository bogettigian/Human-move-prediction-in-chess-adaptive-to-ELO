import chess.pgn


def valid_game(game: chess.pgn.Game):
    if game.headers.get('BlackElo') is None:
        return False
    if game.headers.get('WhiteElo') is None:
        return False
    for node in game.mainline():
        if node.eval() is None:
            return False
        if node.clock() is None and node.emt() is None:
            return False
        return True
    return False


def game_to_dict(game: chess.pgn.Game):
    game_dict = game.headers.__dict__
    moves = []
    board = game.board()
    for node in game.mainline():
        moves.append(
            {'move': node.move.__str__(), 'info': node.__dict__['move'].__dict__, 'comment': node.__dict__['comment']})
        board.push(node.move)
    game_dict['moves'] = moves
    return game_dict


def dict_to_game(game_dict: dict):
    headers = chess.pgn.Headers()
    headers._tag_roster = game_dict['_tag_roster']
    headers._others = game_dict['_others']

    game = chess.pgn.Game(headers)
    mainline = game.game()

    for move_dict in game_dict['moves']:
        move = chess.Move(
            move_dict['info']['from_square'],
            move_dict['info']['to_square'],
            move_dict['info']['promotion'],
            move_dict['info']['drop'])

        mainline.add_main_variation(move, comment=move_dict['comment'])
        mainline = mainline.next()

    return mainline.game()
