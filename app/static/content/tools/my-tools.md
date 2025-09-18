# Tools Tier list

This is a hodgepodge of a tier list made of tools I use or have used in the past enough to have an opinion on them. This could mean I used them for a month on a small project to ongoing regular usage. Tiers are subject to change.   


<br/>

<img src="/static/img/tools/tool_tier_list.png" alt="tier list" width="800"/>  

<br/>
<br/>

Here is my brief rational for my rankings

### Infrastructure related tools 
**Kubernetes** - Instant S tier. The ease of deployment and vast ecosystem make working with it a great experience. There is a learning curve, but I think nowadays the barrier to entry for Kubernetes has been greatly lowered.  
**Terraform** - D tier. For me this wouldn’t have been the case 4 years ago, but Terraform is outclassed by Kubernetes and vendor specific tooling like AWS CDK. It's way to easy to get a state file out of sync, and way too hard to onboard existing infrastructure. Now a days there are few use cases where I would reach for Terraform.   
**Keycloak** - B tier. It provides you with a lot of options and tools around auth, but it can be complex to set up for the first time and it was somewhat hard to parameterize as part of a helm chart. It gets the job done and so far seems to be a pretty solid pick for my auth.  
**ArgoCD** - A tier. Once I wrapped my head around how ArgoCD, Helm, and Kubernetes worked together it was a game changer. Pretty much anything serious I do with kubernetes I use helm charts and ArgoCD now.   
**Helm** - A tier. Helm makes release management and rollbacks so much easier with Kubernetes. Again anything serious on K8s should be done through a helm chart. It also makes it insanely easy to run other open source projects on K8s. Sometimes the templated yaml files can get messy and harder to follow though.   
**RabbitMQ** - B tier. Has a bunch of functionality around queuing, and pretty much just works out of the box without much config.
Minio - B tier. Again works out of the box without much setup, provides the same simple API as S3, and has a pretty good UI for admin management.  
**Docker** - C tier. A few years ago this would have been higher when there were less options for containerization. Somehow docker has seemed to get worse on Windows over the years.
**Podman** - B tier. I’ve had less issues with Podman so far than with docker, but I have only recently started playing around with it. Has better security features than docker, and I’m pretty much only using it to build containers for K8s. I could probably go back and forth with docker vs podman.  
**Nginx** - C tier. This isn’t necessarily Nginx’s fault, but there are always random annotations that I need to add to Nginx that feel like black magic. There are other options for load balancers/http servers, but I just haven’t played around with them yet  

### Data Eng Tools
**Prefect** - B tier. Pretty solid orchestrator if you need one. Since it is pure python you may have other options available where you don’t need an orchestrator at all. The deployment yaml don’t feel great though.   
**Airflow** - D tier. Feels pretty legacy now compared to more modern alternatives like Prefect. Something like Prefect is just easier to get up and running and works better on modern infra. You know you have an issue with deployment if there is a whole multi-million dollar SaaS company focused only on deploying the Airflow stack (Astronmer)  
**Airbyte** - A tier. Simple to setup and a simple UI gives your non-technical users an easy way to build their own pipelines. I’ve been able to scale it up to petabytes of data without doing anything crazy.   
**Coalesce** - F tier. At 2 separate companies we’ve almost lost business because non-technical people chose Coalesce. If you don’t want to write any code, don’t get into data engineering. Basically a half baked UI over some Jinja-esque templates. Don’t expect to automate anything more complex than a POC with Coalesce.  
**Matillion** - F tier. Not as egregious as Coalesce, but you can do the same thing with open source tools at a fraction of the cost. Let’s just stop with the UI driven data engineering tools, they always have sharp edges that you’ll never see in the demos.   
**DBT** - C tier. It's alright. A lot of what DBT does can be done with some simple python scripts (minus the UI), but a lot of other tooling is catching up with providing better lineage governance.  
**Kafka** - C tier. The infra was designed before most things were expected to run on K8s, so it is a little clunky to set up. Setting up connectors sucks since it is Java based. It still gets a C because there aren’t many serious open source competitors still (I want to spend some time looking more into Apache Flink).   

### UI
**React** - C tier. For anything I’m building, React is overkill. Plain HTML and some JS where I need it gets the job done. I take care of any more complex state in the backend.   
**HTMX** - B tier. Its nice to have in certain cases. Its not necessary, but nice to sprinkle in where it makes sense.  
**Streamlit** - D tier. If you want a POC app it's fine. It doesn’t hold up for bigger apps with its full page refreshes. Plus, it takes a lot of work to make anything built not look like a Streamlit app (If you look through their example you’ll see the two “sidebar” and “no-sidebar flavors”)  
**Sigma** - D tier. Again, has similar issues as other low code tools with sharp edges. Sometimes you’d be better just exporting to Excel.   
**Power BI** - C tier. You can do more with it than Sigma, but very “Microsoft”. No one has time to learn a proprietary DAX language for more complex functions.   


### Databases

**Sqlite** - B tier. It’s always there for you when you need it, but most of the time I just go straight to Postgres.  
**Postgres** - Our Second S tier. Coming from Snowflake, it's so nice to have a database that is open source. You can really dive into all of the details, like the postgres protocol, and the community supports a huge number of features like vector embedding storage + search.   
**Snowflake** - B tier. Snowflake is great for data warehousing, but they’ve leaned way too hard into Gen AI features instead of focusing on their bread and butter. A few years ago they might have been A tier, but the new and sometimes buggy features knock it down a tier.   
**DuckDB** - B tier. The SQLite of OLAP workloads, if you need to do any data processing locally DuckDBs got your back. Very handy for some ad-hoc data comparisons from different source systems  
**SQL Server** - D tier. It will still get the job done for you, but you’re going to pay Microsoft an arm and leg for software that you can get for free (Postgres, Mysql, etc..). An obvious pass if you’re looking to start a new project  
**Oracle** - F tier. I can only describe oracle as a worse version of SQL Server, and I hate its weird Oracle specific SQL syntax.  

### Languages and Coding
**Python** - SS tier. Great language, great ecosystem, and great community.   
**Javascript** - C tier. If I didn’t need it for the browser then there wouldn’t be any reason to use it. Use sparingly  
**Go** - B tier. I generally like go, but Python can do pretty much anything Go can with C bindings. The Python ecosystem feels more fleshed out than Go’s does, and I didn’t really get that much more from Go than Python for infra related scripts.  
**Neovim** - A tier. I enjoy coding more when I do it in NeoVim compared to other editors. There’s some visualizations and stuff I still don’t like doing in NeoVim, but I haven’t done a deep dive into all of Neovim's features yet.  
**VS Code** - C tier. I still like using VS code for things like writing markdown documentation or walking through code for someone, but for heavy coding tasks NeoVim is a better experience.   

### Data Science Tools

**Sklearn** - A tier. The OG of data science tools. It has all of the classics to get you going and a ton of great examples.  
**Pandas** - B tier. Another classic that has been falling out of favor recently for more optimized dataframe manipulation tooling like Polars and Apache Arrow. Still good for some simple cases.  
**Hugging Face** - A tier. Makes it very easy to work with LLMs, and you can pretty much find any of the latest models you want on hugging face. It is also great at abstracting away the underlying Tensorflow, Pytorch, etc.. implementations while still letting you fine tune or optimize the models.   
**Tensorflow** - D tier. Lost the battle to Pytorch, and is now mostly good just for some mobile/embedded applications. Back when I used it more there were a lot of issues going from TF1 to TF2  
**Pytorch** - B tier. Beats out Tensorflow in most ways. Since most people use Pytorch now, more cutting edge research is available with Pytorch code.   
**Kedro** - A tier. An awesome framework for bringing more structure and standardization to your data science projects. The learning curve can be a little steep though.   
**Jupyter Notebooks** - C tier. I really loved these when I was first learning python and data science, but now they are more of a liability when I run into them. You can run them in CI/CD processes, but generally I think it is worse than just writing a python module.    
**Apache Arrow** - A tier. The peak of data processing performance in Python.   

<br/>

*This tier list is getting crowded, so I’m going to call it here. I may do a further deep dive into each of the categories above. I didn’t really touch on any cloud providers and their tooling, so I may do another with more of a cloud provider focus in the future.*
