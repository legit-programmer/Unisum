from transformers import pipeline
from PIL import Image, ImageDraw
import pytesseract
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain import HuggingFaceHub
from langchain.docstore.document import Document
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get('TOKEN')
llm = HuggingFaceHub(repo_id='facebook/bart-large-cnn',
                     model_kwargs={'temperature': 2}, huggingfacehub_api_token=TOKEN)


class ImageFile:
    def __init__(self) -> None:
        self.file = None

def ocr(file):
    pytesseract.pytesseract.tesseract_cmd = os.path.join(
        os.getcwd(), 'tesseract/tesseract.exe')

    result = pytesseract.image_to_string(file)
    return result


def saveTextAsImage(text: str):
    arr = text.split()
    count = 0
    mainText = ''
    for i in arr:
        if count >= 20:
            mainText = mainText + '\n' + i
            count = 0
        mainText = mainText + ' ' + i
        count += 1

    img = Image.new('RGB', (1000, 1000), (255, 255, 255))
    d1 = ImageDraw.Draw(img)
    d1.text((1, 1), mainText.encode('utf-8'), fill=(255, 0, 0))
    ImageFile.file = img
    ImageFile.file.show()


def getTextFromDotTxt(file):
    return str(file.read())[2:-1]


def getTextSummarization(TEXT: str):

    model = HuggingFaceHub(repo_id='facebook/bart-large-cnn',
                           model_kwargs={'temperature': 0, 'min_length': 100, 'max_length': 500}, huggingfacehub_api_token=TOKEN)
    text_splitter = CharacterTextSplitter()
    chunks = text_splitter.split_text(TEXT)
    doc = []
    for text in chunks:
        doc.append(Document(page_content=text))
    print(doc)
    # docs = [Document(page_content=text) for text in chunks]
    summary_chain = load_summarize_chain(model, 'map_reduce')
    result = summary_chain.run(doc)
    return [{"summary_text": result}]


def getAnswerFromImage(_question):
    model = pipeline("document-question-answering",
                     model="naver-clova-ix/donut-base-finetuned-docvqa")
    return model(image=ImageFile.file, question=_question)


def summarizeFromIllustration(file):

    image_to_text = pipeline(
        "image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    return image_to_text(file)
