import os
import time
import llama_cpp
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GLib
from llama_cpp import Llama

WIN_NAME = 'MainWindow'
WIN_DEF = './gTokens.glade'

class gTokens():
    def __init__(self, models_path):
        self.models_path = models_path
        self.llm = None

        self.builder = Gtk.Builder()
        self.builder.add_from_file(WIN_DEF)

        self.models_list = self.builder.get_object('ModelsList')
        self.prompt = self.builder.get_object('Prompt')
        self.tokenized_prompt = self.builder.get_object('TokenizedPrompt')
        self.calcular = self.builder.get_object('Calcular')
        self.timmings = self.builder.get_object('Timmings')
        self.timmings_text = self.timmings.get_text()
        self._setTimmings()

        models = os.listdir(models_path)
        models.sort()
        for model in models:
                self.models_list.append_text(model)
        self.models_list.set_active(0)

        self.builder.connect_signals(self)

    def onMainWindowDestroy(self, widget):
        Gtk.main_quit()

    def onModelSelected(self, widget):
        self._setEnable(False)
        self.llm = None

        self.tokenized_prompt.get_buffer().set_text('')
        self.timmings.set_xalign(0.5)
        self.timmings.set_text('\n\n\nCargando el Modelo ...\n\n\n\n')
        self._refreshGUI()
        time.sleep(0.1)

        model_file = self.models_list.get_active_text()
        if(model_file[0] != '-'):
            model = self.models_path + '/' + model_file
            self.llm = llama_cpp.Llama(model_path=model, verbose=True, n_ctx=4*1024, n_batch=4*1024, n_threads=4, n_gpu_layers=0)

        self._setTimmings()
        self._setEnable(True)

    def onPromptChanged(self, widget):
        self.tokenized_prompt.get_buffer().set_text('')
        self._setTimmings()

    def onCalculateClicked(self, widget):
        if(self.llm is None): return
        self.llm.reset()

        self._setEnable(False)
        self.tokenized_prompt.get_buffer().set_text('')
        self.timmings.set_xalign(0.5)
        self.timmings.set_text('\n\n\nCalculando ...\n\n\n\n')
        self._refreshGUI()
        time.sleep(0.1)

        buffer = self.prompt.get_buffer()
        startIter, endIter = buffer.get_bounds()    
        text = buffer.get_text(startIter, endIter, False)
        tokens = self.llm.tokenize(text.encode('utf-8'))
        ntokens = len(tokens)

        text = ''
        for token in tokens:
            t = self.llm.detokenize([token])
            text = text + ' ' + t.decode('utf-8')
        self.tokenized_prompt.get_buffer().set_text(text)

        self.llm.create_completion(tokens[:360], stream=False, max_tokens=3)
        timmings = llama_cpp.llama_get_timings(self.llm.ctx)
        self._setTimmings(ntokens, timmings)

        self._setEnable(True)

    def _setEnable(self, enabled=True):
        self.models_list.set_sensitive(enabled)
        self.prompt.set_sensitive(enabled)
        self.calcular.set_sensitive(enabled)

    def _setTimmings(self, ntokens=0, timmings=None):
        self.timmings.set_xalign(0)
        if(timmings is None):
            self.timmings.set_text(self.timmings_text % (0, 0, 0, 0, 0, 0, 0, 0))
        else:
            self.timmings.set_text(self.timmings_text % (
                                                            ntokens, 
                                                            timmings.n_p_eval, timmings.t_load_ms, timmings.t_sample_ms, 
                                                            timmings.t_p_eval_ms, timmings.n_p_eval/timmings.t_p_eval_ms*1000,
                                                            timmings.t_eval_ms, timmings.t_end_ms - timmings.t_start_ms
                                                        )
                                )

    def _refreshGUI(self):
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)

    def run(self):
       self.builder.get_object(WIN_NAME).show()
       Gtk.main()


# ---
app = gTokens('/mnt/sda5/roberto/LLM Models/gguf/TheBloke')
app.run()
