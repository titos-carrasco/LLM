from llama_cpp import Llama

class Chat():
    def __init__(self, model, user, assistant, system):
        self.model = model
        self.user = user
        self.assistant = assistant
        self.system = system
        self.history = system
        self.llm = Llama(model_path=model, n_ctx=4096, verbose=False)
        #self.llm('', stream=False)

    def _generate(self, prompt):
        prompt = f'{self.history}\n{self.user} {prompt}\n{self.assistant}'
        response = ''
        streamer= self.llm(prompt, stream=True, stop=[self.user, self.assistant], max_tokens= 4096, temperature=0.8, top_k=40, top_p=0.9, seed=-1)
        for chunk in streamer:
            text = chunk['choices'][0]['text']
            print(text, end='', flush=True)
            response += text

        self.history = prompt + response + '\n'

    def run(self):
        while(True):
            print(flush=True)
            try:
                prompt = input('>>> ').strip()
                if(prompt==''): continue
                if(prompt == 'bye'): break
                if(prompt=='h'):
                    print(self.history, flush=True)
                    continue
            except EOFError:
                break
            except KeyboardInterrupt:
                print(flush=True)
                continue

            try:
                self._generate(prompt)
            except KeyboardInterrupt:
                pass
            print(flush=True)

        print(flush=True)


#---
path_models = "/mnt/sda5/roberto/LLM Models/gguf/"
#model = 'TheBloke/vicuna-7b-v1.5.Q4_K_M.gguf'
#model = 'TheBloke/llama-2-7b-chat.Q4_K_M.gguf'
model = 'TheBloke/mistral-7b-openorca.Q4_K_M.gguf'
system = """
Debes responder todo en español de la manera más correcta posible.
Eres un asistente muy cordial y respondes todo de manera resumida y con información verdadera.
"""

chat = Chat(path_models + model, '|USER', '|ASSISTANT|', system)
chat.run()
