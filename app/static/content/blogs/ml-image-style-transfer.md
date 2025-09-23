Machine Learning In Production - Style Transfer
================================================

May 4, 2021

![Gatsby Stylized](/static/img/blogs/ml-image-style-transfer/stary_gatsby2.jpg)


Over the last couple of months, I have been diving into generative machine learning models, and I wanted to create something that people could interact with. In this project, I incorporated many of the techniques and frameworks I’ve learned into one project. Furthermore, I hadn’t seen a project like this done online before, so I thought it would be a good challenge to get the app up and running.

Some of the tools I used in this project:

- Django (Python)  
- TensorFlow / TensorFlow Lite  
- React (JavaScript)  
- Nginx  
- Docker  
- Docker Compose  
- AWS  

*I had created a site for this project that allows you to create your own stylized images, but I have since spun donw the site*

---

## What Is Style Transfer?

Style transfer is a machine learning algorithm that attempts to take the “style” from one image and impose it on another.  

In the example below Van Gogh’s *Starry Night* is the style image and the picture of my dog, Gatsby, is the target image.  
In the generated image you can see that the textures and swirl-like patterns have been transferred to the target image.

![Gatsby Example](/static/img/blogs/ml-image-style-transfer/Gatsby_Styled.jpg)

---

## Background

First off, I could have used TensorFlow.js instead of hosting the machine learning model in the backend to improve the app's performance and decrease complexity. However, the point of this app was to complete a full-stack React/Django/Nginx/Docker ML project with the ML model hosted by the backend. I had used all the tools before, but it was a challenge putting them all together.  

The app is hosted on AWS on the smallest EC2 instance. That means I have minimal resources to work with. Limited resources can pose a challenge for machine learning models, especially for those that deal with images. There is no database for this app because I didn’t want to store people’s photos.  

While I have designed some simple style transfer models previously, I used a pre-made model from Magenta for this app. The Magenta model is specifically optimized for fast style transfer, which is perfect to use on the tiny EC2 instance.

[TensorFlow Model](https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2)

---

## Building + Deploying the App

My general process in creating the app was to design the app (Figma), develop the backend (Python/Django), build frontend (JavaScript/React), and then prep the app for production (Docker + NGINX).  

The app is deployed on Amazon EC2 using a t2.micro instance (1 vCPU, 1 GB RAM). It quickly became apparent that the CPU and RAM limits would be an issue when I deployed my model and it instantly crashed on its first request. Using Docker, I saw CPU spike to 99% and crash. To fix it, I could either pay for a larger instance or optimize the model — I chose optimization.  

TensorFlow Lite solved the problem — reducing model size from ~80MB to ~3MB. The drawback was needing to resize inputs, but it made the app stable.  

Another bottleneck appeared: frontend uploads of large images slowed things down. To fix this, I downsized images client-side before sending them to the backend. This optimization made the app responsive and production-ready.  

Lessons learned: deploy/test in environments that match your production constraints. Development would have been faster if I had limited Docker resources to mimic EC2.

---

## About the Model

Magenta designed the model based on the paper *“Exploring the structure of a real-time, arbitrary neural artistic stylization network”* by Ghiasi et al.  

[Read the paper](https://arxiv.org/abs/1705.06830)

Early style transfer models only applied low-level features (like Monet brushstrokes). The Ghiasi et al. model generalizes much more broadly, even predicting styles it hasn’t seen before.  

The production setup uses two models:  

1. **Style prediction network** — generates an embedding vector from the style image.  
2. **Style transfer network** — uses embedding + content image to predict the stylized result.  

During training, a third model (VGG) is used to compute loss between style, content, and stylized images.  

An additional feature (not yet in my app) is adjusting stylization strength by interpolating embeddings between style and content.

---

### Model Architecture

![style-transfer-model](/static/img/blogs/ml-image-style-transfer/Arbitrary_stylet_ransfer_structure.jpg)
  
*Source: Ghiasi et al. 2017*

---

## Future Steps

Planned improvements:  

- Add loading spinner for uploads  
- Drag-and-drop example style images  
- Add HTTPS certificate (done on other projects)  
- Fix mobile bugs  

---

## References

- Ghiasi, G., Lee, H., Kudlur, M., Dumoulin, V., Shlens, J. 2017. *Exploring the structure of a real-time, arbitrary neural artistic stylization network*. arXiv preprint [arXiv:1705.06830](https://arxiv.org/abs/1705.06830).  

Other resources I used:  

- [React, Django, Docker Tutorial](https://datagraphi.com/blog/post/2020/8/30/docker-guide-build-a-fully-production-ready-machine-learning-app-with-react-django-and-postgresql-on-docker) — Blog by Mausam Gaurav  
- [Porting Arbitrary Style Transfer to the Browser](https://magenta.tensorflow.org/blog/2018/12/20/style-transfer-js/) — Blog by Reiichiro Nakano  
- [Nicholas Renotte’s YouTube Channel](https://www.youtube.com/channel/UCHXa4OpASJEwrHrLeIzw7Yg) — project inspiration  
