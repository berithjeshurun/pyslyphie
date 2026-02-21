from typing import List, Dict, Any, Union, Optional, Literal
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA, LatentDirichletAllocation
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
import numpy as np
import logging, re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from ..utils import ContextUpdater
import fitz
import sys
import pytesseract
from PIL import Image, ExifTags
import io, os
pytesseract.pytesseract.tesseract_cmd = os.environ['TESSERACT_OCR'] # r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
def get_image_details(img: Image.Image) -> dict:
    """Return detailed info about a PIL Image"""
    details = {
        'format': img.format,
        'size': img.size,
        'mode': img.mode,
        'info': img.info,
        'bands': img.getbands(),
    }
    
    dpi = img.info.get('dpi', None)
    if dpi:
        details['dpi'] = dpi

    exif_data = {}
    if hasattr(img, '_getexif'):
        raw_exif = img._getexif()
        if raw_exif:
            for tag, value in raw_exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                exif_data[decoded] = value
    if exif_data:
        details['exif'] = exif_data

    return details


class TextPreprocessor:
    """Advanced text preprocessing with biblical text optimization"""
    
    def __init__(self, **kwargs):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        _old_eng_stpwrds = {'thou', 'thee', 'thy', 'thine', 'ye', 'hath', 'doth', 'saith', 'lo', 'behold'}
        self.stop_words.update(_old_eng_stpwrds)
        if kwargs.get('stopwords', None) != None :
            custom_stwds = kwargs.get('stopwords')
            if isinstance(custom_stwds, list) :
                if not len(custom_stwds) == 0 :
                    self.stop_words.update(set(custom_stwds))
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'[^\w\s\.\,\;\!\?\']', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """Tokenize text into sentences"""
        return sent_tokenize(text)
    
    def tokenize_words(self, text: str) -> List[str]:
        """Tokenize text into words"""
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stop words from tokens"""
        return [token for token in tokens if token not in self.stop_words]
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Stem tokens using Porter stemmer"""
        return [self.stemmer.stem(token) for token in tokens]

    def fit(self, model : Literal['tokenizer-word', 'tokenizer-sentence','stemmer', 'clean', 'formatize', 'stopwords'], text : str) :
        if model == 'clean' : return self.clean_text(text)
        elif model == 'tokenizer-word' : return self.tokenize_words(text)
        elif model == 'tokenizer-sentence' : return self.tokenize_sentences(text)
        elif model == 'stemmer' : return self.stem_tokens(self.tokenize_words(text))
        elif model == 'stopwords' : return self.remove_stopwords(self.tokenize_words(text))
        elif model == 'formatize' : return ' '.join(self.remove_stopwords(self.tokenize_words(self.clean_text(text)))).strip()
        else :
            return text.split(' ')


class VectorizationEngine:
    """Text to numerical data conversion engine"""
    
    def __init__(self):
        self.vectorizers : Dict[str, Union[TfidfVectorizer, CountVectorizer]] = dict()
        self.scaler = StandardScaler()
        
    def create_tfidf_vectorizer(self, name: str = 'default', **kwargs):
        """Create TF-IDF vectorizer"""
        default_params = {
            'max_features': 5000,
            'min_df': 2,
            'max_df': 0.8,
            'ngram_range': (1, 2),
            'stop_words': 'english'
        }
        default_params.update(kwargs)
        
        self.vectorizers[name] = TfidfVectorizer(**default_params)
        return self.vectorizers[name]
    
    def create_count_vectorizer(self, name: str = 'count', **kwargs):
        """Create Count vectorizer"""
        default_params = {
            'max_features': 5000,
            'min_df': 2,
            'max_df': 0.8,
            'ngram_range': (1, 2),
            'stop_words': 'english'
        }
        default_params.update(kwargs)
        
        self.vectorizers[name] = CountVectorizer(**default_params)
        return self.vectorizers[name]
    
    def fit_transform(self, texts: List[str], vectorizer_name: str = 'default') -> np.ndarray:
        """Fit and transform texts to vectors"""
        if vectorizer_name not in self.vectorizers:
            self.create_tfidf_vectorizer(vectorizer_name)
            
        return self.vectorizers[vectorizer_name].fit_transform(texts).toarray()
    
    def transform(self, texts: List[str], vectorizer_name: str = 'default') -> np.ndarray:
        """Transform texts using fitted vectorizer"""
        if vectorizer_name not in self.vectorizers:
            raise ValueError(f"Vectorizer {vectorizer_name} not found")
            
        return self.vectorizers[vectorizer_name].transform(texts).toarray()
    

class ModelCluster:
    """Cluster of sklearn models for comprehensive analysis"""
    
    def __init__(self):
        self.models = {}
        self.vectorization_engine = VectorizationEngine()
        
    def initialize_models(self):
        """Initialize all ML models"""
        self.models['random_forest'] = RandomForestClassifier(n_estimators=100, random_state=42)
        self.models['gradient_boosting'] = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.models['naive_bayes'] = MultinomialNB()
        self.models['svm'] = SVC(probability=True, random_state=42)
        self.models['xgboost'] = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
        self.models['catboost'] = CatBoostClassifier(verbose=False, random_state=42)
        
        self.models['kmeans'] = KMeans(n_clusters=5, random_state=42)
        self.models['dbscan'] = DBSCAN(eps=0.5, min_samples=5)
        
        self.models['lda'] = LatentDirichletAllocation(n_components=5, random_state=42)
        
    def train_classification_models(self, X, y):
        """Train classification models"""
        for name, model in self.models.items():
            if hasattr(model, 'fit') and name not in ['kmeans', 'dbscan', 'lda']:
                try:
                    model.fit(X, y)
                    logging.info(f"Trained {name} successfully")
                except Exception as e:
                    logging.error(f"Failed to train {name}: {e}")
    
    def cluster_data(self, X, method: str = 'kmeans'):
        """Cluster data using specified method"""
        if method in self.models:
            return self.models[method].fit_predict(X)
        else:
            raise ValueError(f"Clustering method {method} not found")

    def query_match(
        self,
        query: str,
        corpus: List[str],
        threshold: float = 0.9,
        vectorizer_name: str = 'default'
    ) -> List[str]:
        """Return items with similarity above threshold for a given query."""
        if vectorizer_name not in self.vectorization_engine.vectorizers:
            self.vectorization_engine.create_tfidf_vectorizer(vectorizer_name)
        vectorizer = self.vectorization_engine.vectorizers[vectorizer_name]
        X = vectorizer.fit_transform(corpus)
        q_vec = vectorizer.transform([query])
        
        similarities = cosine_similarity(q_vec, X)[0]
        results = [
            corpus[i]
            for i in range(len(corpus))
            if similarities[i] >= threshold
        ]
        return results
    

class ChunkingBase :
    '''
    ## `Chunks the text into required quantity`
    '''
    def __init__(self, web_logger_address = None):
        super().__init__()
        self.__web_log_register(web_logger_address)

    def __web_log_register(self, addr) :
        self.___addr = addr
    
    def chunk(self, text : str, chunk_size : int =1000, overlap : int =100):
        chunks = []
        start = 0
        t_len = len(text)
        with ContextUpdater(self.___addr) as cf :
            while start < t_len :
                end = start + chunk_size
                ch = text[start:end]
                cf.update({'mode' : 'SLYPH.DOC.R', 'message' : f'Analyzing document {round( end/ t_len * 100, 2) }%'})
                chunks.append({"text": ch, "start": start, "end": end})
                start = end - overlap
        return chunks


class ImageAnalyzer :
    def __init__(self, web_logger_address = None):
        super().__init__()
        self.__web_log_register(web_logger_address)
    def __web_log_register(self, addr) :
        self.___addr = addr
    
    def analyze(self, file_path : str, **kwargs) -> dict :
        """
        Converts a IMG (even scanned/image-based) to text using OCR.
        """
        text = 'No text Found'
        img = None
        with ContextUpdater(self.___addr) as cf :
            cf.update({'mode':'SLYPH.DOCR.INIT', 'message' : 'Analyzing...'})
            try :
                img = Image.open(file_path)
                text : str = pytesseract.image_to_string(img)
            except Exception as e :
                print(f"OCR failed on page for {file_path}: {e}")
        cf.terminate()
        if kwargs.get('export', None) == True :
            output_file =  kwargs.get('out', file_path.rsplit(".", 1)[0] + ".txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
        data = {'text' : text}
        if img != None and isinstance(img, Image.Image):
            data['meta'] = get_image_details(img)
        return data


class PDFAnalyzer :
    def __init__(self, web_logger_address = None):
        super().__init__()
        self.__web_log_register(web_logger_address)
    def __web_log_register(self, addr) :
        self.___addr = addr
    
    def analyze(self, file_path : str, **kwargs) -> str :
        """
        Converts a PDF (even scanned/image-based) to text using OCR.
        """
        full_text = []
        with ContextUpdater(self.___addr, ) as cf :
            cf.update({'mode':'SLYPH.DOCR.INIT', 'message' : 'Analyzing...'})
            doc = fitz.open(file_path)
            lt = len(doc)
            for page_num, page in enumerate(doc, start=1):
                cf.update({'mode':'SLYPH.DOCR.R', 'message' : f'Analyzing...{round(page_num / lt * 100, 2)}%'})
                text = page.get_text()
                if text.strip():
                    full_text.append(text)
                    continue
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes()))
                try:
                    text = pytesseract.image_to_string(img)
                    full_text.append(text)
                except Exception as e:
                    print(f"OCR failed on page {page_num}: {e}")
                    continue
        text = "\n".join(full_text)
        if kwargs.get('export', None) == True :
            output_file =  kwargs.get('out', file_path.rsplit(".", 1)[0] + ".txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
        return text