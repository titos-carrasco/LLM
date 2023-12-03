
<h1>Notebook Asus FX505DY</h1>

```
$ cat /proc/cpuinfo 
vendor_id	: AuthenticAMD
cpu family	: 23
model		: 24
model name	: AMD Ryzen 5 3550H with Radeon Vega Mobile Gfx
cpu MHz		: 1327.366
cache size	: 512 KB
cpu cores	: 4

$ cat /proc/meminfo 
MemTotal:       16177096 kB

$ lspci
01:00.0 Display controller: Advanced Micro Devices, Inc. [AMD/ATI] Baffin [Radeon RX 460/560D / Pro 450/455/460/555/555X/560/560X] (rev e5)
05:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Picasso/Raven 2 [Radeon Vega Series / Radeon Vega Mobile Series] (rev c2)
```

<h1>Instalación normal de Llama.cpp Python</h1>

```
FORCE_CMAKE=1 pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --verbose
```

<h1>Instalación de Llama.cpp Python con aceleración de gpu Radeon</h1>

```
CXX=hipcc CMAKE_ARGS="-DLLAMA_HIPBLAS=on" CMAKE_BUILD_TYPE=Release FORCE_CMAKE=1 pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir --verbose
```

