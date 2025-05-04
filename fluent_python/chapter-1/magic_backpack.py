class Backpack:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.items = []
        self.total_quantity = 0

    def __setitem__(self, key, value):
        if self.total_quantity + value > self.capacity:
            raise ValueError("Backpack capacity exceeded")
        
        for i, (item_key, item_value) in enumerate(self.items):
            if item_key == key:
                self.total_quantity -= item_value
                self.items[i] = (key, value)
                self.total_quantity += value
                return
                
        self.items.append((key, value))
        self.total_quantity += value
        
    def __getitem__(self, key):
        for item in self.items:
            if item[0] == key:
                return item[1]
        raise KeyError(f"Item '{key}' was not found in the backpack")
    
    def __len__(self):
        return len(self.items)
    
    def __repr__(self):
        return f"Backpack(capacity={self.capacity}, items={self.items}, total_quantity={self.total_quantity})"
    

# test the Backpack class
backpack = Backpack(6)
backpack["apple"] = 2
backpack["banana"] = 3
backpack["cherry"] = 1

print(backpack)