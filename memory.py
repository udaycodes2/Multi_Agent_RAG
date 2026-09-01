class ConversationMemory:

    def __init__(self, max_history=5):

        self.max_history = max_history

        self.history = []

    def add_message(self, question, answer):

        self.history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        if len(self.history) > self.max_history:

            self.history.pop(0)

    def get_context(self):

        context = ""

        for item in self.history:

            context += f"""
User: {item['question']}

Assistant: {item['answer']}

"""

        return context