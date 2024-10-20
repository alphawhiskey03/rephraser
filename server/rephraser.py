from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from enum import Enum

class SentenceLength(Enum):
    consise = "consise"
    elaborated = "elaborated"
    same = "the same length as the original"

class TempratureBasedOnTone(Enum):
    neutral = 0.3
    excited = 0.8
    calm = 0.4
    urgent = 0.7
    professional = 0.4
    witty = 0.9
    authoritative = 0.3

class Rephraser:
    def __init__(self):
        self.model_name="llama3.2:3b"
        self.whole_text_sentance_prompt_template = PromptTemplate.from_template(
        template=
        """
        Rephrase the following sentence while maintaining the same meaning. 
        The new sentence should be {sentence_length} words long.
        Adjust the tone to be {tone}.
        Provide only the rephrased sentence; do not include any other information, special characters, or escape sequences
        """
        )

        self.selected_text_rephrasing_template = PromptTemplate.from_template(
            """
            Rephrase the following part of the sentence while maintaining the original context
            Full sentence: {whole_text}
            Part to rephrase: {text}
            Desired tone: {tone}
            Desired length: {sentence_length}
            Provide only the rephrased sentence; do not include any other information, special characters, or escape sequences.
            """
        )
        

    def rephrase_whole_text(self,text,sentence_length,tone):
        llm = OllamaLLM(model=self.model_name, temperature = TempratureBasedOnTone[tone].value)
        whole_sentance_rephrasing_chain = self.whole_text_sentance_prompt_template | llm
        rephrased_text = whole_sentance_rephrasing_chain.invoke({"text": text, 
                                                                 "sentence_length": SentenceLength[sentence_length].value,
                                                                "tone": tone
                                                                })
        return rephrased_text
    
    def rephrase_selected_text(self,text,whole_text,sentence_length,tone):
        llm = OllamaLLM(model=self.model_name, temperature = TempratureBasedOnTone[tone].value)
        selected_text_rephrase_chain = self.selected_text_rephrasing_template | llm
        rephrased_text= selected_text_rephrase_chain.invoke({"text": text, "sentence_length": sentence_length, "tone": tone, "whole_text": whole_text})
        return rephrased_text



        

    