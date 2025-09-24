Creating Custom Parsers For LlamaIndex
======================================

Jun 17, 2024

![Custom Markdown Parsing With LlamaIndex](/static/img/blogs/creating-custom-parsers-for-llamaindex/llama_index_thumbnail.png)

LlamaIndex has some good built-in tools for most standard document parsing cases, but if you have more specific document splitting needs, you may need to create your own custom parser.

A custom parser should be fairly easy to add, but LlamaIndex doesn’t have any documentation for building custom parsers. There is a _NodeParser_ base class, but it is up to the user to navigate the code base and figure out how to use it. In this post, I’ll walk you through how I created my custom LlamaIndex parser.

If you want to skip all the writing and get straight to the code, you can check everything out in my [custom-llama-index-parser-example repo](https://github.com/PrestonBlackburn/custom-llama-index-parser-example) on GitHub.

The change I want to make to the default parser is small. Instead of splitting the document on each level of header, like the default parser, I want to be able to split the document at a heading level and group everything below it. It happens that heading level 2 is a good level to split on for the documents I’m analyzing. The image below shows an example of what the new parsing looks like.

![Grouping of header 2 and header 3 for the custom parser](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*TAvb6dOrPQf7hqD3)

Before we dig into the code, let’s take a look at how nodes and parsers work in LlamaIndex.

Background
----------

To understand how the custom node parser fits into to LlamaIndex we’ll take a look at splitters vs parsers and a basic Llama index flow.

**Splitters vs Parsers**

In the documentation, two main concepts are used when talking about splitting documents — splitters and parsers. Effectively, we can think of these concepts as mostly being the same thing. Both implement a _get_nodes_from_documents_ method that will return a list of nodes. They both eventually inherit from the _NodeParser_ class, but the splitters seem to have intermediate text splitter classes to handle more complex logic. As far as I can tell, that is the main difference.

*   **Node Parsers** — These classes inherit from the _NodeParser_ class. Node parsers are the default base parser for most files.
*   **Splitters** — These classes inherit from the _MetadataAwareTextSplitter,_ which inherits from the _TextSplitter_ class, and finally the_NodeParser_. The additional logic tries to split text in more advanced ways than the standard node parsers.

**Basic Llama Index Flow**

For simple use cases, the user needs to follow four steps in the LlamaIndex API.

1.  Read data to create “documents”. LlamaIndex refers to the source data before processing as documents, but we can immediately read the documents as nodes.
2.  Process nodes with a NodeParser or Splitter. This is where the main processing logic will be handled to create a new list of processed nodes.
3.  Now, we can create a vector store index from the parsed nodes we created.
4.  The vector store index can then be used for RAG queries.

To see an example of the custom node parser being used end to end, check out the [tests/test_end_to_end.py](https://github.com/PrestonBlackburn/custom-llama-index-parser-example/blob/main/tests/test_end_to_end.py) file.

Now that we know a little about what we are creating and how it fits into the wider scope of LlamaIndex, let’s take a look at the code.

The Code
--------

A natural starting point for us is the LlamaIndex [default markdown node parser](https://github.com/run-llama/llama_index/blob/891cc863ca80f7480ea4bdaeee9a37cebb57ba54/llama-index-core/llama_index/core/node_parser/file/markdown.py#L12).

The basic use of the MarkdowNodeParser looks like:

```
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.readers.file import FlatReader
from pathlib import Path
md_docs = FlatReader().load_data(Path("./test.md"))
parser = MarkdownNodeParser()
nodes = parser.get_nodes_from_documents(markdown_docs)
```

Where the _FlatReader_ returns the “document” as a node. Parsers and splitters typically get initialized and then call the _get_nodes_from_documents_ method on nodes created from files.

In the case of the _MarkdownNodeParser_, the get_nodes_from_documents method is inherited from the NodeParser base class and calls the _parse_nodes method from the _MarkdownNodeParser_ class.

Now we can focus on the __parse_nodes_ method as the endpoint for implementing our logic. However, we still need to see how the metadata for nodes is being added and how to add some user input to define the heading level to group on.

In the __build_node_from_split_ method the metadata for the nodes is added, and the new nodes are created. We’ll add the new node text and the metadata for the nodes in the g_et_nodes_from_node_ method called the __build_node_from_split_ method. A snippet is shown below:

```
  def get_nodes_from_node(self, node: BaseNode, **kwargs) -> List[TextNode]:
      """Get Nodes from document basedon headers"""
      text = node.get_content(metadata_mode=MetadataMode.NONE)
      markdown_nodes = []
      # heading level can get passed as kwargs
      headings = self._split_on_heading(text, **kwargs)
      headings_w_metadata = self._get_heading_text(headings, **kwargs)
      for heading, metadata in headings_w_metadata:
          markdown_nodes.append(self._build_node_from_split(heading, node, metadata))
      return markdown_nodes
```

Last, we want to specify the heading level we will group on to allow more flexibility in the grouping. The easiest way is to pass the heading grouping level as kwargs. Both the _get_nodes_from_documents_ and __parse_nodes_ methods already accept kwargs, so we can just continue to pass the headling_level kwarg down to the method that uses it. The newly created __split_on_heading_ and __get_heading_text_ methods will end up using the heading level parameter. For example:

```
  def _split_on_heading(self, document: str, heading_level: int = 2) -> List[str]:
      split_headings = []
      document = [document]
      for i in range(heading_level):
          split_on = "\n" + "#" * (i + 1) + " "
          split_headings.append(split_on)
      for current_level, heading in enumerate(split_headings):
          _logger.debug(f"splitting on: {heading}")
          document = self._document_splitter(heading, document, current_level)
      return document
```

Now we have the new splitting logic, new metadata, and new parameters added, and the custom node parser is ready to be used. Example usage:

```
from llama_index.readers.file import FlatReader
from pathlib import Path
md_docs = FlatReader().load_data(Path("example_source.md"))
print(md_docs)
print(len(md_docs))
parser = HeadingMarkdownNodeParser()
nodes = parser.get_nodes_from_documents(md_docs, heading_level=2)
print(nodes)
print(len(nodes))
assert len(nodes) == 5
```

If you want to create your own custom node parser, the example below will help you get started:

```
"""Custom Node Parser"""
from typing import Any, Dict, List, Optional, Sequence
from llama_index.core.callbacks.base import CallbackManager
from llama_index.core.node_parser.interface import NodeParser
from llama_index.core.node_parser.node_utils import build_nodes_from_splits
from llama_index.core.schema import BaseNode, MetadataMode, TextNode
from llama_index.core.utils import get_tqdm_iterable
class CustomNodeParser(NodeParser):
    """Your Custom Node Parser
    """
    @classmethod
    def from_defaults(
        cls,
        include_metadata: bool = True,
        include_prev_next_rel: bool = True,
        callback_manager: Optional[CallbackManager] = None,
    ) -> "CustomNodeParser":
        callback_manager = callback_manager or CallbackManager([])
        return cls(
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
        )
    @classmethod
    def class_name(cls) -> str:
        """Get class name."""
        return "CustomNodeParser"
    def _parse_nodes(
        self,
        nodes: Sequence[BaseNode],
        show_progress: bool = False,
        **kwargs: Any,
    ) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")
        for node in nodes_with_progress:
            nodes = self.get_nodes_from_node(node, **kwargs)
            all_nodes.extend(nodes)
        return all_nodes
    # ------------------------------------------------
    # ----------- <your custom logic here> -----------
    # ------------------------------------------------
    def get_nodes_from_node(self, node: BaseNode, **kwargs) -> List[TextNode]:
        """Get Nodes from document basedon headers"""
        text = node.get_content(metadata_mode=MetadataMode.NONE)
        markdown_nodes = []
        # <call your custom logic here>
        # Where - Heading is a string or the text for the node
        # and metadata is a dictionary of metadata for the node
        # text is the source text from the document
        for heading, metadata in your_text_and_metadata_tuple:
            markdown_nodes.append(self._build_node_from_split(heading, node, metadata))
        return markdown_nodes
    def _build_node_from_split(
        self,
        text_split: str,
        node: BaseNode,
        metadata: dict,
    ) -> TextNode:
        """Build node from single text split."""
        node = build_nodes_from_splits([text_split], node, id_func=self.id_func)[0]
        if self.include_metadata:
            node.metadata = {**node.metadata, **metadata}
        return node

```

Feel free to drop a comment if you have any questions or run into any issues.