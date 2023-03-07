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


def get_pieces_array(piece_map: dict):
    w_rs = [-1] * 4
    w_rs_i = 0
    w_ns = [-1] * 4
    w_ns_i = 0
    w_bs = [-1] * 4
    w_bs_i = 0
    w_q = [-1] * 5
    w_q_i = 0
    w_k = [-1]
    w_ps = [-1] * 8
    w_ps_i = 0

    b_rs = [-1] * 4
    b_rs_i = 0
    b_ns = [-1] * 4
    b_ns_i = 0
    b_bs = [-1] * 4
    b_bs_i = 0
    b_q = [-1] * 5
    b_q_i = 0
    b_k = [-1]
    b_ps = [-1] * 8
    b_ps_i = 0

    for key in piece_map.keys():
        match str(piece_map[key]):
            case 'r':
                b_rs[b_rs_i] = key
                b_rs_i += 1
            case 'n':
                b_ns[b_ns_i] = key
                b_ns_i += 1
            case 'b':
                b_bs[b_bs_i] = key
                b_bs_i += 1
            case 'q':
                b_q[b_q_i] = key
                b_q_i += 1
            case 'k':
                b_k[0] = key
            case 'p':
                b_ps[b_ps_i] = key
                b_ps_i += 1
            case 'R':
                w_rs[w_rs_i] = key
                w_rs_i += 1
            case 'N':
                w_ns[w_ns_i] = key
                w_ns_i += 1
            case 'B':
                w_bs[w_bs_i] = key
                w_bs_i += 1
            case 'Q':
                w_q[w_q_i] = key
                w_q_i += 1
            case 'K':
                w_k[0] = key
            case 'P':
                w_ps[w_ps_i] = key
                w_ps_i += 1

    return w_rs + w_ns + w_bs + w_q + w_k + w_ps + b_rs + b_ns + b_bs + b_q + b_k + b_ps
