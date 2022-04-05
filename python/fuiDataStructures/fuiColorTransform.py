from dataclasses import dataclass, field

@dataclass(init=False)
class fuiColorTransform:
    fmt = "8f"

    mult_terms:list = field(default_factory=list)
    add_terms:list = field(default_factory=list)

    def __init__(self, red_mult_term:float, green_mult_term:float, blue_mult_term:float, alpha_mult_term:float, red_add_term:float, green_add_term:float, blue_add_term:float, alpha_add_term:float):
        self.mult_terms = list([red_mult_term, green_mult_term, blue_mult_term, alpha_mult_term])
        self.add_terms = list([red_add_term, green_add_term, blue_add_term, alpha_add_term])

    def __iter__(self):
        return iter([*self.mult_terms, *self.add_terms])