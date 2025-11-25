MLOps Challenges With Snowflake And Kedro
================================================

Jan 16, 2023

![Snowflake UDF](/static/img/blogs/snowflake-with-kedro/kedro_snowflake.png)


As I work on ML projects I always try to keep the three V's of MLOps in mind: **Velocity, Validation, and Versioning**.  
As investigated in *Operationalizing Machine Learning: An Interview Study*  
([snowflake-udf-performance-testing](https://arxiv.org/pdf/2209.09125.pdf)), these three V's are essential for a successful ML project.  
Since this project was still in the POC stage, my main focus is primarily on keeping a high velocity and good versioning, and less on validation.  

---


The main challenges I was facing were:

1. I was getting to the point where the pipeline was hard to conceptualize without any visualizations.  
   This reduced my velocity since I would need to take time to review the project structure every time I started a new development session.  

2. It was hard to onboard others to the project due to the increasing size of the project.  
   This also reduced the velocity of the project.  

3. I needed to do a better job of tracking dataset and model versions since I was starting to develop multiple datasets and models.  

4. I was starting to spend a considerable amount of time waiting for processing tasks to run.  
   A slow feedback loop was leading to a slower velocity.  

5. I needed to start thinking about ways to easily deploy my pipeline to a production environment.  
   This isn't part of the three V's, but was important for the next stage of the project.  

---

These are fairly common ML challenges, so a number of solutions exist to solve them. I knew I wanted a tool that would allow me to visualize my ML pipelines (preferably open source), so some options I looked into included Zen ML, Airflow, AWS Sagemaker, and Kedro. 
After some initial testing, I decided to go with Kedro, and I have really loved using it. 


> *“Kedro is an open-source Python framework to create reproducible, maintainable, and modular data science code. It uses software engineering best practices to help you build production-ready data science pipelines.”* (From the docs)

The Kedro project framework was similar to the project structure we were currently using so migrating wasn’t too bad. To migrate (generally), instead of wrapping a pipeline in a class, we moved the class initialization code out to the Kedro data catalog and parameter store, then registered the functions as Kedro nodes.

---


### Here is how I solved some of my challenges with Snowflake and Kedro:

1. *I was getting to the point where the pipeline was hard to conceptualize without any visualizations.*  
   - Kedro helps in two ways here. First, having this extensible framework out of the box made it easier to manage some of the complexity of the project by making it easy to split out the data loading into Kedro's data catalog.  
   - Second, Kedro has a **pipeline visualization tool**, so you can easily view how all of your pipelines are connected.  
     As part of the Kedro pipeline, nodes are created and node dependencies are automatically determined based on connections between the inputs and outputs of the nodes.  
     These connections can then be visualized using the **Kedro Viz extension**.  

2. *It was hard to onboard others to the project due to the increasing size of the project.*  
   - Since we weren't using a standardized framework and didn’t have any pipeline visualization tools, it took a long time to onboard new project contributors.  
   - With Kedro, new contributors can use Kedro Viz to see the full pipeline, and they can refer to the Kedro docs to get familiar with the project structure.  

3. *I needed to do a better job of tracking dataset and model versions.*  
   - The inputs to our ML project are dynamic, so both features and datasets themselves might change from run to run.  
   - Kedro made it easy to integrate **MLflow** to handle model versioning and results tracking.  
   - With MLflow I could easily reference all of the datasets and inputs used during experimentation.  

4. *I was starting to spend a considerable amount of time waiting for processing tasks to run.*  
   - I offloaded some of the computing I was doing locally and pushed it into **Snowflake**.  
   - I was already pushing intermediate datasets to Snowflake, so it was logical to do some of the simpler computations using **Snowpark**.  

5. *I needed to start thinking about ways to easily deploy my pipeline to a production environment.*  
   - Kedro comes in helpful here as well.  
   - Once your pipeline is developed it supports many deployment options like **Airflow** or **Sagemaker**.  
   - For the POC stages of this project all we needed to do was **dockerize the Kedro project** and run it on an EC2 instance, but using the framework means we can easily scale up in the future.  

---

My new local development workflow looks similar to this:

![local dev image](/static/img/blogs/snowflake-with-kedro/kedro_options.png)

---

Kedro comes with some SQL data support out of the box,  
but for a more full integration with Snowflake I had to create some new **Kedro DataSet classes**.  
The Kedro framework is extensible, so this was a relatively straightforward and well-documented process.  

You can find some of the code for creating the DataSets on my GitHub page:  
[PrestonBlackburn/kedro-snowflake-extensions](https://github.com/PrestonBlackburn/kedro-snowflake-extensions)

---

### Outcomes:

1. By switching our project to use the Kedro framework we were able to increase our velocity, improve our versioning, and prepare our project for deployment.  
   **Kedro Snowflake DataSets** make it easy to integrate Snowflake into your ML pipeline.  

2. By adopting a standardized framework I can more easily start up and switch between future projects.  

