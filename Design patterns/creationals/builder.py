class House:
    """The Product."""
    def __init__(self, builder):
        self.foundation = builder.foundation
        self.structure = builder.structure
        self.roof = builder.roof
        self.interior = builder.interior
        # ... other attributes

    def display(self):
        print(f"House with: {self.foundation}, {self.structure}, {self.roof}, {self.interior}")

class HouseBuilder:
    """The Concrete Builder."""
    def __init__(self):
        self.foundation = None
        self.structure = None
        self.roof = None
        self.interior = None

    def set_foundation(self, foundation):
        self.foundation = foundation
        return self  # Enables method chaining

    def set_structure(self, structure):
        self.structure = structure
        return self

    def set_roof(self, roof):
        self.roof = roof
        return self
    
    def set_interior(self, interior):
        self.interior = interior
        return self

    def build(self):
        """Returns the final, constructed product."""
        return House(self)

# Client Usage
builder = HouseBuilder()
dream_house = builder.set_foundation("Concrete") \
                     .set_structure("Wood Frame") \
                     .set_roof("Shingles") \
                     .set_interior("Modern") \
                     .build()

dream_house.display()
