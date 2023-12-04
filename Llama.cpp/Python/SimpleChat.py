import json
import time
from llama_cpp import Llama

class SimpleChat():
    def __init__(self, config_file):
        self.config = self._loadConfig(config_file)
        self.history = ''
        self.system = self.config['generate']['template']['system']

        t0 = time.time()
        print('Cargando modelo', self.config['name'], '...', end='', flush=True)
        self.llm = Llama(**self.config['init'])
        print('%6.2f segundos' % (time.time() - t0), flush=True)

    def _loadConfig(self, config_file):
        f = open(config_file, 'rb')
        data = f.read(-1).decode('utf-8')
        f.close()
        return json.loads(data)

    def _generate(self, user_input):
        template = self.config['generate']['template']
        prompt = template['user'].replace('{prompt}', user_input) + \
                 template['assistant']
        response = ''
        streamer= self.llm(self.history + self.system + prompt, stream=True, **self.config['generate']['params'])
        for chunk in streamer:
            text = chunk['choices'][0]['text']
            print(text, end='', flush=True)
            response += text
        response = template['response'].replace('{response}', response)
        self.history = self.history + prompt + response

    def run(self):
        while(True):
            print(flush=True)
            try:
                user_input = input('>>> ').strip()
                if(user_input==''): continue
                if(user_input == 'bye'): break
                if(user_input=='h'):
                    print(self.history, flush=True)
                    continue
            except EOFError:
                break
            except KeyboardInterrupt:
                print(flush=True)
                continue

            try:
                self._generate(user_input)
            except KeyboardInterrupt:
                pass
        print(flush=True)


#---
#model = 'models/Mistral 7B OpenOrca - GGUF.json'
model = 'models/llama-2-7b-chat - GGUF.json'

chat = SimpleChat(model)
chat.run()
