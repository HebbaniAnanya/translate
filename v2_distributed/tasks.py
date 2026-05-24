from celery_app import celery_app
from models import TranslationalModel, User
from transformers import AutoModelForSeq2SeqLM, NllbTokenizer

# Map your clean API input strings directly to NLLB BCP-47 codes
LANG_MAP = {
    "english": "eng_Latn",
    "french": "fra_Latn",
    "spanish": "spa_Latn",
    "german": "deu_Latn",
    "hindi": "hin_Deva",
    "chinese": "zho_Hans"
}

print("Loading Facebook NLLB-200 weights into memory...")
MODEL_NAME = "facebook/nllb-200-distilled-600M"

# FIX 1: Use NllbTokenizer specifically, and initialize with default codes
tokenizer = NllbTokenizer.from_pretrained(
    MODEL_NAME, 
    src_lang="eng_Latn", 
    tgt_lang="fra_Latn"
)
translator = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def store_translation(t, current_user_username):
    user = User.get(User.username == current_user_username)
    model = TranslationalModel(
        user=user,
        text=t.text,
        base_lang=t.base_lang,   # Expects lowercase from main.py
        final_lang=t.final_lang
    )
    model.save()
    return model.id

@celery_app.task(name="tasks.run_translation")
def run_translation(t_id: int):
    model = TranslationalModel.get_by_id(t_id)
    
    # Retrieve language codes safely matching your LANG_MAP dictionary
    src_code = LANG_MAP.get(model.base_lang, "eng_Latn")
    tgt_code = LANG_MAP.get(model.final_lang, "fra_Latn")
    
    # FIX 2: Manually update the tokenizer's current targets before processing text
    tokenizer.src_lang = src_code
    tokenizer.tgt_lang = tgt_code
    
    # Tokenize the raw text (DO NOT pass text prefixes like "translate...")
    inputs = tokenizer(model.text, return_tensors="pt")
    
    # FIX 3: Force the generation layer to start tokenizing via target language vocab ID
    outputs = translator.generate(
        **inputs, 
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_code),
        max_length=512
    )
    
    # Decode integers back into regular characters
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Save the output to your database row
    model.translation = translation
    model.save()
    return f"Task {t_id} processed successfully"

def find_translation(t_id: int):
    try:
        model = TranslationalModel.get_by_id(t_id)
        return model.translation or "Processing check back later"
    except TranslationalModel.DoesNotExist:
        return "Task ID not found"