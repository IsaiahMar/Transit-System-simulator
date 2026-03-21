class Station:
    def __init__(self, station_id, name, capacity):
        self.station_id = station_id  # Unique ID
        self.name = name              # Station Name
        self.capacity = capacity      # Passenger Capacity
        
    def __repr__(self):
        return f"Station({self.name}, ID: {self.station_id})"