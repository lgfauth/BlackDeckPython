import logging
from EnergyFarmer import executar_energy_farm
from DungeonExplorer import executar_dungeon_explorer

def menu_principal():
    while True:
        print('\n' * 15)

        print("""
        ============================
               BLACK DECK BOT
              
                    MENU
        ============================
        """)
        print(" ")
        print(" ")
        print("1 - Energy Farm")
        print("2 - Dungeon Explorer")
        print("0 - Sair")
        print(" ")
        
        print('\n' * 15)
        escolha = input("Selecione uma opção: ").strip()

        if escolha == "1":
            executar_energy_farm()
        elif escolha == "2":
            executar_dungeon_explorer()
        elif escolha == "0":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")
