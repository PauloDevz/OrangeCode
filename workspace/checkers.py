import sys

# Simple console checkers (draughts) implementation with basic capture rules
# Board is 8x8 list of strings. '.' = empty
# 'b' = black man, 'B' = black king, 'r' = red man, 'R' = red king

def create_board():
    board = [['.' for _ in range(8)] for _ in range(8)]
    # Place black pieces on rows 0,1,2 on dark squares (col+row odd)
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = 'b'
    # Place red pieces on rows 5,6,7 on dark squares
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = 'r'
    return board

def print_board(board):
    print('  a b c d e f g h')
    for i, row in enumerate(board):
        rank = 8 - i
        line = f"{rank} " + ' '.join(row) + f" {rank}"
        print(line)
    print('  a b c d e f g h')

def algebraic_to_index(pos):
    if len(pos) != 2:
        raise ValueError('Invalid position')
    file = pos[0].lower()
    rank = pos[1]
    if file < 'a' or file > 'h' or rank < '1' or rank > '8':
        raise ValueError('Invalid position')
    col = ord(file) - ord('a')
    row = 8 - int(rank)
    return row, col

def opponent(piece):
    if piece.lower() == 'b':
        return ('r', 'R')
    if piece.lower() == 'r':
        return ('b', 'B')
    return ()

def is_king(piece):
    return piece.isupper()

def possible_captures(board, player):
    caps = []
    dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece.lower() != player:
                continue
            for dr, dc in dirs:
                # Men move forward only unless king
                if not is_king(piece):
                    if player == 'b' and dr < 0:
                        continue
                    if player == 'r' and dr > 0:
                        continue
                r_mid, c_mid = r + dr, c + dc
                r_dst, c_dst = r + 2*dr, c + 2*dc
                if 0 <= r_mid < 8 and 0 <= c_mid < 8 and 0 <= r_dst < 8 and 0 <= c_dst < 8:
                    if board[r_mid][c_mid] in opponent(piece) and board[r_dst][c_dst] == '.':
                        caps.append(((r, c), (r_dst, c_dst)))
    return caps

def move_piece(board, src, dst, player, forced_capture):
    src_row, src_col = algebraic_to_index(src)
    dst_row, dst_col = algebraic_to_index(dst)
    piece = board[src_row][src_col]
    if piece == '.':
        raise ValueError('No piece at source')
    if piece.lower() != player:
        raise ValueError('Not your piece')
    dr = dst_row - src_row
    dc = dst_col - src_col
    if abs(dr) != abs(dc):
        raise ValueError('Move must be diagonal')
    if board[dst_row][dst_col] != '.':
        raise ValueError('Destination not empty')
    # Simple move
    if abs(dr) == 1:
        if forced_capture:
            raise ValueError('Capture available, you must capture')
        # Men can only move forward
        if not is_king(piece):
            if player == 'b' and dr != 1:
                raise ValueError('Black men must move forward')
            if player == 'r' and dr != -1:
                raise ValueError('Red men must move forward')
        board[dst_row][dst_col] = piece
        board[src_row][src_col] = '.'
    # Capture move
    elif abs(dr) == 2:
        r_mid = src_row + dr // 2
        c_mid = src_col + dc // 2
        mid_piece = board[r_mid][c_mid]
        if mid_piece not in opponent(piece):
            raise ValueError('No opponent piece to capture')
        # Men capture forward only unless king
        if not is_king(piece):
            if player == 'b' and dr != 2:
                raise ValueError('Black men capture forward')
            if player == 'r' and dr != -2:
                raise ValueError('Red men capture forward')
        board[dst_row][dst_col] = piece
        board[src_row][src_col] = '.'
        board[r_mid][c_mid] = '.'
    else:
        raise ValueError('Invalid move distance')
    # Promotion
    if piece == 'b' and dst_row == 7:
        board[dst_row][dst_col] = 'B'
    if piece == 'r' and dst_row == 0:
        board[dst_row][dst_col] = 'R'
    return board

def main():
    board = create_board()
    player = 'b'  # black starts
    print('Checkers with basic capture rules')
    print_board(board)
    while True:
        caps = possible_captures(board, player)
        forced = len(caps) > 0
        if forced:
            print(f'Player {player.upper()} must capture')
        try:
            move = input(f"Player {player.upper()} move (e.g., b6a5) or 'quit': ").strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting.')
            break
        if move.lower() in ('quit', 'exit'):
            print('Good bye!')
            break
        if len(move) != 4:
            print('Invalid format. Use b6a5.')
            continue
        src = move[:2]
        dst = move[2:]
        try:
            board = move_piece(board, src, dst, player, forced)
            print_board(board)
            # Switch player after a successful move
            player = 'r' if player == 'b' else 'b'
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    main()
