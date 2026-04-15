from pipeline.guard_pipeline import analyze_prompt

if __name__ == "__main__":
    while True:
        text = input("Enter prompt: ")
        result = analyze_prompt(text)
        print(result)