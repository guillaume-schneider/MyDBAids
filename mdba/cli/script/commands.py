def init_database(interface):
    dt = interface.init()
    print(f"Database initialized !")

def inject_data(interface, nb_insertions):
    interface.inject(int(nb_insertions))
    print(f"{nb_insertions} data injected !")

def clear(interface):
    interface.delete_injected_data()
    print("Injected data deleted !")

def use_database(interface, database_name):
    dt = interface.change_database(database_name)
    print(f"Database changed to {dt} !")

def update(interface):
    interface.update()
    print("Database updated !")
