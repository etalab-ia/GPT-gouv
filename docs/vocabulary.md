Informations à vérifier !

- Instruct : fine-tuning du modèle avec des exemples de question / réponse.
- [rlhf](https://huggingface.co/blog/rlhf) : Reinforcement Learning from Human Feedback : Système de fine-tuning utilisé par OpenAI qui donne des récompenses au modèle en fonction de ses réponses.
- Oobabooga : Un user GitHub qui a créé text-generation-webui
- PAL : astuce de demander à un modèle de générer du code qui va permettre de répondre à un problème. très util pour les mathématiques.
- CoT : Chain of Though, manière de demander à un modèle de résonner.
- text-generation-webui : [A gradio web UI for running Large Language Models like LLaMA](https://github.com/oobabooga/text-generation-webui)
- [GGML](https://github.com/ggerganov/ggml) : c'est ce qui permet d'utiliser le CPU pour l'inférence au lieu d'un GPU, mais c'est aussi un format de fichier ?
- GPTQ : Permet de réduire la taille des modèles, par exemple pour faire tenir Falcon-40B dans 24Go de VRAM
- ExLlama : Version spéciale Llama de GPTQ, chargement modèle plus rapide et inférence plus rapide également.

- GGML is a format for LLM's created to run inference (text completion) on CPU's.

GGML quantizes the model weights. It converts a more precise (bigger data type) and quantizes it into a smaller data type. For example from BF16 or FP16 into int8, int4, int3 etc. It was up until recently mostly executed on CPUs especially on llama.cpp, but can also be executed on GPUs. It works for most types of models, not only transformer based.

- GPTQ is a format that can be used by GPU's, how to actually use it?

GPTQ is another quantization method, that works only for transformer model architectures. It quantizes the stored model weights in a non-linear fashion, and ends up having better quality compared to just linear quantization into a smaller data type. GPTQ has a triton and a cuda branch, which was tricky initially, as it lead to a lot of confusion and non-compatibility especially on windows.

- What about ".safetensor" how to use this models?

Initially most models used a the pickle format to store tensors. Pickle files allowed to store python code, that will be executed on your local machine at runtime. This poses a security risk. Lately the safetensor format is being used instead, which doesn't contain executable python code

- What is the difference between them? why different formats?

GGML: slower(not sure), q3, q4, q5, q8 bit, many model architectures supported, mostly on CPU but works on GPU, runs on llama.cpp and similar implementations

GPTQ: faster(triton, but not sure), 4, 8 bit, only transformer architecture supported, only GPU, runs on many implementations

- llamacpp is C++ implementation of Llama by facebook, why is it needed?

it's not from facebook. it's optimized to run on modern apple hardware, which has an unified memory architecture and can thus use it's very fast SoC Memory, not needing any GPU memory. Before llama.cpp was here, you needed a beefy GPU with a lot of vram. Now you have the choice to run natively on a CPU with xxxx.cpp using GGML formatted models, or on a GPU using any other implementation and safetensor or HF .bin models.

- Oobabooga/KoboldAI is a UI wrapper for llamacpp and ____ ?

Oobabooga isn't a wrapper for llama.cpp, but it can act as such. A usual Oobabooga installation on windows will use a GPTQ wheel (binary) compiled for cuda/windows, or alternatively use llama.cpp's API and act as a GUI. On Linux you had the choice to use the triton or cuda branch for GPTQ, but I don't know if that is still the case. You can also go the route to use virtualized and hardware accelerated WSL2 Ubuntu on Windows and use anything similar to linux.

- KoboldAI vs Oobabooga, seems they do exactly the same with different UI.

KobolAI is actually llama.cpp or to be more clear, it is a fork, which implements some nice feautures. The main feature is, that it runs as web-app on local-server (same technique like oobabooga). Another cool thing is, the developer has pretty much compatibility in mind. So kobolAI should be able to run more diferent ggml formatted llms (not just llama based) and one more very important thing is backward compatibility. So KoboldAI Users dont have to care about breaking changes in the main developing of llama.cpp Ah, and you can save sessions/context/world information and characters in KoboldAI, which is really very pleasant and comfortable.

BUT: Of course the updates and upgrades are slower, since to dev has to do worke on more applications at the same time (means mainly different llama.cpp versions).

- Where, how, why CUDA, OpenBLAS, CLBlast is used, and how related to each other?

cuBLAS is a GPU-accelerated library for basic linear algebra subroutines (BLAS) for NVIDIA GPU

clBLAS does the same but for OpenCL, so it has wider GPU support, not only NVIDIA

CLBlast is an optimized clBLAS library with several advantages over clBLAS

Overall it doesn't really matter as an end-user, it's more for the folks implementing features and working on tools. Use cuBLAS if you have an nvidia GPU and the tool supports it. Otherwise use CLBlast and only then use clBLAS

- How an agent actually run code (tools), how is that "Action: use tool X" -> X(), is it basic code string manipulation that runs over the output?

        Several things: Usually the model is pre-prompted with an instruction to think in terms of steps (CoT - Chain of Thought) or inner thoughts, before making decisions.

        The topic is huge, have a look into ToolFormer, LangChain, Microsoft guidance, Microsoft semantic-kernel, LlamaIndex and lately on YouTube videos. There are some good introductions

- PyTorch, Tensorflow, what, how, why is needed for oobabooga?

        Based on Torch, a ML library but written in Lua, PyTorch does the same in Python

        PyTorch is a big framework for various ML tasks, not only LLMs

        The most important concept of PyTorch are probably "Tensors", which like Arrays but are optimized to run on CUDA capable Nvidia GPUs (and other similar hardware) Since those Arrays are broad and long they benefit from massive parallelization and usually GPUs are much better than CPUs to do that. Lately support for AMD ROCm and Apple Metal is added

        Most common operations on tensors are n-dimensional array operations like BLAS (see above), dot product, matrix multiplication etc.

        Read an introduction on ML and one on LLMs to learn more

        AFAIK, Tensorflow is a similar framework but from GoogleBrain and is not compatible. Parallelism is easier implemented on PyTorch than on Tensorflow

- "Install GPTQ-for-LLaMa and the monkey patch" what is the purpose of this? -

        Since GPTQ-for-LLaMa had several breaking updates, that made older models incompatible with newer versions of GPTQ, they are sometimes refering to a certain version of GPTQ-for-LLaMa. So if the notes of a model, or a tutorial tells you to install GPTQ-for-LLaMa with a certain patch, it probably referrs to a commit, which if you know git, you can specifically clone a commit-hash or a feature branch


