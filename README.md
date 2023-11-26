# LLM
Mis pruebas con modelos de lenguaje grandes (LLM) utilizando sólo CPU

* Directorio Llama.cpp: Inference of LLaMA model in pure C/C++ (https://github.com/ggerganov/llama.cpp)


Algunas notas que debo eventualmente verificar:
* Texto entra al LLM, texto sale del LLM
* La producción del texto de salida depende del texto de entrada y del corpus utilizado en el entrenamiento
* La calidad de lo producido depende de la calidad del texto de entrada y de la calidad del corpus de entrenamiento
* El "conocimiento" del LLM depende de la cantidad del corpus de entrenamiento y de la cantidad del texto de entrada
* Los llamados "templates" sirven para crear una estructura del texto de entrada tal de guiar al LLM en su inferencia
* El LLM no tiene memoria. Se debe sumar al texto de entrada toda la entrasa y salida anterior de manera acumulativa
* El LLM no puede generar nada que no esté en su data de entrenamiento y/o la data de entrada
* El LLM tendría solucionado la interacción en lenguaje natural y en diferentes idiomas
* Aumentar el "conocimiento" del LLM se podría hacer con:
    * Entrenamiento del LLM
    * Ajuste fino del LLM
    * Aumentar el texto de entrada (RAG?) inyectando el nuevo "conocimiento" al texto del usuario

* La primera vez que se aghrega al texto de entrada un texto grande, se produce una demora importante antes de que se empiece a generar la salid
* Esto no ocurre si los nuevos textos que se agregan son pequeños (aunque se sigue inyectando toda la conversación)
