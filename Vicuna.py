from llama_cpp import Llama

class Chat():
    def __init__(self, model, system):
        self.model = model
        self.system = system
        self.history = ''
        self.llm = Llama(model_path=model, n_ctx=4096, verbose=False)

    def _generate(self, prompt):
        # template = 'system context. USER: {prompt} ASSISTANT:'
        prompt = f'{self.history}\nUSER: {prompt}\nASSISTANT:'

        response = ''
        streamer= self.llm(self.system + prompt, stream=True, stop=['USER', 'ASSISTANT'], temperature=0.8, top_k=40, top_p=0.9, seed=-1)
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
system = """
Debes responder todo en español de la manera más correcta posible.
Eres un asistente muy cordial y respondes todo de manera resumida y con información verdadera.
"""
chat = Chat('/home/roberto/Pruebas/llm/models/gguf/vicuna-7b-v1.5.Q4_K_M.gguf', system)
chat.run()
