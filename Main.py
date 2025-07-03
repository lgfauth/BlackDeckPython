import logging
from Menu import menu_principal

# Configura o log para exibir no console
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

if __name__ == '__main__':
    menu_principal()
