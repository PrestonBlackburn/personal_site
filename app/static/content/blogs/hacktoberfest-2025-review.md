Hacktoberfest 2025 Review: Good Intentions, Bad Incentives
==========================================================

Oct 29, 2025

![A sampling of some hacktoberfest participating repos](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Pl2SHuqH7AWyXXobcFzO_g.png)

This is my first year participating in Hacktoberfest. I’ve heard mixed things about it in the last few years, but I wanted to check it out for myself this year. Currently Hacktoberfest 2025 is coming to an end, so I want to share my experience. As a small OSS project maintainer it has been a positive experience. However as a potential OSS project contributor it has been rough.

### **As (Very) Small OSS Project Maintainer**

First off, I have an open source project that I’ve been working on, [struct_strm](https://github.com/PrestonBlackburn/structured_streamer), that I opened up to Hacktoberfest by adding the “hacktoberfest” repo tag. It is probably an ideal repo for something like Hacktoberfest because:

*   The repo is small enough that it is fairly easy to understand without a large time investment for contributors
*   I already have good CI/CD processes in place with pytest and pyright automation
*   The python package is hosted on Pypi which makes it really easy to get started using the library

To kick off hacktoberfest I put together some good beginner issues and tagged them appropriately. The detail was about the level that if I were to throw it into an LLM it would probably have a good chance at correctly addressing the PR with minimal review. None of it was too complex, but I thought the issues could be good learning opportunities for other contributors.

As the maintainer, it takes effort to pull together issues that are good beginner issues, but also provide value to the project. Then providing detailed feedback, testing, and reviewing the updates take time and can’t all be done by the CI/CD process. For example if someone is adding a UI component example I still had to test that out manually so I knew what the component would actually look like.

Spending this time was worth it for me to get some OSS maintainer experience, since these were the only PRs from the public to the project. It also isn’t bad to get more eyes on the project.

Other minor gripes I had were people asking to be assigned issues that they never worked on or abandoned. This isn’t a big deal since no one owes me anything, and these issues aren’t critical to the project functionality. Plus, I don’t have any sort of contributing guidelines on the repo yet.

In general the contributors were pleasant to work with. Even if it was clear that some used AI as part of their PR, they were pretty good at fixing issues I pointed out.

### **As a potential contributor**

Surprisingly, it was as someone casually looking for an OSS hacktoberfest project to contribute to where I wandered into a landscape of Hacktoberfest projects meant to game the system.

Hacktoberfest has had a bad rap over the last years, but with their repo tagging based participation approach, it is really on the maintainers if they want to participate or not. Even with this, I think Hacktoberfest still has a reputation of producing a lot of low quality un-solicited PRs which prevent many serious OSS projects from participating. If a maintainer is already having a tough time keeping up with managing PRs, Hacktoberfest would likely only exacerbate the issue.

This leads to a lot of demand from Hacktoberfest participants for repos to contribute to, but a low supply of repos participating in the event — an environment ripe for AI slop repos.

As a participant myself, I had a really hard time finding any mid-sized python project participating. I think that searching for a “random” repo isn’t necessarily the right way to go about it, but I thought I could spend a couple weeks getting familiar with a code base before making a contribution if I found the right project.

During this search I ran into swaths of low-quality AI generated repos created just for hacktoberfest. So many repos follow the same pattern, littered with emojis and fully fleshed out readme pages for simple todo apps. And so many fucking rocketship emojis. Everyone is going to the moon with their AI generated todo and OpenAI wrapper apps.

I’ve pulled out a couple readme examples from some of these repos, but I’ll keep the repos themselves anonymous. The actual code in the repos is fine, like most AI generated code for simple, uninteresting “in-distribution” examples.

### Examples

This was one of the first AI generated repos that really stood out to me. There may have been more text in the readme than actual code in the repo. We can see they didn’t even bother fixing the markdown heading format though.

![captionless image](https://miro.medium.com/v2/resize:fit:1388/format:webp/1*2e8BPTC39Bn_AbKOQUgyIQ.png)

In this CLI todo app example I think it would have taken me more time to find and add all of the emojis than it would to write all of the code. Obviously the author did not add the emojis by hand. Emoji maximalists are commonplace in many Hacktoberfest focused repos.

![captionless image](https://miro.medium.com/v2/resize:fit:1382/format:webp/1*61bXSFs3BcDfkQkNC26fzg.png)

These were a couple of the worst offenders, but there is clearly a common format and pattern to these AI Generated repos. If the purpose of creating repos like these is learning, why undermine your efforts by outsourcing all of the learning opportunities to AI?

**The Spirit of Hacktoberfest**

I’m not saying there aren’t quality projects participating in Hacktoberfest, but it is a lot of work to sift through all of the slop to find the projects and maintainers making a genuine effort.

The goal of hacktoberfest is supposed to be to support and get involved with open source projects, but because of the incentives most people are concerned most with padding resumes and getting the free shirt.

![t-shirts are a popular topic](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KJYOse1xo39N0DSj1RU7Nw.png)

With AI, bad actors have an easy way to generate a repo that adds no real value to open source, then share it on social sites using AI generated posts, and accept AI generated PRs to create a self-sustaining cycle and avoid actually learning or making meaningful contributions.

All of these barriers make it harder for participants who are operating in the spirit of Hacktoberfest. I think for future Hacktoberfests Digital Ocean (the Hacktoberfest host) needs to address these issues. Some of the changes they could make may involve creating centralized repos that they manage for everyone just wanting to learn how to make their first PR, and reducing the incentives for PRs.

Overall, my opinion of Hacktoberfest remains mixed. I think that Digital Ocean still has work they need to do to improve the event. Adding controls for maintainers to de-insentivize hacktoberfest PRs was a good first step, as I can definitely see why larger projects may not want to participate. From the contributor perspective, they have a lot of work to do to promote “real” open source projects and learning. On the other hand, it was a pretty good experience as a small OSS project maintainer.