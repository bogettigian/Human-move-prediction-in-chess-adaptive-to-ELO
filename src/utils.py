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


def generate_columns(prefix: str):
    col_names = []

    for i in range(1, 65):
        col_names.append(str(i) + prefix)

    col_names.append('from_square' + prefix)
    col_names.append('to_square' + prefix)
    col_names.append('checkmate_count' + prefix)
    col_names.append('valuation' + prefix)
    col_names.append('delta_valuation' + prefix)

    return col_names


def columns():
    return [list(range(1, 65)) + generate_columns('_1b') + generate_columns('_2b') + generate_columns('_3b') + [
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
        'delta_valuation']]


def game_dict_to_array(game_dict: dict):
    data = []
    saved_records = 0

    game = dict_to_game(game_dict)
    board_game = game.board()

    move_3b = [0] * 69
    move_2b = [0] * 69
    move_1b = [0] * 69
    prev_val = 0

    for node in game.mainline():
        row = get_pieces_array(board_game.piece_map())
        row = row + move_1b + move_2b + move_3b

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

        row.append(int(game.headers['WhiteElo']) if board_game.turn else int(game.headers['BlackElo']))
        game_time, increase = game.headers['TimeControl'].split('+')
        row.append(game_time)
        row.append(increase)
        row.append(int(node.clock()) if node.clock() is not None else int(node.emt()))
        row.append(node.move.from_square)
        row.append(node.move.to_square)

        board_game.push(node.move)
        if board_game.is_checkmate() and not board_game.turn:
            row.append(0)
            if not board_game.turn:
                val = CHECKMATE_VAL
            else:
                val = - CHECKMATE_VAL
        elif node.eval() is not None:
            if node.eval().pov(not board_game.turn).is_mate():
                row.append(abs(node.eval().pov(not board_game.turn).mate()))
                if not board_game.turn:
                    val = CHECKMATE_VAL
                else:
                    val = - CHECKMATE_VAL
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

        move_1b = row[:64] + row[-5:]
        move_2b = move_1b
        move_3b = move_2b
        prev_val = val
        saved_records += 1
        data.append(row)

    return data, saved_records
