import chess.pgn


CHECKMATE_VAL = 999999


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


def get_pieces_array(piece_map: dict):
    board = [0] * 64

    for key in piece_map.keys():
        match str(piece_map[key]):
            case 'r':
                board[key] = - chess.ROOK
            case 'n':
                board[key] = - chess.KNIGHT
            case 'b':
                board[key] = - chess.BISHOP
            case 'q':
                board[key] = - chess.QUEEN
            case 'k':
                board[key] = - chess.KING
            case 'p':
                board[key] = - chess.PAWN
            case 'R':
                board[key] = chess.ROOK
            case 'N':
                board[key] = chess.KNIGHT
            case 'B':
                board[key] = chess.BISHOP
            case 'Q':
                board[key] = chess.QUEEN
            case 'K':
                board[key] = chess.KING
            case 'P':
                board[key] = chess.PAWN

    return board
