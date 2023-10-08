import json
from difflib import get_close_matches
import re

#C:\logisim\RestaurantChatbot\Restaurant-Chatbot-main
# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Dictionnaire pour associer les mots numéraux aux chiffres
word_to_number = {
    "un": 1,
    "deux": 2,
    "trois": 3,
    # Ajoutez les autres nombres au besoin
}

# Modifiez la fonction extract_numbers
def extract_numbers(user_input):
    numbers = re.findall(r'\d+', user_input)  # Extraire les chiffres numériques
    words = user_input.split()  # Séparer les mots

    # Convertir les mots numéraux en chiffres
    for word in words:
        if word.lower() in word_to_number:
            numbers.append(str(word_to_number[word.lower()]))

    return [int(number) for number in numbers]


# Save the updated knowledge base to the JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


# Find the closest matching question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(
        user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None


# Main function to handle user input and respond
def chatbot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == 'quit':
            break

        # Extraire les chiffres de l'entrée de l'utilisateur
        numbers = extract_numbers(user_input)

        if numbers:
            # Si des chiffres sont présents dans l'entrée
            for number in numbers:
                print(f"Bot: Vous avez mentionné le chiffre {number}")
                best_match: str | None = find_best_match(
                user_input, [q["question"] for q in knowledge_base["questions"]])

            if best_match:
                # If there is a best match, return the answer from the knowledge base
                answer: str = get_answer_for_question(best_match, knowledge_base)
                print(f"Bot: {answer}")
            else:
                print("Bot: Je ne connais pas la réponse?")
                new_answer: str = input("Écrivez la réponse a la question pour l'ajouter a la base de connaissance ou écrivez 'skip' pour ne pas ajouter a la base de connaissance: ")

                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append(
                        {"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print("Bot: Thank you! I've updated the knowledge base.")
                
        else:

            # Finds the best match, otherwise returns None
            best_match: str | None = find_best_match(
                user_input, [q["question"] for q in knowledge_base["questions"]])

            if best_match:
                # If there is a best match, return the answer from the knowledge base
                answer: str = get_answer_for_question(best_match, knowledge_base)
                print(f"Bot: {answer}")
            else:
                print("Bot: Je ne connais pas la réponse?")
                new_answer: str = input("Écrivez la réponse a la question pour l'ajouter a la base de connaissance ou écrivez 'skip' pour ne pas ajouter a la base de connaissance: ")

                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append(
                        {"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print("Bot: Thank you! I've updated the knowledge base.")


if __name__ == "__main__":
    chatbot()
