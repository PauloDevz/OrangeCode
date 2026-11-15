import sys

# Simple console chess representation
# Board is 8x8 list of strings. Uppercase = White, lowercase = Black, '.' = empty

def create_board():
    # Starting position
    board = [
        list('rnbqkbnr'),
        list('pppppppp'),
        list('........'),
        list('........'),
        list('........'),
        list('........'),
        list('PPPPPPPP'),
        list('RNBQKBNR'),
    ]
    return board

def print_board(board):
    print('  a b c d e f g h')
    for i, row in enumerate(board):
        rank = 8 - i
        print(f"{rank} " + ' '.join(row) + f" {rank}")
    print('  a b c d e f g h')

def algebraic_to_index(pos):
    # pos like 'e2'
    if len(pos) != 2:
        raise ValueError('Invalid position')
    file = pos[0].lower()
    rank = pos[1]
    if file < 'a' or file > 'h' or rank < '1' or rank > '8':
        raise ValueError('Invalid position')
    col = ord(file) - ord('a')
    row = 8 - int(rank)
    return row, col

def move_piece(board, src, dst):
    src_row, src_col = algebraic_to_index(src)
    dst_row, dst_col = algebraic_to_index(dst)
    piece = board[src_row][src_col]
    if piece == '.':
        raise ValueError('No piece at source')
    # Simple move without rule checking
    board[dst_row][dst_col] = piece
    board[src_row][src_col] = '.'
    return board

def main():
    board = create_board()
    print('Simple Chess (no rule enforcement)')
    print_board(board)
    while True:
        try:
            move = input('Enter move (e.g., e2e4) or "quit": ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting.')
            break
        if move.lower() in ('quit', 'exit'):
            print('Good bye!')
            break
        if len(move) != 4:
            print('Invalid format. Use e2e4.')
            continue
        src = move[:2]
        dst = move[2:]
        try:
            board = move_piece(board, src, dst)
            print_board(board)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    main()
