class Log:
    def __init__(self):
        with open("log.txt", "w") as log:
            pass

    def write(self, text: str)->None:
        with open("log.txt", "a") as log:
            log.write(f"{text}\n")
