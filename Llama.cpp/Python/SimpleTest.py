from llama_cpp import Llama

text="""
Pablo Neruda fue uno de los poetas más fecundos de la literatura chilena, latinoamericana y mundial del siglo XX. La influencia de su vida y obra trasciende el ámbito literario, permeando todos los campos de la cultura popular y académica, irradiando la historia política y social del país y alzándose como un referente indiscutido para la creación artística contemporánea.
En 1918 publicó sus primeros poemas, "Mis Ojos" y "Primavera", en la revista Corre Vuela, uno de los primeros exponentes del periodismo moderno chileno. Pese a su germinal talento, la poesía no fue del agrado de su padre. De ahí en octubre de 1920 el joven Neftalí Reyes decidió adoptar el seudónimo de Pablo Neruda, con el fin de evitar las preocupaciones familiares y ocultar así los esperados altibajos en la precoz trayectoria de un joven poeta provinciano.
En 1921, con apenas 16 años de edad, Neruda se trasladó a Santiago con el objetivo de estudiar Pedagogía en Francés en el Instituto Pedagógico de la Universidad de Chile. 
El ambiente intelectual y literario en torno a la Universidad y la vida bohemia santiaguina permitió que Neruda interactuara con otros poetas y escritores, 
integrando 1 2
"""
path_models = "/mnt/sda5/roberto/LLM Models/gguf/"
#model = 'TheBloke/llama-2-7b-chat.Q4_K_M.gguf'                      # n_ctx_train 4096
model = 'TheBloke/mistral-7b-openorca.Q4_K_M.gguf'                  # n_ctx_train = 32768
#model = 'TheBloke/neural-chat-7b-v3-1.Q4_K_M.gguf'                  # n_ctx_train = 32768 
#model = 'TheBloke/openhermes-2.5-mistral-7b.Q4_K_M.gguf'            # n_ctx_train = 32768
#model = 'TheBloke/vicuna-7b-v1.5.Q4_K_M.gguf'                       # n_ctx_train 4096 24.78

# swapoff -a
# 360 tokens -> prompt eval = 38 tokens/sec 
# llm = Llama(model_path=path_models+model, verbose=True, n_ctx=4*1024, n_batch=4*1024, n_threads=4, n_gpu_layers=0)
llm = Llama(model_path=path_models+model, verbose=True, n_ctx=4*1024, n_batch=4*1024, n_threads=4, n_gpu_layers=0)
llm.create_completion(text, stream=False, max_tokens=30 )
