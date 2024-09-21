import socket
from random import choice
from time import sleep
import play_game as zero

class AlphaHexAgent():

    HOST = "127.0.0.1"
    PORT = 1234

    def __init__(self, board_size=11):
        self.s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        self.s.connect((self.HOST, self.PORT))

        self.board_size = board_size
        self.board = []
        self.colour = ""
        self.turn_count = 0
        
        self.game_ZERO = zero.start_game()
        self.game_ZERO.respond("boardsize 11")
        

    def run(self):
        """Reads data until it receives an END message or the socket closes."""

        while True:
            data = self.s.recv(1024)
            if not data:
                break
            # print(f"{self.colour} {data.decode('utf-8')}", end="")
            if (self.interpret_data(data)):
                break

        # print(f"Naive agent {self.colour} terminated")

    def interpret_data(self, data):
        """Checks the type of message and responds accordingly. Returns True
        if the game ended, False otherwise.
        """

        messages = data.decode("utf-8").strip().split("\n")
        messages = [x.split(";") for x in messages]
        # print(messages)
        for s in messages:
            if s[0] == "START":
                self.board_size = int(s[1])
                self.colour = s[2]
                self.board = [
                    [0]*self.board_size for i in range(self.board_size)]

                if self.colour == "R":
                    self.make_move()

            elif s[0] == "END":
                return True

            elif s[0] == "CHANGE":
                if s[3] == "END":
                    return True

                elif s[1] == "SWAP":
                    self.colour = self.opp_colour()
                    if s[3] == self.colour:
                        self.make_move()

                elif s[3] == self.colour:
                    action = [int(x) for x in s[1].split(",")]
                    self.board[action[0]][action[1]] = self.opp_colour()
                    move_ZERO = chr(action[1]+ord("a")) + str(action[0]+1)
                    print(move_ZERO)
                    
                    self.game_ZERO.respond("play 1 "+move_ZERO)

                    self.make_move()

        return False

    def make_move(self):
        
        # print(f"{self.colour} making move")
        if self.colour == "B" and self.turn_count == 0:
            self.s.sendall(bytes("SWAP\n", "utf-8"))
            # else:
            #     move_ZERO = self.game_ZERO.respond('genmove')
            #     move_ZERO = (int(move_ZERO[1:])-1, ord(move_ZERO[0])-ord('a'))
            #     pos = move_ZERO
            #     self.s.sendall(bytes(f"{pos[0]},{pos[1]}\n", "utf-8"))
            #     self.board[pos[0]][pos[1]] = self.colour
        else:
            if self.colour == "R":
                move_ZERO = self.game_ZERO.respond('genmove')
                move_ZERO = (int(move_ZERO[1:])-1, ord(move_ZERO[0])-ord('a'))
            elif self.colour == "B":
                move_ZERO = self.game_ZERO.respond('genmove')
                move_ZERO = (int(move_ZERO[1:])-1, ord(move_ZERO[0])-ord('a'))
            pos = move_ZERO
            self.s.sendall(bytes(f"{pos[0]},{pos[1]}\n", "utf-8"))
            self.board[pos[0]][pos[1]] = self.colour
        self.turn_count += 1

    def opp_colour(self):
        """Returns the char representation of the colour opposite to the
        current one.
        """
        if self.colour == "R":
            return "B"
        elif self.colour == "B":
            return "R"
        else:
            return "None"


if (__name__ == "__main__"):
    agent = AlphaHexAgent()
    agent.run()
