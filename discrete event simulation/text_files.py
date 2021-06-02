import pandas as pd
#create text file to store value 
def create_text(name, value):
    with open(f'{name}.txt', 'w') as f:
        f.write(f'{value}')

# get value from text file
def get_text_value(txt_name):
    value = float(open(f"{txt_name}.txt", "r").read())
    return value

def clean_csv(name):
    import pandas as pd
    df = pd.read_csv(f'{name}')
    df.to_csv(f'{name}', index=False)