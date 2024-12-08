class Shader:
    def __init__(self):
        self.content = None
    
    def get_shader_file(self, path):
        with open(path, 'r') as file:
            self.content = file.read()