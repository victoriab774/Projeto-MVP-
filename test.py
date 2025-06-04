from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# Escopo da API do Google Forms
SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

# Autenticação
store = file.Storage("token.json")
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
    creds = tools.run_flow(flow, store)

# Conectar à API do Forms
form_service = discovery.build(
    "forms", "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

# Criação inicial do formulário (apenas título permitido)
form = form_service.forms().create(body={
    "info": {
        "title": "Questionário: Práticas de TI Verde"
    }
}).execute()

form_id = form["formId"]
print("📝 Formulário criado com sucesso!")
print(f"🔗 Link de edição: https://docs.google.com/forms/d/e/1FAIpQLSdAizWBQW1gHtRv5U8wAWJwZ3cCWVqe2yi-1imSVMpnUdVHhg/viewform")

# 🧾 Adicionar descrição e perguntas via batchUpdate

# Função para montar opções
def opcoes(lista):
    return [{"value": item} for item in lista]

# Descrição + perguntas
requests = [
    {
        "updateFormInfo": {
            "info": {
                "description": "Este formulário foi gerado automaticamente via API para levantamento de práticas de TI Verde. Por favor, responda todas as questões.",
            },
            "updateMask": "description"
        }
    }
]

# Lista das perguntas
perguntas = [
    {
        "titulo": "Qual é o seu cargo atual na organização?",
        "tipo": "RADIO",
        "opcoes": ["Analista de TI", "Desenvolvedor(a)", "Gestor(a) de TI", "Suporte Técnico", "Outros"]
    },
    {
        "titulo": "Há quanto tempo você trabalha na área de TI na organização atual?",
        "tipo": "RADIO",
        "opcoes": ["Menos de 1 ano", "1 a 5 anos", "6 a 10 anos", "11 anos ou mais"]
    },
    {
        "titulo": "Qual é o porte da organização onde você trabalha?",
        "tipo": "RADIO",
        "opcoes": ["Microempresa", "Pequena empresa", "Média empresa", "Grande empresa"]
    },
    {
        "titulo": "Qual é o principal setor de atuação da organização?",
        "tipo": "RADIO",
        "opcoes": ["Tecnologia da Informação", "Indústria", "Serviços", "Comércio", "Outro"]
    },
    {
        "titulo": "Qual é o modelo de trabalho da sua equipe atualmente?",
        "tipo": "RADIO",
        "opcoes": ["Presencial", "Híbrido", "Remoto"]
    },
    {
        "titulo": "A organização onde você trabalha possui políticas ou iniciativas de TI Verde documentadas?",
        "tipo": "RADIO",
        "opcoes": ["Sim", "Não", "Não sei informar"]
    },
    {
        "titulo": "Quais práticas de TI Verde são aplicadas em sua organização?",
        "tipo": "CHECKBOX",
        "opcoes": [
            "Reciclagem de equipamentos",
            "Virtualização de servidores",
            "Redução de impressões",
            "Cloud computing sustentável",
            "Equipamentos ecológicos",
            "Teletrabalho",
            "Outra(s)"
        ]
    },
    {
        "titulo": "No seu time, há alguma prática de TI Verde sendo aplicada regularmente?",
        "tipo": "RADIO",
        "opcoes": [
            "Sim, frequentemente",
            "Sim, ocasionalmente",
            "Não há práticas estruturadas",
            "Não sei informar"
        ]
    },
    {
        "titulo": "Com que frequência práticas de economia de energia são promovidas?",
        "tipo": "RADIO",
        "opcoes": ["Sempre", "Às vezes", "Raramente", "Nunca"]
    },
    {
        "titulo": "Você acredita que a adoção de TI Verde melhora a imagem da organização?",
        "tipo": "RADIO",
        "opcoes": [
            "Concordo totalmente",
            "Concordo parcialmente",
            "Neutro",
            "Discordo parcialmente",
            "Discordo totalmente"
        ]
    },
    {
        "titulo": "Quais benefícios a TI Verde traz para sua organização?",
        "tipo": "CHECKBOX",
        "opcoes": [
            "Redução de custos",
            "Melhoria da imagem institucional",
            "Cumprimento de normas ambientais",
            "Engajamento dos colaboradores",
            "Nenhum benefício percebido",
            "Outros"
        ]
    },
    {
        "titulo": "Quais barreiras você enxerga para a adoção de práticas de TI Verde?",
        "tipo": "RADIO",
        "opcoes": [
            "Falta de recursos financeiros",
            "Falta de conhecimento técnico",
            "Falta de interesse da gestão",
            "Dificuldade de adaptação",
            "Outras"
        ]
    },
    {
        "titulo": "Qual seria a principal ação para incentivar práticas de TI Verde no seu time?",
        "tipo": "RADIO",
        "opcoes": [
            "Treinamento",
            "Metas sustentáveis",
            "Tecnologias verdes",
            "Divulgação de boas práticas",
            "Outros"
        ]
    },
    {
        "titulo": "Você se sente motivado(a) a propor práticas de TI Verde no trabalho?",
        "tipo": "RADIO",
        "opcoes": ["Sim", "Talvez", "Não"]
    },
    {
        "titulo": "Quão interessado(a) você estaria em participar de projetos de TI Verde?",
        "tipo": "RADIO",
        "opcoes": [
            "Muito interessado(a)",
            "Interessado(a)",
            "Neutro",
            "Pouco interessado(a)",
            "Sem interesse"
        ]
    }
]

# Adiciona cada pergunta como nova requisição
for idx, p in enumerate(perguntas):
    tipo = "RADIO" if p["tipo"] == "RADIO" else "CHECKBOX"
    requests.append({
        "createItem": {
            "item": {
                "title": p["titulo"],
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": tipo,
                            "options": opcoes(p["opcoes"]),
                            "shuffle": False
                        }
                    }
                }
            },
            "location": {"index": idx}
        }
    })

# Enviar todas as perguntas e descrição de uma vez
form_service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
print("✅ Perguntas e descrição adicionadas com sucesso!")
