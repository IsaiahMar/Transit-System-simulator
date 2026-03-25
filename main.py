from collections import deque
import time
class Station:
    def __init__(self, station_id, name, capacity):
        self.station_id = station_id
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return f"{self.name} (Cap: {self.capacity})"

class TransitNetwork:
    def __init__(self):
        self.stations = {}  
        self.adj_list = {}  

    # 1. Add Station
    def add_station(self, station_id, name, capacity):
        if station_id not in self.stations:
            self.stations[station_id] = Station(station_id, name, capacity)
            self.adj_list[station_id] = []
            print(f"Added station: {name}")
        else:
            print(f"Error: Station ID {station_id} already exists.")

    # 2. Remove Station
    def remove_station(self, station_id):
        if station_id in self.stations:
            # First, scrub this station from all its neighbors' connection lists
            for neighbor_id in self.adj_list[station_id]:
                self.adj_list[neighbor_id].remove(station_id)
            
            # Then, delete the station's own adjacency list and object
            del self.adj_list[station_id]
            removed_station = self.stations.pop(station_id)
            print(f"Removed station: {removed_station.name}")
        else:
            print(f"Error: Station ID {station_id} not found.")

    # 3. Add Connection (Edge)
    def add_connection(self, id1, id2):
        if id1 in self.stations and id2 in self.stations:
            # Prevent duplicate connections
            if id2 not in self.adj_list[id1]:
                self.adj_list[id1].append(id2)
                self.adj_list[id2].append(id1)
                print(f"Connected {self.stations[id1].name} <-> {self.stations[id2].name}")
        else:
            print("Error: One or both station IDs not found.")

    # 4. Remove Connection
    def remove_connection(self, id1, id2):
        if id1 in self.adj_list and id2 in self.adj_list:
            if id2 in self.adj_list[id1]:
                self.adj_list[id1].remove(id2)
                self.adj_list[id2].remove(id1)
                print(f"Severed connection: {self.stations[id1].name} <-X-> {self.stations[id2].name}")
        else:
            print("Error: One or both station IDs not found.")

    # 5. Display Network
    def display_network(self):
        print("\n=== Current Transit Network ===")
        if not self.stations:
            print("Network is currently empty.")
            return

        for station_id, station in self.stations.items():
            connections = [self.stations[adj_id].name for adj_id in self.adj_list[station_id]]
            conn_str = ", ".join(connections) if connections else "None"
            
            print(f"[{station_id}] {station.name} (Cap: {station.capacity})")
            print(f"    --> Connects to: {conn_str}")
        print("===============================\n")
        
    def if_path_exists(self, current_id, target_id, visited=None):
            if visited is None:
                visited = set()
                
            visited.add(current_id)
            
            if current_id == target_id:
                return True
            
            for neighbor