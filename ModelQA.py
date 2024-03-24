
"""
Установить!
pip install transformer
pip install annoy
pip install transformers[torch]
pip install -U sentence-transformers
"""
from annoy import AnnoyIndex
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import pickle as pkl
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


# Загрузка SBERT модели
data = pd.read_csv('output_new.csv')
question = list(data.question)
answer = list(data.answer)
sbert_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
sbert_model = SentenceTransformer(sbert_model_name)
with open('model_man.pkl', 'rb') as f:
    sbert_embeddings = pkl.load(f)
annoy_index = AnnoyIndex(len(sbert_embeddings[0]), 'angular')
annoy_index.load('Annoy_index_man')
sbert_embeddings = [torch.tensor(embedding) for embedding in sbert_embeddings]


def question_response(sbert_embeddings, inp_question):
    top_k_hits = 3
    question_embedding = sbert_model.encode(inp_question)

    corpus_ids, scores = annoy_index.get_nns_by_vector(question_embedding, top_k_hits, include_distances=True)
    hits = [{'corpus_id': id, 'score': 1 - ((score ** 2) / 2)} for id, score in zip(corpus_ids, scores)]
    hits_above_threshold = [hit for hit in hits if hit['score'] > 0.8]

    if hits_above_threshold:
        print("Возможные ответы на ваш вопрос:")
        for hit in hits_above_threshold:
            print("\t{:.3f}\t{}".format(hit['score'], question[hit['corpus_id']]))

        # Семантический поиск с SBERT
        correct_hits = util.semantic_search(question_embedding, sbert_embeddings, top_k=top_k_hits)[0]
        correct_hits_ids = [hit['corpus_id'] for hit in correct_hits]

        return answer[correct_hits_ids[0]]
    else:
        an = 'К сожалению, мы не поняли ваш вопрос. Возможно, вы имели в виду один из следующих вопросов:'
        #print("К сожалению, мы не поняли ваш вопрос. Возможно, вы имели в виду один из следующих вопросов:")
        for hit in hits[:3]:
            #print("\t{}".format(question[hit['corpus_id']]))
            an += '\n' + "\t{}".format(question[hit['corpus_id']])
        return an



print(question_response(sbert_embeddings, 'What does the chmod command do ?'))
