Exploring LLM Citation Generation In 2025
=============================================

May 7, 2025

![captionless image](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*2fIbwtrHsBtaRYrldVPE8A.png)

Question answering is one of the most popular use cases for LLMs. However, the propensity for LLMs to hallucinate means that users should not trust responses, and must cross reference LLM responses with ground truth data whenever possible. Citations are a great way to add more explainability to your LLM’s responses, and make it easy to verify that the LLM is using relevant information, thus reducing the probability of hallucinations.

Combatting hallucinations is critical for scenarios where accurate responses are needed. For example, in the [chatbot I’m building for college courses](https://www.teacherspet.tech/), if a student queries the chatbot about the due date of an assignment they can double check the cited documents to easily verify the correctness of the response.

A more extreme example of a lack of LLM literacy and hallucinations was the viral case of a lawyer who submitted six fake case citations in a court that was exposed by this [New York Times article](https://www.nytimes.com/2023/05/27/nyregion/avianca-airline-lawsuit-chatgpt.html). The lawyer ended up being fined $5,000 for submitting the false documents to the court. If easy to validate citations would have been provided with responses, the lawyers may have been able to spot the fake cases. That article came out in 2023, and I’d like to think more people have learned to question LLM responses, but this leads to a trust issue with LLM responses. This is another area where citations can help. In this [Citations and Trust in LLM Generated Responses paper](https://ojs.aaai.org/index.php/AAAI/article/view/34550) we can see that citations significantly increase trust.

![Citations can work both ways, with random/bad citations decreasing trust and correct citations increasing trust](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*HpGpll3qgQMPzBSS)

With the increase of LLMs integration in search experiences (ex: the AI Overview feature in google) we are seeing citations becoming more prevalent. In the case of Google’s AI Overview for search, citations in the form of links are provided. For my use case of searching across class documents, I explore some ways that citations can be provided for responses — naïve generation, structured outputs, and context free grammar. All citation cases will begin with a RAG pipeline returning a few key document chunks.

### **Naïve Citation Generation**

The most basic citation generation approach, naïve generation, only consists of a few main components. All that is needed is the reference documents/content and some prompting to specify the citation format. If only a few documents are needed they can be added to the prompt context window, otherwise we can use RAG to only return the most relevant documents to the user’s query. This simple workflow is shown below:

![High level RAG workflow with citation generation](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*D_35WEsmAjjf1DQd)

I’ve added a couple other common steps related to my use case. We chunk the documents in a way that makes sense for our use case, and then use a metadata table to make sure we can track the chunks to their source documents along with other metadata. This also has the benefit of scoping our citations to a more granular level than the document.

In this naïve citation generation scenario we must post-process the text returned from the model to extract the document references, so they can be properly linked when the user views them in the UI.

Citation formatting can be handled a variety of ways, but for this exploration, I want to return the citations in a numerical format, where I’ll add a hover over effect when the user hovers over the bracketed citation number as a starting point. This format will be defined in the system prompt. Static example response:

_The project must include a working demo [1]_

Now that we have an idea of what naïve citation generation looks like, some drawbacks should start to become apparent

*   There is no guarantee the the citation will actually be generated
*   There is no guarantee that the citation will be correct
*   We could generate a citation without knowing which document it belongs to based on the prompting

The benefits of this approach are that it is simple to set up, and may be good enough when citations are not critical for the application. However, we address some of these issues by using structured outputs for citation generation.

### **Structured Output Citation Generation**

Structured output is a response option from most major LLM providers where the output will be guaranteed to follow a given JSON schema. We’ll get into the mechanism behind structured outputs in the next section when we get into grammar rules.

Overall the pipeline with structured output generation looks the exact same as the naïve citation, but we need to provide schema we want the output to conform to. We can either do this directly with JSON, or indirectly with Python classes using Pydantic, which then get converted into JSON.

Originally I thought this may have a performance impact, but when I was testing the naïve citation generation performance vs the structured output generation. This might be because I used the OpenAI completions API for structured output generation, but the newer responses API for the naïve generation. Both are close enough differences could just be due to differences in traffic on the OpenAI side and slight difference in completion tokens returned.

![Performance of the naïve (standard) and structured output strategies are basically the same. There could be some caching going on eventhough all context starts with a random number. On first runs the TTFT is more around 0.4s](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*SIK4UFrdCmfmGv3l)

All of the code for this post is on [GitHub](https://github.com/PrestonBlackburn/llm_citations)

A drawback to the structured output response is that I need to conform to json formatting rules (no inline citations), so I can’t insert citations until they are generated at the very end of the response with my current structure. Potentially there are other ways I could format my structured response object, but I’d still need to work around the json schema structure.

Example response format

```
class ResponseWithCitations(BaseModel):
    response: str
    citations: List[DocumentEnum]
```

We can get around this limitation, and return more flexible structures by using context free grammar instead of just JSON Schema/Pydantic.

### **Context Free Grammar (CFG) Citation Generation**

With context free grammar and constrained decoding we can start to create more complex grammar rules than just JSON schemas. With these techniques we can identify tokens that violate the rules and mask off the logits, so any invalid tokens will not be considered. This means that the output will be 100% compliant with the defined grammar. Constrained decoding is used to define the JSON structured outputs that we tested above. Unlike JSON Schema CFG can support recursive nested structures.

XGrammar has a post that goes into much more detail if you’re interested in learning more — [Achieving Efficient Flexible Portable Structured Generation with XGrammar](https://blog.mlc.ai/2024/11/22/achieving-efficient-flexible-portable-structured-generation-with-xgrammar)

If we look at the application of grammar rules and logits masking in the classic transformer architecture we would see that it it fits between the linear and softmax layers.

![Transformer architecture with grammar rule processor](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*mDGAJhANS-JnwyyA)

From a token perspective the flow might look like the diagram below. The grammar rules step shown above corresponds to the “Outlines regex logits processor” in the diagram.

![Example of token masking based on a rule set from the Outlines library documentation](https://miro.medium.com/v2/resize:fit:570/format:webp/0*hZKdj96yOLFjsTUs)

We can express these context-free grammars (CFGs) using EBNF (Extended Backus–Naur Form). This is how we can control what tokens do and don’t get filtered out in the above diagram. For our citation use case, an example is shown below where the _document_options_ are provided dynamically based on the available documents returned from RAG.

```
start: sentence+
sentence: TEXT citation TEXT*
citation: "[" NUMBER "]" "<" DOCUMENT ">"
%import common.NUMBER
%import common.WS
%import common.LETTER
%import common.WORD
%ignore WS
DOCUMENT: {document_options}
TEXT: /[^\\[]+/
```

With this logic wherever a citation occurs in the response (ex: [1]) then the next token must be a document provided from our returned RAG document options. This still doesn’t guarantee that the document name returned is correct, but could make our parsing and linking of the document in the UI more performant.

Various libraries support EBNF for CFG, like XGrammar and Outlines, however you may have already realized that you need access to the underlying model, so it won’t work with any OpenAI or other closed source models.

When testing the Outlines library I also ran into issues with providing EBNF rules using the Llama cpp python library, but was able to get it to work with the Transformers library. The only downside is that running local models is much slower and cloud hosting models are not economical at small scales.

### **Special Mention: Anthropic Citation Generation**

Anthropic’s Claude model actually has a native citations API available. It seems to do a simple RAG workflow where documents are chunked to sentences by default, or the user can upload their own documents. In the response each text block that is associated with a citation returns info about its source. We can see how this may be done in a similar way as the context free grammar rules we defined, but responses are returned by source in the API.

You can read more up on Anthropic’s citations [here](https://docs.anthropic.com/en/docs/build-with-claude/citations), but they don’t go deep into technical details.

### **Issues with Citations**

With structured outputs we are able to constrain the referenced documents returned, but citations are prone to hallucinations, just like any other LLM response. In the “[How well do LLMs cite relevant medical references](https://arxiv.org/abs/2402.02008)” paper, we can see that RAG helps citation performance, but for their medical questions use case they found that _“GPT-4 with retrieval augmented generation (RAG) and find that, even still, around 30% of individual statements are unsupported”,_ and from another chart in the paper around 25% of citations did not support the response (either incorrect or not related). For the time being we’ll need to make sure that users validate LLM responses and verify cited documents.

### **Takeaways**

There is still a ton to dig into related to context free grammar, and additional use cases related to SQL and coding responses. However, custom context free grammar is not very practical on a small scale since you’d need to host your own model. There is lots of activity in oss projects (Outlines, XGrammar), so I wouldn’t be surprised if OpenAI supports EBNF for defining CFG in the near future.

Structured outputs don’t show much performance loss vs standard responses, at least for these simple responses and short prompts. Even a small slowdown is most likely worth it for guaranteed selection of valid documents. While not directly related to citations, I also confirmed that OpenAI’s structured output endpoint supports streaming.

There are other more advanced citation strategies that I still have not explored. For example the [CiteFix](https://arxiv.org/abs/2504.15629) paper cross-checks generated citations against retrieved articles to improve citation accuracy. I haven’t dug into using knowledge graphs for citation generation either, but it can be done shown by this [KG-CTG](https://arxiv.org/pdf/2404.09763) paper.

For the time being I’ll go forward with structured outputs for my citations, but I’ll be holding out hope for EBNF support from OpenAI.

If you have any tips or approaches that you’ve had success with for citation generation I’d love to hear them!

Supporting code for citations and CFG on [GitHub](https://github.com/PrestonBlackburn/llm_citations)