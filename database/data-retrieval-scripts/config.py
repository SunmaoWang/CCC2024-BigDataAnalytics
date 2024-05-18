# Helper function to read config data, obtained from workshop repository
def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()
