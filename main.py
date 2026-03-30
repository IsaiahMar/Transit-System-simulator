from collections import deque
import time
def main():
    network = TransitNetwork()
    print("Welcome to the Transit System Simulator")

    while True:
        print("\n--- Main Menu ---")
        print("1. Add a Station")
        print("2. Remove a Station")
        print("3. Add a Connection")
        print("4. Remove a Connection")
        print("5. Display Network")
        print("6. Exit")
        print("7. Find a route")
        print("8. Add Passenger")
        print("9. Board Train")
        print("10. Undo Last Action")
        
        try:
            choice = int(input("Enter your choice (1-10): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if choice == 1:
            s_id = int(input("Enter Station ID (number): "))
            name = input("Enter Station Name: ")
            cap = int(input("Enter Passenger Capacity: "))
            network.add_station(s_id, name, cap)
        elif choice == 2:
            s_id = int(input('Enter Station Number to remove:'))
            network.remove_station(s_id)
            
        elif choice == 3:
          id1 = int(input('Enter first Station ID')) 
          id2 = int(input('Enter second Station ID'))
          network.add_connection(id1, id2)
          
        elif choice == 4:
            try:
                id1 = int(input('Enter first Station ID: '))
                id2 = int(input('Enter second Station ID: '))
                network.remove_connection(id1, id2)
            except ValueError:
                print("Invalid input. Please enter numbers.")
            

        elif choice == 5:
            network.display_network()
        
        elif choice == 6:
            print('Exiting simulator. Goodbye!')
            break
        
        elif choice == 7:
            start = int(input('Enter starting Station ID'))
            end = int(input('Enter destination Station ID'))
            if network.dfs_path_exists(start, end):
                print("\nPath confirmed via DFS!")
                shortest = network.get_shortest_path(start, end)
                print(f"Shortest Route: {' -> '.join(shortest)}")
            else:
                print("\nNo route exists between those stations.")
                
        elif choice == 8:
            try:
                s_id = int(input('Enter Station ID to add passenger: '))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if s_id in network.stations:
                p_name = input('Enter Passenger Name: ')
                network.stations[s_id].add_passenger(p_name)
            else:
                print("Station not found.")
                
        elif choice == 9:
            try:
                s_id = int(input("Enter Station ID for boarding train: "))
                if s_id in network.stations:
                    train_cap = int(input("How many empty seats on the train? "))
                    network.stations[s_id].board_train(train_cap)
                else:
                    print("Station not found.")
            except ValueError:
                print("Invalid input. Please enter numbers.")
        elif choice == 10:
            network.undo_last_action()
             
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        return len(self.items) == 0

class Station:
    def __init__(self, station_id, name, capacity):
        self.station_id = station_id
        self.name = name
        self.capacity = capacity
        self.passenger_queue = deque()
    
    def add_passenger(self, passenger_name):
        self.passenger_queue.append(passenger_name)
        print(f"{passenger_name} joined the queue at {self.name}.")
        
    def board_train(self, train_capacity):
        boarded_count = 0
        print(f"\n--- Boarding at {self.name} ---")
        while self.passenger_queue and boarded_count < train_capacity:
            passenger = self.passenger_queue.popleft()
            print(f"{passenger} boarded the train.")
            boarded_count += 1
        
        if self.passenger_queue:
            print(f"{len(self.passenger_queue)} passengers left waiting in line.")
        else:
            print("The queue is now empty.")

    def __repr__(self):
        return f"{self.name} (Cap: {self.capacity})"

class TransitNetwork:
    def __init__(self):
        self.stations = {}  
        self.adj_list = {}
        self.action_history = Stack()

    # 1. Add Station
    def add_station(self, station_id, name, capacity):
        if station_id not in self.stations:
            self.stations[station_id] = Station(station_id, name, capacity)
            self.adj_list[station_id] = []
            self.action_history.push(f"add_station:{station_id}")
            print(f"Added station: {name}")
        else:
            print(f"Error: Station ID {station_id} already exists.")

    # 2. Remove Station
    def remove_station(self, station_id):
        if station_id in self.stations:
            station_name = self.stations[station_id].name
            # First, scrub this station from all its neighbors' connection lists
            for neighbor_id in self.adj_list[station_id]:
                self.adj_list[neighbor_id].remove(station_id)
            
            # Then, delete the station's own adjacency list and object
            del self.adj_list[station_id]
            self.stations.pop(station_id)
            self.action_history.push(f"remove_station:{station_id}:{station_name}")
            print(f"Removed station: {station_name}")
        else:
            print(f"Error: Station ID {station_id} not found.")

    # 3. Add Connection (Edge)
    def add_connection(self, id1, id2):
        if id1 in self.stations and id2 in self.stations:
            # Prevent duplicate connections
            if id2 not in self.adj_list[id1]:
                self.adj_list[id1].append(id2)
                self.adj_list[id2].append(id1)
                self.action_history.push(f"add_connection:{id1}:{id2}")
                print(f"Connected {self.stations[id1].name} <-> {self.stations[id2].name}")
        else:
            print("Error: One or both station IDs not found.")

    # 4. Remove Connection
    def remove_connection(self, id1, id2):
        if id1 in self.adj_list and id2 in self.adj_list:
            if id2 in self.adj_list[id1]:
                self.adj_list[id1].remove(id2)
                self.adj_list[id2].remove(id1)
                self.action_history.push(f"remove_connection:{id1}:{id2}")
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
        
    def dfs_path_exists(self, current_id, target_id, visited=None):
        if visited is None:
            visited = set()
        if current_id not in self.adj_list:
            return False
        visited.add(current_id)
        if current_id == target_id:
            return True
        for neighbor in self.adj_list[current_id]:
            if neighbor not in visited:
                if self.dfs_path_exists(neighbor, target_id, visited.copy()):
                    return True
        return False

    def get_shortest_path(self, start, end):
        if start not in self.adj_list or end not in self.adj_list:
            return None
        from collections import deque
        queue = deque([start])
        visited = set([start])
        parent = {start: None}
        found = False
        while queue:
            current = queue.popleft()
            if current == end:
                found = True
                break
            for neighbor in self.adj_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = current
        if not found:
            return None
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        return path[::-1]

    def undo_last_action(self):
        action = self.action_history.pop()
        if action is None:
            print("No actions to undo.")
            return
        print(f"Undid: {action}")

if __name__ == "__main__":
    main()
