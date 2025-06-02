from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

tarefas = {}

class Tarefa(BaseModel):
    nome_tarefa: str
    descricao_tarefa: str
    concluida: bool = False

@app.post("/adicionar")
def adicionar_tarefa(tarefa: Tarefa):
    if tarefa.nome_tarefa in tarefas:
        raise HTTPException(status_code=400, detail="Essa tarefa já existe")
    else:
        tarefas[tarefa.nome_tarefa] = tarefa.dict()
        return {"message": "A tarefa foi criada com sucesso"}


@app.get("/tarefas")
def listar_tarefas():
    if not tarefas:
        raise HTTPException(status_code=400, detail="Não existe nenhuma tarefa")
    else:
        return {"Tarefas": tarefas}
    
@app.put("/atualizar/{nome_tarefa}")
def atualizar_conclusão(nome_tarefa: str, tarefa: Tarefa):
    if nome_tarefa not in tarefas:
        raise HTTPException(status_code=404, detail="Essa tarefa não existe no banco de dados")
    else:
        if tarefa.concluida == False:
           tarefas[nome_tarefa]['concluida'] = True
        else:
            tarefas[nome_tarefa]['concluida'] = False
            return tarefas[nome_tarefa]


@app.delete("/deletar/{nome_tarefa}")
def delete_tarefa(nome_tarefa: str):
    if nome_tarefa not in tarefas:
        raise HTTPException(status_code=404, detail="Essa tarefa não foi encontrada")
    else:
        del tarefas[nome_tarefa]
        return {"message": "A tarefa foi deletada"}