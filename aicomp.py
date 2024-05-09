batchSize = 1
print("Importing AI, this might take a second")
from semantic_text_similarity.models import WebBertSimilarity
#from semantic_text_similarity.models import ClinicalBertSimilarity

web_model = WebBertSimilarity(device='cpu', batch_size=batchSize) #defaults to GPU prediction

#clinical_model = ClinicalBertSimilarity(device='cpu', batch_size=10) #defaults to GPU prediction
def AiCompare(answer, inputed):
    correlation = web_model.predict([(answer, inputed)])
    return correlation
