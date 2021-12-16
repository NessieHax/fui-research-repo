

class fuiColorTransform:
    def __init__(self, red_mult_term:float, green_mult_term:float, blue_mult_term:float, alpha_mult_term:float, red_add_term:float, green_add_term:float, blue_add_term:float, alpha_add_term:float):
        self.transform:dict = {
            "mult_terms" : [red_mult_term, green_mult_term, blue_mult_term, alpha_mult_term],
            "add_terms" : [red_add_term, green_add_term, blue_add_term, alpha_add_term]
        }

    def get(self) -> dict:
        return self.transform

    def __str__(self) -> str:
        return self.transform.__str__()