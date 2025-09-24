Machine Learning For Your Gaming PC
================================================

Mar 30, 2022

![Windows Nvidia](/static/img/blogs/machine-learning-for-your-gaming-pc/windows_nvidia_docker_padded.png)

## Set Up Docker, Windows 11, and Nvidia GPUs for machine learning acceleration. 


Setting up local graphics cards (GPUs) to accelerate machine learning tasks can be tedious with
dependencies between GPU drivers, CUDA drivers, python, and python libraries to manage. With the
release of Windows 11, we can automatically handle dependencies between CUDA, Python, and deep
learning libraries such as Tensorflow, by using Docker. By using docker you can worry less about
driver compatibility issues between your drivers for gaming and drivers for deep learning workloads. 
<br />
<br />
You can receive major benefits from GPU acceleration depending on what types of models that you run.
Transformers are a popular choice for many NLP tasks, however, even just fine tuning smaller transformers 
such as DistilBERT can take hours if you are only using your computer's CPU. The results of training a 
Small BERT model on my CPU, GPU, and Google Colab are shown below. By switching to my GPU I was able to
fine-tune the model in minutes instead of hours. All the notebooks I used for testing are in this  
[Github Repo - ML Training Notebooks](https://github.com/PrestonBlackburn/gpu-acceleration-comparison)

![BertResults](/static/img/blogs/machine-learning-for-your-gaming-pc/bert_training_times.png)

Furthermore, the current trend in machine learning is to train larger and larger models to achieve
higher accuracy, which in turn take longer to fine-tune. As models get larger, fine-tuning using
GPU accelerated training will become more and more necessary. The figure below compares some 
high-performing models over the last decade. I recommend taking a look at more models on Papers
with Code and comparing the size of the recent top-scoring models with older models for yourself.  
[apersWithCode Imagenet Comparison](https://paperswithcode.com/sota/image-classification-on-imagenet)  

![ModelComp](/static/img/blogs/machine-learning-for-your-gaming-pc/model_size_comparision.png)

## Overview of setup

There are a lot of good resources for different elements of this setup, so I'll 
focus on bringing all of the components together in a step by step guide. For 
this walkthrough I'll go through upgrading to Windows 11 from Windows 10 (not
required, but recommended) and setting up docker to run TensorFlow on a Jupyter notebook. 

![NvidiaArc](/static/img/blogs/machine-learning-for-your-gaming-pc/docker_nvida_image.png)


## Part 1 Upgrading to Windows 11
*(skip if you already have W11)*  

<br/>

Check Windows 11 compatability:
<br />
<br />
There are a few things to check to make sure that you can upgrade
to Windows 11. There are workarounds for some of the requirmeents,
but the requirements are good security features to have enabled.
<br />
You can check your PC using [PC Health Check](https://www.microsoft.com/en-us/windows/windows-11#pchealthcheck)
<br />
Two new requirements for Windows 11 are secure boot and TPM 2.0 which may
not be enabled on older computers. 
If your PC fails any of the PC health checks follow the steps below.
Otherwise skip to the next section.  


1. Setting up Secure Boot
<br />
<br />
You'll need to enable secure boot in your computers bios. Follow allong with this
video to set it up if it isn't already - [Secure Boot Setup - YouTube](https://www.youtube.com/watch?v=vurIhOhTF0A) 
<br />
<br />
2. Enable TPM 2.0
<br />
<br />
Check processor compatibility.
If the processor is compatible then you should be good to go, but there may be some bios options that need to be changed
TMP 2.0 will be called PTT for intel chips. Checkout this video for how to setup TMP 2.0. [TMP 2.0 Setup - YouTube](https://www.youtube.com/watch?v=h-_c5vLj03A)
<br />
<br />
3. Download windows 11                    
<br />
<br />
Windows 11 still not officially rolled out to some PCs like mine, 
so you might need to download it form their site here - [Windows 11 Install](https://www.microsoft.com/en-us/software-download/windows11)

## Part 2 Setup docker for GPU

**Requirements**
<br />
<br />
1. WSL-2
<br />
2. Docker Desktop
<br />
3. Nvidia GPU Driver

**Make sure WSL-2, Docker, and Nvidia drivers are up to date**
<br />
<br />
1. Install or Update WSL-2 
<br />
<br />
run <i>wsl -l -v</i>  in terminal to check your WSL version. It should show version 2.
Also update WSL to the latest version with this command in the terminal <i> wsl --update </i>.  (my version was 5.10.102.1)

<br />
If it isn't installed follow this documentation [WSL Install Guide](https://docs.microsoft.com/en-us/windows/wsl/install)
<br />
<br />
2. Install and Update Docker Desktop
<br />
<br />
Follow the doces to install docker or update through the Docker desktop app. (my version was 4.6.1) [Docker Install Guide](https://docs.docker.com/desktop/windows/install/)
<br />
<br />
3. Update NVIDIA Driver                  
<br />
<br />
If you are using a PC for gaming just make sure your graphics card is updated in the GeForce Experience desktop app. (my version was 512.15 ) [Nvidia GeForce App](https://www.nvidia.com/en-us/geforce/geforce-experience/)

## Part 3 Test and Setup Jupyter Notebook

Once all of your apps are up to date test out if docker can detect your GPU
<br />
In the terminal run <i> docker run --gpus all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark </i>
<br />
If Docker can detect your GPU you can try to spin up a docker container with jupyter notebook and
TensorFlow to test if TensorFlow can detect your GPUs:
<br />
<br />
<i> docker run -it --gpus all -p 8888:8888 tensorflow/tensorflow:latest-gpu-jupyter </i>
<br />
<br />
Check out the full Nvidia guide here: &nbsp;
<a href="https://docs.nvidia.com/cuda/wsl-user-guide/index.html" target="_blank"> Nvidia WSL Guide </a> 
<br />
And the list of TensorFlow tested containers here:  &nbsp;
<a href="https://hub.docker.com/r/tensorflow/tensorflow/" target="_blank"> Official TensorFlow Docker Images </a> 
<br />
<br />
Next you'll probably want to mount a volume so you can access your existing Jupyter notebooks
and save your Jupyter notebooks outside of docker
<br />
<br />
In the terminal run:
<br />
<br />
<i> docker run -it --gpus all --rm -v C:\Users\your_username\your_jupyter_notebook_folder/:/tf/local_notebooks -p 8888:8888  tensorflow/tensorflow:latest-gpu-jupyter </i>
<br />
<br />
To break down the command:
<br />
<br />
<b> docker run </b> &nbsp; &nbsp; runs docker containers
<br />
<br />
<b> -it </b> &nbsp; &nbsp; basically makes the container look like a terminal connection session
<br />
<br />
<b> --gpus all </b>  &nbsp; &nbsp;assigns all available gpus to the docker container
<br />
<br />
<b> --rm </b> &nbsp; &nbsp; automatically clean up the container and remove the file system when the container exits
<br />
<br />
<b> -v </b> &nbsp; &nbsp; for specifying a volume
<br />
<br />
<b> C:\Users\your_username\your_jupyter_notebook_folder </b>   &nbsp; &nbsp; Local filepath that to use. This will be wherever you normally save your jupyter notebooks. 
<br />
<br />
<b> /tf/local_notebooks </b>  &nbsp; &nbsp; The filepath in docker
<br />
<br />
<b> -p </b>  &nbsp; &nbsp; expose ports, jupyter notebooks run on port 8888 by default so we
map port 8888 from the container to our local host to keep things simple
<br />
<br />
<b> tensorflow/tensorflow:latest-gpu-jupyter </b>  &nbsp; &nbsp; The image that we want to build. This comes 
pre-setup from tensorflow, but we can modify it needed. 

---

## Testing                 

For my testing I copied a TensorFlow tutorial for fine tuning BERT for sentiment
analysis on the imbd movie dataset. I also compared the performance to a Google 
Colab notebook with a free cloud GPU. My results are show below, and the notebooks
can be found on GitHub. &nbsp;
<a href="https://github.com/PrestonBlackburn/gpu-acceleration-comparison" target="_blank"> GitHub Notebooks </a> 

<br />
<br />
<b>Testing Results: </b>
<br />
<br />
Local GPU Time:
<br />
~2:40 minutes per epoch
<br />
Total Time: 16.1 minutes
<br />
<br />
Local CPU Time:
<br />
~22:00 minutes per epoch
<br />
Total Time: 131.8 minutes
<br />
<br />
Google Colab Time:
<br />
~4:30 minutes per epoch
<br />
Total Time: 26.6 minutes

<br />

My System
<br />
CPU: Intel i7-8700K
<br />
GPU: Nvidia RTX 2070
<br />
RAM: 24 GB


<br />
All tests were based on this notebook from TensorFlow:  &nbsp;
<a href="https://www.tensorflow.org/text/tutorials/fine_tune_bert" target="_blank"> TensorFlow BERT Fine Tuning </a> 


<br/>


### GPU Training

![GpuLoad](/static/img/blogs/machine-learning-for-your-gaming-pc/gpu_load_2.png)

### CPU Training

![CpuLoad](/static/img/blogs/machine-learning-for-your-gaming-pc/cpu_load_training.png)
