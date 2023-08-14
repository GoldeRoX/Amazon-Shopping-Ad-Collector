from amazonadcollector.main import main

if __name__ == "__main__":
    while True:
        while True:
            try:
                main(5554)
            except Exception as e:
                print(e)
                pass
