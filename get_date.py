import datetime
from allow_df import verdade

def juru(verdade):
    data = None
    if verdade:
        data = datetime.datetime.now().date()
    return data

if __name__ == "__main__":
    resultado = juru(verdade)
resultado=juru(verdade)