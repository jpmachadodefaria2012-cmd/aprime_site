from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Emoções
tristeza = ["triste", "chateado", "desanimado", "deprimido", "mal"]
alegria = ["feliz", "alegre", "contente", "otimista"]
ansiedade = ["ansioso", "ansiosa", "nervoso", "nervosa", "preocupado", "preocupada"]
frustracao = ["frustrado", "frustrada", "irritado", "irritada"]
medo = ["medo", "assustado", "assustada"]
motivacao = ["animado", "animada", "pronto", "pronta", "força"]

# Respostas de confirmação
confirmacao = ["sim", "ok", "beleza", "claro", "pode"]

# Frases por emoção (2 cada)
frases = {
    "tristeza": [
        "Entendo que tá difícil, mas tô contigo. Vamos superar isso juntos.",
        "Sei que não tá fácil, mas cada passo que você dá já é uma vitória."
    ],
    "alegria": [
        "Que bom que você está feliz! Isso me anima mais ainda.",
        "Sua felicidade contagia! Continue aproveitando esses momentos."
    ],
    "ansiedade": [
        "Calma, respira. Entendo sua ansiedade. Estamos juntos nisso.",
        "Sei que tá nervoso, mas respira fundo e vamos devagar."
    ],
    "frustracao": [
        "É normal se sentir frustrado, mas isso não te torna pior. Estamos juntos.",
        "Frustração acontece, mas você está aprendendo e crescendo com isso."
    ],
    "medo": [
        "Medo é natural. Vamos enfrentar isso juntos, com calma.",
        "Não se assuste, juntos conseguimos superar qualquer medo."
    ],
    "motivacao": [
        "Excelente energia! Vamos usar isso para melhorarmos cada vez mais.",
        "Continue motivado! Cada passo positivo conta."
    ],
}

# Sugestões para emoções que pedem ajuda
sugestoes = {
    "tristeza": "Tente escrever seus sentimentos ou conversar com alguém de confiança.",
    "ansiedade": "Faça exercícios de respiração ou uma caminhada para se acalmar.",
    "frustracao": "Tire um tempo para relaxar ou tente resolver o problema em pequenos passos.",
    "medo": "Enfrente devagar o que te assusta, sempre se apoiando em alguém confiável."
}

# Armazena última emoção detectada
ultima_emocao = None
aguardando_sugestao = False

def detectar_emocao(mensagem):
    msg = mensagem.lower()
    for emocao, palavras in [("tristeza", tristeza), ("alegria", alegria),
                             ("ansiedade", ansiedade), ("frustracao", frustracao),
                             ("medo", medo), ("motivacao", motivacao)]:
        if any(p in msg for p in palavras):
            return emocao
    return None

def resposta_aprime(mensagem):
    global ultima_emocao, aguardando_sugestao
    msg = mensagem.lower()

    # Se estiver esperando confirmação para sugestão
    if aguardando_sugestao:
        if any(c in msg for c in confirmacao):
            # Retorna sugestão específica
            sugestao = sugestoes.get(ultima_emocao, "")
            aguardando_sugestao = False
            return f"Aqui vai uma sugestão: {sugestao}"
        else:
            aguardando_sugestao = False
            return "Tudo bem, sem problemas. Se quiser depois, posso dar uma sugestão."

    emocao = detectar_emocao(msg)
    if emocao:
        ultima_emocao = emocao
        # Seleciona aleatoriamente entre as duas frases
        from random import choice
        frase = choice(frases[emocao])
        # Pergunta se quer sugestão para certas emoções
        if emocao in sugestoes:
            aguardando_sugestao = True
            return f"{frase} Quer que eu te dê uma sugestão para lidar com isso?"
        else:
            return frase
    else:
        return "Estou aqui com você. Me conta mais do que tá rolando."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensagem = data.get("mensagem", "")
    resposta = resposta_aprime(mensagem)
    return jsonify({"resposta": resposta})
import os


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Pega a porta do Render ou usa 5000 local
    app.run(host="0.0.0.0", port=port)
