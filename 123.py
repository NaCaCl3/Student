from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")
print("Start")
generator = pipeline("text-generation", model = "ai-forever/rugpt3small_based_on_gpt2")
print("Enter")
print("Quit = 'q'")
while(True):
    user_input = input()
    if user_input.lower == "q":
        break
    print("AI think")
    result = generator(user_input, max_length = 1500, num_return_sequences = 1, truncation = True, do_sample = True, temperature = 0.1, repetition_penalty = 1.2)
    generated_text = result[0]['generated_text']
    print("Result", generated_text)