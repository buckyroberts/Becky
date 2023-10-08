class Challenge:

    def __init__(self, *, instructions, name, output, points, source_code):
        self.instructions = instructions
        self.name = name
        self.output = output
        self.points = points
        self.source_code = source_code

    def __str__(self):
        return f'{self.points} | {self.name}'
