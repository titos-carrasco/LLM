import os
import time
import json
import llama_cpp
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GLib
from llama_cpp import Llama

WIN_NAME = 'MainWindow'
WIN_DEF = './gChat.glade'

class gChat():
    def __init__(self, models_path):
        self.models_path = models_path
        self.llm_history = ''
        self.llm = None

        self.builder = Gtk.Builder()
        self.builder.add_from_file(WIN_DEF)

        self.models_list = self.builder.get_object('ModelsList')
        self.history = self.builder.get_object('History')
        self.prompt = self.builder.get_object('Prompt')
        self.enviar = self.builder.get_object('Enviar')

        models = os.listdir(models_path)
        models.sort()
        for model in models:
            self.models_list.append_text(model)
        self.models_list.set_active(0)

        buffer = self.history.get_buffer()
        endIter = buffer.get_end_iter()
        self.mark = buffer.create_mark('', endIter, False)

        self.builder.connect_signals(self)

    def onMainWindowDestroy(self, widget):
        Gtk.main_quit()

    def onModelSelected(self, widget):
        self.history.get_buffer().set_text('')
        self.prompt.set_text('')

        model_file = self.models_list.get_active_text()
        if(model_file[0] == '-'): 
            self.prompt.set_sensitive(False)
            self.enviar.set_sensitive(False)
            return
            
        self._setEnable(False)
        self._refreshGUI()
        
        config_file = self.models_list.get_active_text()
        self.config = self._loadConfig(config_file)
        self.system = self.config['generate']['template']['system']

        t0 = time.time()
        print('Cargando modelo', self.config['name'], '...', end='', flush=True)
        self.llm = Llama(**self.config['init'])
        print('%6.2f segundos' % (time.time() - t0), flush=True)        
        
        self._setEnable()
        self.prompt.grab_focus()

    def onSendClicked(self, widget):
        if(self.llm is None): return

        prompt = self.prompt.get_text().strip()
        if(prompt == ''): return
        self.prompt.set_text('')

        self._setEnable(False)

        buffer = self.history.get_buffer()
        text = '\n\n' + 'Usted: ' + prompt + '\nIA: '
        self._refreshHistory(text)

        self._generate(prompt)
        
        self._setEnable(True)
        self.prompt.grab_focus()

    def run(self):
       self.builder.get_object(WIN_NAME).show()
       Gtk.main()

    def _setEnable(self, enabled=True):
        self.models_list.set_sensitive(enabled)
        self.prompt.set_sensitive(enabled)
        self.enviar.set_sensitive(enabled)
        self._refreshGUI()

    def _loadConfig(self, config_file):
        f = open(self.models_path + '/' + config_file, 'rb')
        data = f.read(-1).decode('utf-8')
        f.close()
        return json.loads(data)    
        
    def _refreshHistory(self, text):
        buffer = self.history.get_buffer()
        endIter = buffer.get_end_iter()
        buffer.insert(endIter, text)
        self.history.scroll_mark_onscreen(self.mark)
        self._refreshGUI()

    def _generate(self, prompt):
        template = self.config['generate']['template']
        prompt = template['user'].replace('{prompt}', prompt) + \
                 template['assistant']
        response = ''
        streamer= self.llm(self.llm_history + self.system + prompt, stream=True, **self.config['generate']['params'])
        for chunk in streamer:
            text = chunk['choices'][0]['text']
            print(text, end='', flush=True)
            self._refreshHistory(text)
            response += text
        response = template['response'].replace('{response}', response)
        self.llm_history = self.llm_history + prompt + response

    def _refreshGUI(self):
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)


# ---
app = gChat('./models')
app.run()
