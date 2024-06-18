from get_date import resultado
import datetime


def jubu(resultado):
    data = None
    if isinstance(resultado, datetime.datetime):
        data = resultado.date()
        print(data)
    return data

if __name__ == "__main__":
    resultado = jubu(resultado)
