import random
import hashlib

def rank(seed, node_id):
    # Simple hash-based ranking function
    return hashlib.sha256(f'{seed}-{node_id}'.encode()).hexdigest()

# The BASALT algorithm simulation
class BasaltNode:
    def __init__(self, node_id, num_nodes, view_size):
        self.id = node_id
        allNodes = list(range(num_nodes))
        allNodes.remove(self.id)
        self.id = node_id
        self.view_size = view_size
        self.view = random.sample(allNodes,view_size)
        self.seeds = [random.randint(0, num_nodes) for _ in range(view_size)]
        self.hits = [0 for _ in range(view_size)]


    def initialiser_voisins(self):
        toutes_paires = [(i, j) for i in self.view_size for j in range(i + 1, len(self.noeuds))]
        random.shuffle(toutes_paires)  # Mélanger aléatoirement les paires

        for i, j in toutes_paires:
            if len(self.noeuds[i].voisins) < self.NumNeighbors and len(self.noeuds[j].voisins) < self.NumNeighbors:
                self.noeuds[i].ajouter_voisin(j)
                self.noeuds[j].ajouter_voisin(i)
            
            # Vérifier si tous les nœuds ont le nombre requis de voisins
            if all(len(noeud.voisins) == self.NumNeighbors for noeud in self.noeuds.values()):
                break
    # Function to select peer based on the lowest hits
    def select_peer(self):
        min_hits = min(self.hits)
        candidates = [i for i, h in enumerate(self.hits) if h == min_hits]
        selected_index = random.choice(candidates)
        self.hits[selected_index] += 1
        return self.view[selected_index]

    # Function to update the view with new samples
    def update_sample(self, new_samples):
        for i in range(self.view_size):
            for new_peer in new_samples:
                # If new peer is better match, update the view
                if new_peer and (self.view[i] is None or rank(self.seeds[i], new_peer) < rank(self.seeds[i], self.view[i])):
                    self.view[i] = new_peer
                    self.hits[i] = 1
                elif new_peer == self.view[i]:
                    self.hits[i] += 1

    # Function to refresh seeds periodically
    def refresh_seeds(self, k, num_nodes):
        for i in range(k):
            r = (i % self.view_size) + 1
            self.seeds[r] = random.randint(0, num_nodes)
            self.view[r] = self.select_best_match_for_seed(r)

    def select_best_match_for_seed(self, seed_index):
        current_best = self.view[seed_index]
        for peer_id in self.view:
            if peer_id and rank(self.seeds[seed_index], peer_id) < rank(self.seeds[seed_index], current_best):
                current_best = peer_id
        return current_best
    def est_malveillant(self,allNodes):
        #un noeud est malveillant si hits est tres grand ou tres petit
        seuil  = 1.5 # a voir, depends de combien on veut voir la dispersion de la avg_hits dans les hits
        all_hits = [sum(node.hits)/len(node.hits) for node in allNodes]
        avg_hit = sum(all_hits)/len(all_hits)
        return abs(avg_hit-sum(self.hits)/len(self.hits))/avg_hit > 1.5  
    
    def afficher(self):
        return f'Le noeud {self.id} a pour view {self.view}\nhits : {self.hits}\nseeds : {self.seeds}'



#systeme distribue
num_nodes = 100  
view_size = 5   
exchange_interval = 1  
nodes = [BasaltNode(node_id=i, num_nodes=num_nodes, view_size=view_size) for i in range(num_nodes)]
print("-------------Avant Basalt-------------------")
for i in range(10):
    print(nodes[i].afficher())

# echanges 
for current_time in range(0, 1000, exchange_interval):
    for node in nodes:
        # Each node selects a peer to PULL from and sends a request
        pull_peer = node.select_peer()
        # Simulate receiving the pull_peer's view
        node.update_sample(nodes[pull_peer].view if pull_peer is not None else [])

        # Each node selects a peer to PUSH to
        push_peer = node.select_peer()
        # Simulate the push_peer updating its view based on the sender's view
        if push_peer is not None:
            nodes[push_peer].update_sample(node.view)

    # Periodically refresh seeds
    if current_time % (view_size / exchange_interval) == 0:
        for node in nodes:
            node.refresh_seeds(k=int(view_size / 2), num_nodes=num_nodes)

print("-------------------------Apres basalt---------------------")
for i in range(10):
    print(nodes[i].afficher())


print("------------------Malveillants------------------------")

all_hits = [node.hits for node in nodes]

for node in nodes:
    if node.est_malveillant(nodes):
        print(f"Le noeud {node.id} est potentiellement malveillant.")