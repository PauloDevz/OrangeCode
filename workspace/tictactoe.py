"""Jogo da Velha (Tic-Tac-Toe) - versão simples para linha de comando.

Execute o script e siga as instruções para jogar contra outro jogador humano.

O tabuleiro é numerado da seguinte forma:

 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9

Digite o número da posição onde deseja colocar seu símbolo (X ou O).
"""

def print_board(board):
    """Exibe o tabuleiro atual.
    board: lista de 9 strings (' ', 'X' ou 'O').
    """
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")


def check_winner(board):
    """Retorna 'X' ou 'O' se houver vencedor, ou None caso contrário."""
    linhas = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
              (0, 3, 6), (1, 4, 7), (2, 5, 8),
              (0, 4, 8), (2, 4, 6)]
    for a, b, c in linhas:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None


def is_full(board):
    return all(cell != " " for cell in board)


def get_move(board, player):
    while True:
        try:
            move = input(f"Jogador {player} (digite 1-9): ")
            pos = int(move) - 1
            if pos < 0 or pos > 8:
                print("Posição inválida. Use números de 1 a 9.")
                continue
            if board[pos] != " ":
                print("Posição já ocupada. Escolha outra.")
                continue
            return pos
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")


def main():
    board = [" "] * 9
    current_player = "X"
    while True:
        print_board(board)
        pos = get_move(board, current_player)
        board[pos] = current_player
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Parabéns! Jogador {winner} venceu!")
            break
        if is_full(board):
            print_board(board)
            print("Empate! O tabuleiro está cheio.")
            break
        # Troca de jogador
        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    main()
