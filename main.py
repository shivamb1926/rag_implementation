from src.pipeline import ask

def main():
    result = ask("what vegetarian dishes can i maek")
    print("Answer:", result["answer"])
    print("Sources:", result["sources"])

if __name__ == "__main__":
    main()
