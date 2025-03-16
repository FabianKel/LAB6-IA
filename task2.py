from connect4 import Connect4
from agent import Agent
from player import Player

if __name__ == "__main__":
    game = Connect4()
    #Implementar menu para ejecutar cada modo de juego

    #Se crean los agentes
    agent1 = Agent(depth=2, alpha_beta=True, player_id=1)
    agent2 = Agent(depth=5, alpha_beta=True, player_id=2)

    #Se crean los jugadores
    player1 = Player("Red", None)
    player2 = Player("Purple", agent2)

    game.play(player1, player2) 