import types
from rwkv.model import RWKV
from rwkv.utils import PIPELINE

CHUNK_LEN = 256  # split input into chunks to save VRAM (shorter -> slower, but saves VRAM)

# RWKV模型配置
args = types.SimpleNamespace()
args.strategy = "cuda fp16"  # use CUDA, fp16
args.MODEL_NAME = "model/RWKV-x060-World-1B6-v2.1-20240328-ctx4096"

print(f"Loading model - {args.MODEL_NAME}")
model = RWKV(model=args.MODEL_NAME, strategy=args.strategy)
pipeline = PIPELINE(model, "rwkv_vocab_v20230424")

model_tokens = []
model_state = None

def run_rnn(ctx):
    global model_tokens, model_state

    ctx = ctx.replace("\r\n", "\n")
    tokens = pipeline.encode(ctx)
    tokens = [int(x) for x in tokens]
    model_tokens += tokens

    while len(tokens) > 0:
        out, model_state = model.forward(tokens[:CHUNK_LEN], model_state)
        tokens = tokens[CHUNK_LEN:]

    return out

if model_state is None:  # 使用初始提示
    init_ctx = "User: hi\n\nAssistant: Hi. I am your assistant and I will provide expert full response in full details. Please feel free to ask any question and I will always answer it.\n\n"
    run_rnn(init_ctx)

def generate_response(message):
    global model_tokens, model_state

    GEN_TEMP = 1.0
    GEN_TOP_P = 0.3
    GEN_alpha_presence = 0.5
    GEN_alpha_frequency = 0.5
    GEN_penalty_decay = 0.996

    msg = "User: " + message + "\n\nAssistant:"
    out = run_rnn(msg)
    occurrence = {}
    out_tokens = []
    out_last = 0

    response = ""
    for i in range(99999):
        for n in occurrence:
            out[n] -= GEN_alpha_presence + occurrence[n] * GEN_alpha_frequency  # repetition penalty
        out[0] -= 1e10  # disable END_OF_TEXT

        token = pipeline.sample_logits(out, temperature=GEN_TEMP, top_p=GEN_TOP_P)
        out, model_state = model.forward([token], model_state)
        model_tokens += [token]
        out_tokens += [token]

        for xxx in occurrence:
            occurrence[xxx] *= GEN_penalty_decay
        occurrence[token] = 1 + (occurrence[token] if token in occurrence else 0)

        tmp = pipeline.decode(out_tokens[out_last:])
        if ("\ufffd" not in tmp) and (not tmp.endswith("\n")):
            response += tmp
            out_last = i + 1

        if "\n\n" in tmp:
            response += tmp
            break

    return response.strip()
