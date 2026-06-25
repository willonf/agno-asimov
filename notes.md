Toda vez que uma classe Agno é instanciada pela primeira vez, as tools são incluídas no prompt inicial do Agno, passando uma descrição do cada uma faz.
A própria docstring do Python pode ser usada para essa "documentação" da tool.

Cada conversa no Agno é uma session. Sessions são stateless, ou seja, cada vez que o agente é executado a session anterior é deletada.


    Storage armazena histórico da sessão e memória.

