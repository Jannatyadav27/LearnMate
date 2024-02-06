import g4f

class GenerateQuiz:
    def __init__(self, topic, question_count=5):
        self.topic = topic
        self.question_count = question_count

    def start(self):
        prompt = f"Generate multiple-choice quiz questions about '{self.topic}'"
        response = g4f.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        print(response)

if __name__ == "__main__":
    test = GenerateQuiz("photosynthesis", 5)
    test.start()