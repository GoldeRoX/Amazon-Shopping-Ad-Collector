from amazonadcollector.main import main

if __name__ == "__main__":
    while True:
        try:
            main(5560)
        except Exception as e:
            print(e)
            pass
