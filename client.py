import socket
import json
import threading
import time
import random
from sys import argv

class Client:
    def __init__(self):
        # Lecture des arguments
        self.client_port = int(argv[1])
        self.client_name = argv[2]
        server_ip = argv[3]
        server_port = int(argv[4])
        self.matricule = argv[5]

        self.server_address = (server_ip, server_port)

        # Socket pour parler au serveur (inscription)
        self.s_server = socket.socket()
        self.s_server.bind(("0.0.0.0", 0))  # écoute sur un port aléatoire

        # Socket pour écouter après inscription
        self.listener = socket.socket()
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # SOL_SOCKET pour utiliser TCP,IP, UDP ? -> aléatoire, va pouvoir réutiliser le meme port, 1 = activé ( 0 = désactivé)
        self.listener.bind(("0.0.0.0", self.client_port))   # peut écouter le serveur( 0.0.0.0) depuis le port du client


    def subscribe(self):
        message = {
            "request": "subscribe",      # création du message
            "port": self.client_port,
            "name": self.client_name,
            "matricules": [self.matricule]
        }

        self.s_server.connect(self.server_address) # établit la connexion entre le serveur et le client (en TCP)

        msg_encoded = json.dumps(message).encode()  # converti le message en bytes
        self.s_server.sendall(msg_encoded)  # et on l'envoie au serveur

        data = self.s_server.recv(1024)  # si le serveur le reçois pas on est bloqué ici et on ne va pas plus loins

        response = json.loads(data.decode())  # converti la réponse du serveur des bytes en python 

        if response.get("response") == "ok":  # si on reçois un 'ok' 
            print("Inscription validée")  # on met qu'on est inscrit
            return True
        else:
            print("Erreur d'inscription :", response)   # sinon on affiche ce qu'il a envoyé
            return False
        

    def listen_for_ping(self):
        print(f"En attente de connexions sur le port {self.client_port}...") # affiche qu'il essaye de se connecter
        self.listener.listen() # écoute le serveur

        while True:   # tant que le serveur tourne
            client_socket, addr = self.listener.accept()   # initie cette connexion
            print(f"Connexion de {addr}")   # affiche la connexion

            try:
                data = client_socket.recv(1024)   # peut recevoir jusqu'a 1024 octets et bloque tant qu'on a pas reçu le message
                message = json.loads(data.decode())  # le décode en python
                print("Reçu :", message)   # si on a reçu le message on l'affiche

                if message.get("request") == "ping":   # si on a bien reçu un "ping", .get pour ne pas faire une erreure si on a pas rçu de request
                    response = {"response": "pong"}     # on définit la réponse en tant qu'un "pong"
                    client_socket.sendall(json.dumps(response).encode())  # on envoie la réponse en bytes
                    print("Pong envoyé")    # et on affiche qu'on a bien envoyé un pong
            
                
                elif message.get("request") == "play":   # Si on reçois un request de play
                    state = message.get("state", {})     # l'état du plateau
                    board = state.get("board", [])       # on mets chaques cases du plateau dans une liste
                    piece_to_play = message["state"]["piece"]

                    def random_piece(board, piece_to_play = None):
                        # Génère tous les ensembles possibles de pièces (16 au total)
                        all_pieces = set()
                        for t in ['B', 'S']:
                            for c in ['D', 'L']:
                                for f in ['E', 'F']:
                                    for s in ['C', 'P']:
                                        all_pieces.add(frozenset([t, c, f, s]))  # frozenset ≠ set

                        # Pièces déjà utilisées, converties en frozensets
                        for p in board:
                            if p is not None and len(p) == 4:
                                all_pieces.discard(frozenset(p))
                        
                        if piece_to_play is not None:
                            all_pieces.discard(frozenset(piece_to_play))

                        if all_pieces:    # pieces qu'on peut jouer
                            chosen_set = random.choice(list(all_pieces))
                            return ''.join(chosen_set)  # retourne une string comme attendu
                        else:
                            return None
                    
                    try:
                        position = board.index(None)  # on essaye la première case vide
                    except ValueError:
                        position = None   # si none existe pas on mets none a position

                        # on génère une pièce aléatoire à donner à l'adversaire
                    next_piece = random_piece(board, piece_to_play)

                    if position is not None: 
                        move = {                      # on dit que move sera la position libre 
                            "pos": position,     # en donnant la prochaine pièce que l'adversaire doit mettre
                            "piece": next_piece
                        }  
                        response = {             # on définit la réponse a envoyer au serveur 
                            "response": "move",
                            "move": move,
                            "message": "Je joue un coup au hasard ;)"
                        }
                        print("Coup envoyé :", move)  
                    else:
                        response = "giveup" # si il n'y a plus de coup de disponible j'abandonne


                    client_socket.sendall(json.dumps(response).encode())  # on envoie la rep au serveur
        
                                    
            except Exception as e:   # prends tout types d'erreur
                print("Erreur réception ou décodage :", e)  # on affiche que le message n'a pas pu etre reçu ou pas envoyé 
            finally:  
                client_socket.close()    # on va pour l'instant fermer le socket dès que c'est fait une fois
                                         # le but est de remplacer ceci par quelque chose pour pouvoir jouer au jeu

    def run(self):
        if self.subscribe(): # si on réussi a s'inscrire il mets True et lance listen, sonon il ne le lance pas
            # Laisse le serveur 1 seconde pour préparer le ping (laisse le temps au client de lancer listen())
            time.sleep(1)
            thread = threading.Thread(target=self.listen_for_ping)   # on défini un thread qui va executer le listen
            thread.start()  # on lance ce thread, il va dcp faire le listen et en même temps il va pouvoir envoyer des messages

if __name__ == "__main__":    # si c'est bien sur ce programme, on le lance
    Client().run()

# Il faudrait supprimer les pièce qui ont déjà été employées