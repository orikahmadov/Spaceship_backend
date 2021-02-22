

class Starship:
    """Spaceship will have only name and hyperdrive rating"""
    def __init__(self, name, hyper_rating):
        self.name =  str(name)
        self.hyper_rating =  float(hyper_rating)


    def __repr__(self):
        return f"Name: {self.name} Rating: {str(self.hyper_rating)}"

