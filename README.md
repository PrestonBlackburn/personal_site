# Source Code For My Personal Site

My personal site setup. Feel free to reference this code or use it as starting point for your own projects.

<br/>

**Screenshot**  
![Site Example](/img/site_example.png)


# Some Tools and libraries Used

## UI

### Hydra Video Synth
Video synth that I'm using for the backgrounds
- Docs: https://hydra.ojack.xyz/docs/
Checkout their interactive browser here - [Hydra Interactive](https://hydra.ojack.xyz)

### xtermjs
Terminal emulator in the browser  
- Docs: https://xtermjs.org/  
Simple install - 
```bash
npm install @xterm/xterm
npm install --save xterm-addon-fit
```  

### Highlight JS
Syntax highlighting for codeblocks  
- Docs: https://highlightjs.org/  

### Tailwind
For some css styling, but I also just use a lot of custom CSS classes    
Docs - https://tailwindcss.com/  


## Backend

### FastAPI
Python server. I will probably introduce a build step in the future to clean this up, but right now I have most of my content as markdown files that I convert to HTML with Python. A lot of the endpoints + metadata is driven by the blog content in the markdown files.   

### Kubernetes
The backend is deployed with Kubernetes and I build the image for the site with the github action in this repo. 