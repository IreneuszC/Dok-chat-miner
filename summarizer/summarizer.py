from langchain_openai import ChatOpenAI
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document
from prompts_templates import map_template, stuff_template, reduce_template


class Summarizer:
    def __init__(
        self, open_ai_api_key: str, chunk_size=10000, chunk_overlap=500
    ) -> None:
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo-1106", temperature=0.1, api_key=open_ai_api_key
        )
        self.max_tokens = 10000  # gpt-3.5-turbo-1106 has 16K window size so 10k should be enough to left 6k for response
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n"],
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

        return text_splitter.create_documents([text])

    def summarize_very_long_text(self, text: str) -> str:
        reduce_prompt = PromptTemplate.from_template(reduce_template)
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=self.llm, prompt=map_prompt)
        reduce_chain = LLMChain(llm=self.llm, prompt=reduce_prompt)
        docs = self.split_text(text)

        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="docs"
        )

        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=combine_documents_chain,
            collapse_documents_chain=combine_documents_chain,
            token_max=self.max_tokens,
        )

        map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=map_chain,
            reduce_documents_chain=reduce_documents_chain,
            document_variable_name="docs",
            return_intermediate_steps=False,
        )

        return map_reduce_chain.run(docs)

    def summarize_short_text(self, text: str) -> str:
        prompt = PromptTemplate.from_template(stuff_template)

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        stuff_chain = StuffDocumentsChain(
            llm_chain=llm_chain, document_variable_name="docs"
        )

        return stuff_chain.run(text)

    def get_num_tokens(self, text: str) -> int:
        return self.llm.get_num_tokens(text)

    def summarize(self, text: str) -> str:
        tokens = self.get_num_tokens(text)

        if tokens > self.max_tokens:
            return self.summarize_very_long_text(text)

        return self.summarize_short_text(text)
