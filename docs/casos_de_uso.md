# Documento de Casos de Uso

## Lista dos Casos de Uso

- [CDU 01](#cdu-01--fazer-login): Fazer login
- [CDU 02](#cdu-02--pesquisar-eventos): Pesquisar eventos
- [CDU 03](#cdu-03--visualizar-detalhes-de-evento): Visualizar detalhes de evento

## Lista dos Atores

- Usuário visitante (não autenticado)
- Usuário autenticado (cadastrado/logado)
- Administrador

## Descrição dos Casos de Uso

### CDU 01 – Fazer login

#### Atores: 
- Usuário autenticado
- Administrador

**Fluxo Principal**

1. O usuário seleciona a opção "Entrar".
2. O sistema solicita os dados de login (e-mail e senha).
3. O usuário insere os dados e confirma a operação.
4. O sistema valida as informações fornecidas.
5. O sistema autentica o usuário e redireciona para a tela de perfil.

**Fluxo Alternativo A**

1. Se os dados de login forem inválidos, o sistema apresenta a mensagem: "E-mail ou senha incorretos".

**Fluxo Alternativo B**

2. O usuário pode cancelar a operação clicando no botão "X", sendo redirecionado para a página principal.

### CDU 02 – Pesquisar eventos

#### Lista dos Atores 

- Usuário visitante (não autenticado)
- Usuário autenticado (cadastrado/logado)

**Fluxo Principal**

1. O usuário acessa a barra de pesquisa.
2. O usuário digita o nome do evento, artista ou palavra-chave.
3. O sistema processa a pesquisa.
4. O sistema exibe a lista de eventos que correspondem ao termo pesquisado.

**Fluxo Alternativo A**

1. Caso não existam eventos correspondentes, o sistema exibe a mensagem: "Nenhum evento encontrado".

### CDU 03 – Visualizar detalhes de evento

####  Atores 

- Usuário visitante (não autenticado)
- Usuário autenticado (cadastrado/logado)
  
**Fluxo Principal**

1. O usuário seleciona um evento da lista exibida.
2. O sistema exibe uma página de detalhes do evento contendo: nome, data, local, preço e acessibilidade.
3. O sistema também exibe as avaliações e comentários já feitos por outros usuários.

**Fluxo Alternativo A**

1. Caso as informações do evento estejam temporariamente indisponíveis, o sistema apresenta a mensagem: "Não foi possível carregar os detalhes do evento".
