import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()

try:
    json_file = open("intents.json")
    words_pkl_file = open("words.pkl", "rb")
    classes_pkl_file = open("classes.pkl", "rb")
except IOError as e:
    print(f"failed to open the file, {e.args[1]}")
else:
    intents = json.loads(json_file.read())
    words = pickle.load(words_pkl_file)
    classes = pickle.load(classes_pkl_file)

try:
    model = load_model("chatbot_model.h5")
except IOError as e:
    print(f"failed to load the model, check if it exists: {e.args[1]}")


class PredictResponse(object):
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(words)
        for w in sentence_words:
            for i, word in enumerate(words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        result = model.predict(np.array([bow]), verbose=None)[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(result) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        return return_list

    def get_response(self, intents_list, intents_json):
        tag = intents_list[0]["intent"]
        list_of_intents = intents_json["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i["responses"])
                break
        return result


def main():
    print("Felix Bot is running!")
    predict = PredictResponse()

    while True:
        message = input("You: ")
        ints = predict.predict_class(message)
        result = predict.get_response(ints, intents)
        print(f"Felix:", result)


if __name__ == "__main__":
    main()
