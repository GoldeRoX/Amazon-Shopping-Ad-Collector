from amazonadcollector.main import main
from amazonadcollector.database_connector import get_emulators_info, update_host

if __name__ == "__main__":
    # update_host()
    print(get_emulators_info())
    tab = get_emulators_info()
    for info in tab:
        print(info)