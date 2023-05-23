
# Sobre:

Projeto desenvolvido em Python com Django. As tecnologias utilizadas foram:` brotli, dj-database-url, djangorestframework, djangorestframework-simplejwt, drf-spectacular, gunicorn, ipython, psycopg2-binary, python-dotenv, whitenoise.`
Esse serviço possui uma API REST para que seja possível criar, logar, listar, editar e deletar usuários e usuários administradores. Os usuários podem cadastrar e editar o endereço em uma tabela relacionada. Os usuários também podem ser vendedores ou não (padrão). Vendedores podem cadastrar e editar produtos, bem como listá-los. Todos os usuários podem adicionar itens ao carrinho pelo id do produto inserindo a quantidade desejada. É possível realizar pedidos e os vendedores responsáveis por cada pedido podem editar o status do mesmo. Por padrão, a aplicação informa o status do pedido via e-mail sempre que ele é atualizado.

- O banco de dados utilizado foi **PostgreSQL**.

# Documentação:

<a href="https://ecommerce-g35.onrender.com/api/docs/swagger/" target="_blank">CLIQUE AQUI PARA ABRIR A DOCUMENTAÇÃO</a>

# Instruções:

- Para iniciar faça uma cópia do arquivo ".env.example", crie um Banco de Dados, preencha os campos necessários e nomeie o arquivo copiado para ".env".

### Crie o ambiente virtual

```
python -m venv venv
```

### Ative o venv

```bash
# linux:
source venv/bin/activate

# windows
source venv/Scripts/activate
```

### Instale as dependências

```
pip install -r requirements.txt
```

### Execute as migrações

```
python manage.py migrate
```

### Rode o servidor

```
python manage.py runserver
```

#

# Endpoints do serviço

### User

| Método | Endpoint                | Responsabilidade                        |
| ------ | ----------------------- | --------------------------------------- |
| POST   | /api/users/             | Criar usuário                           |
| POST   | /api/users/login/       | Logar usuário                           |
| GET    | /api/users/             | Listar usuários                         |
| GET    | /api/users/id/          | Listar usuário por id                   |
| PATCH  | /api/users/id/          | Atualizar usuário por id                |
| PATCH  | /api/users/activate/id/ | Ativa usuário no banco pelo id          |
| DELETE | /api/users/id/          | Realizar soft delete no usuário pelo id |

#

### Product

| Método | Endpoint          | Responsabilidade         |
| ------ | ----------------- | ------------------------ |
| POST   | /api/products/    | Cadastrar produto        |
| GET    | /api/products/    | Listar todos os produtos |
| GET    | /api/products/id/ | Listar produto por id    |
| PATCH  | /api/products/id/ | Atualizar produto por id |

#

### Cart

| Método | Endpoint              | Responsabilidade                 |
| ------ | --------------------- | -------------------------------- |
| PATCH  | /api/cart/product/id/ | Inserir produto (id) ao carrinho |
| PATCH  | /api/cart/clear/id/   | Limpar carrinho(id)              |

#

### Order

| Método | Endpoint                   | Responsabilidade           |
| ------ | -------------------------- | -------------------------- |
| POST   | /api/users/orders/         | Criar ordem(pedido)        |
| GET    | /api/users/orders/selling/ | Listar ordens de venda     |
| GET    | /api/users/orders/buying/  | Listar ordens de compra    |
| PATCH  | /api/orders/id/            | Atualizar status do pedido |

#

### Address

| Método | Endpoint               | Responsabilidade           |
| ------ | ---------------------- | -------------------------- |
| PATCH  | /api/users/address/id/ | Atualizar/inserir endereço |

#

## Requisitos do Serviço

### **User**

### POST: /api/users/

- É possível criar um usuário contendo os seguintes dados:
  - **username**: string.
  - **password**: string.
  - **email**: string.
  - **is_seller**: default=false.
  - **is_superuser**: default=false.
  - **address**: {
    **street**: string,
    **number**: string,
    **po**: string,
    **city**: string,
    **country**: string,
    **state**:string,
    **complement**: string
    }
  - **first_name**: string.
  - **last_name**: string.

**Exemplo de envio**:

```json
{
  "username": "first_user",
  "password": "Aa1234",
  "email": "testehj@mail.com",
  "address": {
    "street": "teste",
    "number": "100",
    "po": "10000-000",
    "city": "Kenzielândia",
    "country": "Brasil",
    "state": "Paraná",
    "complement": "Seguindo reto onde o tiro fez curva."
  },
  "first_name": "second",
  "last_name": "user"
}
```

**Retorno**:

```json
{
  "id": "b8adb9a5-1341-4973-968f-47d7ab3142fe",
  "username": "first_user",
  "email": "testehj@mail.com",
  "first_name": "second",
  "last_name": "user",
  "is_superuser": false,
  "is_seller": false,
  "cart": {
    "id": 1,
    "total_price": "0.00",
    "items": 0,
    "products": []
  },
  "address": {
    "id": 1,
    "street": "teste",
    "number": "100",
    "po": "10000-000",
    "city": "Kenzielândia",
    "country": "Brasil",
    "state": "Paraná",
    "complement": "Seguindo reto onde o tiro fez curva."
  }
}
```

- Não é possível criar um usuário com username ou email que já estejam cadastrados

**Exemplo de envio**:

```json
{
  "username": "first_user",
  "password": "Aa1234",
  "email": "testehj@mail.com",
  "address": {
    "street": "teste",
    "number": "100",
    "po": "10000-000",
    "city": "Kenzielândia",
    "country": "Brasil",
    "state": "Paraná",
    "complement": "Seguindo reto onde o tiro fez curva."
  },
  "first_name": "second",
  "last_name": "user"
}
```

**Exemplo de retorno**:

```json
{
  "username": ["A user with that username already exists."],
  "email": ["This field must be unique."]
}
```

- Os campos username, password, email e address são obrigatórios

**Exemplo de envio**:

```json
{
    {
	    "first_name": "second",
	    "last_name": "user"
    }
}
```

**Exemplo de retorno**:

```json
{
  "username": ["This field is required."],
  "email": ["This field is required."],
  "password": ["This field is required."],
  "address": ["This field is required."]
}
```

### POST: /api/users/login/

- É possível logar um usuário inserindo os seguintes dados:
  - **username**: string.
  - **password**: string.

**Exemplo de envio**:

```json
{
  "username": "first_user",
  "password": "Aa1234"
}
```

**Exemplo de retorno**:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NDE2OTU1OCwiaWF0IjoxNjgzNTY0NzU4LCJqdGkiOiJjYTQ1MTBlNjRjNzg0NmZlYmJmMTE2YTgzZWFiNWY2YyIsInVzZXJfaWQiOiI4OGY4ZmY1Ny1jZDUyLTQ0MTAtODNmZC1lMDhjMmM0ZmQ3YjUifQ.ogQAZ45WXi7U4q8iFYzaDSDEN2KmU7Zx-8v_VvxDWlY",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgzNjE4NzU4LCJpYXQiOjE2ODM1NjQ3NTgsImp0aSI6IjQzMjZkM2IyMmFkYjRlZDA5NzQ5YmIxMWZiNzg3NDE1IiwidXNlcl9pZCI6Ijg4ZjhmZjU3LWNkNTItNDQxMC04M2ZkLWUwOGMyYzRmZDdiNSJ9.mLKuZad4B3uwUb6ECwXmr8o8KbGdMfde6lhs_1po8QY"
}
```

- Não é possível fazer o login com username ou password invalidos

**Exemplo de envio**:

```json
{
  "username": "fi_user",
  "password": "Aa1234"
}
```

**Exemplo de retorno**:

```json
{
  "detail": "No active account found with the given credentials"
}
```

- Os campos username e password são obrigatórios

**Exemplo de envio**:

```json
{}
```

**Exemplo de retorno**:

```json
{
  "username": ["This field is required."],
  "password": ["This field is required."]
}
```

### GET: /api/users/

- É possível listar todos os usuários
  - **não há corpo na requisição**
  - **token**: Bearer {token}

**Exemplo de retorno**:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "88f8ff57-cd52-4410-83fd-e08c2c4fd7b5",
      "username": "first_user",
      "email": "firsuser@mail.com",
      "first_name": "first",
      "last_name": "user",
      "is_superuser": false,
      "is_seller": false,
      "cart": {
        "id": 1,
        "total_price": "0.00",
        "items": 0,
        "products": []
      },
      "address": {
        "id": 1,
        "street": "teste",
        "number": "100",
        "po": "10000-000",
        "city": "Kenzielândia",
        "country": "Brasil",
        "state": "Paraná",
        "complement": "Seguindo reto onde o tiro fez curva."
      }
    }
  ]
}
```

- A API acusa erro caso não seja enviado o token de acesso.

**Exemplo de retorno**:

```json
{
  "detail": "Authorization header must contain two space-delimited values",
  "code": "bad_authorization_header"
}
```

### GET: /api/users/id/

- É possível listar os usuários por id
  - **não há corpo na requisição**
  - **token**: Bearer {token}

**Exemplo de retorno**:

```json
{
  "id": "88f8ff57-cd52-4410-83fd-e08c2c4fd7b5",
  "username": "first_user",
  "email": "firsuser@mail.com",
  "first_name": "first",
  "last_name": "user",
  "is_superuser": false,
  "is_seller": false,
  "cart": {
    "id": 1,
    "total_price": "0.00",
    "items": 0,
    "products": []
  },
  "address": {
    "id": 1,
    "street": "teste",
    "number": "100",
    "po": "10000-000",
    "city": "Kenzielândia",
    "country": "Brasil",
    "state": "Paraná",
    "complement": "Seguindo reto onde o tiro fez curva."
  }
}
```

- A API acusa erro caso não seja enviado o token de acesso.

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

- A API acusa erro caso o usuário não exista.

```json
{
  "detail": "Not found."
}
```

### PATCH: /api/users/id/

- É possível editar um usuário por id:
  - **username**: string.
  - **password**: string.
  - **email**: string.
  - **is_seller**: boolean

**Exemplo de envio**:

```json
{
  "username": "primeiro_usuário",
  "password": "Aa1234",
  "email": "primeirousuario@mail.com",
  "is_seller": true
}
```

**Exemplo de retorno**:

```json
{
  "id": "88f8ff57-cd52-4410-83fd-e08c2c4fd7b5",
  "username": "primeiro_usuário",
  "email": "primeirousuario@mail.com",
  "first_name": "first",
  "last_name": "user",
  "is_superuser": false,
  "is_seller": true,
  "cart": {
    "id": 1,
    "total_price": "0.00",
    "items": 0,
    "products": []
  },
  "address": {
    "id": 1,
    "street": "teste",
    "number": "100",
    "po": "10000-000",
    "city": "Kenzielândia",
    "country": "Brasil",
    "state": "Paraná",
    "complement": "Seguindo reto onde o tiro fez curva."
  }
}
```

- A API acusa erro caso o usuário não exista.

```json
{
  "detail": "Not found."
}
```

- A API acusa erro caso não seja enviado o token de acesso.

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### PATCH: /api/users/activate/id/

- A API acusa erro caso o usuário não exista.

```json
{
  "detail": "Not found."
}
```

### DELETE: /api/users/id/

- É possível deletar um usuário por id

- A API acusa erro caso o usuário não exista.

```json
{
  "detail": "Not found."
}
```

- Caso tente deleter um usuário que possua ordens abertas a API retorna o seguinte erro:

**Exemplo de retorno**:

```json
{
  "message": "This user has unfinished orders."
}
```

### **Product**

### POST: /api/products/

- É possível cadastrar um produto contendo os seguintes dados:
  - **name**: string.
  - **category**: string.
  - **stock**: number.
  - **price**: number.

**Exemplo de envio**:

```json
{
  "name": "Produto Teste 4",
  "category": "Teste",
  "stock": 100,
  "price": 2000.0
}
```

**Exemplo de retorno**:

```json
{
  "id": 1,
  "name": "Produto Teste 4",
  "category": "Teste",
  "stock": 100,
  "price": "2000.00",
  "availability": true,
  "seller_id": "88f8ff57-cd52-4410-83fd-e08c2c4fd7b5"
}
```

- Se um usuário que não é vendedor tentar cadastrar um produto a seguinte mensagem de erro é retornada:

**Exemplo de retorno**:

```json
{
  "detail": "You are not registered as a seller."
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

- Os dados são obrigatórios:

**Exemplo de envio**:

```json
{}
```

**Exemplo de retorno**:

```json
{
  "name": ["This field is required."],
  "category": ["This field is required."],
  "stock": ["This field is required."],
  "price": ["This field is required."]
}
```

### GET: /api/products/

- É possível listar todos os produtos:

**Exemplo de retorno**:

```json
{
  "count": 13,
  "next": "http://127.0.0.1:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Televisão",
      "category": "Eletrodomésticos",
      "stock": 100,
      "price": "1320.99",
      "availability": true,
      "seller_id": "88f8ff57-cd52-4410-83fd-e08c2c4fd7b5"
    },
    {
      "id": 2,
      "name": "Pc",
      "category": "Eletrodomésticos",
      "stock": 100,
      "price": "1320.99",
      "availability": true,
      "seller_id": "88f8ff57-cd52-4410-83fd-e08c2c4fd7b5"
    }
  ]
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### GET: /api/products/id/

- É possível listar os produtos por id:

**Exemplo de retorno**:

```json
{
  "id": 10,
  "name": "Produto teste",
  "category": "Eletrodomésticos",
  "stock": 100,
  "price": "1320.99",
  "availability": true,
  "seller_id": "88f8ff57-cd52-4410-83fd-e08c2c4fd7b5"
}
```

- Se o produto pesquisado não existir a API retorna um erro:

**Exemplo de retorno**:

```json
{
  "detail": "Not found."
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### PATCH: /api/products/id/

- É possível editar os produtos por id:

**Exemplo de envio**:

```json
{
  "category": "Update teste",
  "stock": 90
}
```

**Exemplo de retorno**:

```json
{
  "id": 1,
  "name": "Produto Teste 4",
  "category": "Update teste",
  "stock": 90,
  "price": "2000.00",
  "availability": true,
  "seller_id": "88f8ff57-cd52-4410-83fd-e08c2c4fd7b5"
}
```

- Caso o usuário logado não tenha permissão para editar o produto:

**Exemplo de retorno**:

```json
{
  "detail": "You do not have permission to perform this action."
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### **Cart**

### PATCH: /api/cart/product/id/

- É possível adicionar produtos ao carrinho inserindo o id do produto por parâmetro e a quantidade no corpo da requisição:

**Exemplo de envio**:

```json
{
  "quantity": 1
}
```

**Exemplo de retorno**:

```json
{
  "id": 5,
  "total_price": "1320.99",
  "items": 1,
  "products": [
    {
      "id": 1,
      "name": "Televisão",
      "category": "Eletrodomésticos",
      "price": "1320.99",
      "seller_id": "88f8ff57-cd52-4410-83fd-e08c2c4fd7b5",
      "availability": true
    }
  ]
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

- A quantidade de itens é obrigatória:

**Exemplo de envio**:

```json
{}
```

**Exemplo de retorno**:

```json
{
  "detail": "You must inform a valid quantity for the item."
}
```

### PATCH: /api/cart/clear/id/

- Sem corpo na requisição

**Exemplo de retorno**:

```json
{
  "id": 1,
  "total_price": "0.00",
  "items": 0,
  "products": []
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### **Order**

### POST: /api/users/orders/

- É possível criar ordens caso o carrinho tenha produtos inseridos
- Não há corpo na requisição
- Caso o carrinho esteja vazio:

**Exemplo de retorno**:

```json
{
  "message": "Your cart is empty."
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### GET: /api/users/orders/selling/

- É possível listar as orders de venda:

**Exemplo de retorno**:

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 187,
      "order_status": "PEDIDO REALIZADO",
      "total_price": "4000.00",
      "created_at": "2023-05-09T20:58:11.770566Z",
      "product": [
        {
          "id": 14,
          "name": "Produto Teste 4",
          "category": "Teste",
          "price": "2000.00",
          "seller_id": "27c1528d-8940-4dba-bd82-c14dfccbc559",
          "availability": true
        },
        {
          "id": 15,
          "name": "Produto Teste 4",
          "category": "Teste",
          "price": "2000.00",
          "seller_id": "27c1528d-8940-4dba-bd82-c14dfccbc559",
          "availability": true
        }
      ]
    },
    {
      "id": 187,
      "order_status": "PEDIDO REALIZADO",
      "total_price": "4000.00",
      "created_at": "2023-05-09T20:58:11.770566Z",
      "product": [
        {
          "id": 14,
          "name": "Produto Teste 4",
          "category": "Teste",
          "price": "2000.00",
          "seller_id": "27c1528d-8940-4dba-bd82-c14dfccbc559",
          "availability": true
        },
        {
          "id": 15,
          "name": "Produto Teste 4",
          "category": "Teste",
          "price": "2000.00",
          "seller_id": "27c1528d-8940-4dba-bd82-c14dfccbc559",
          "availability": true
        }
      ]
    }
  ]
}
```

- Caso não tenha ordens:

**Exemplo de retorno**:

```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### GET: /api/users/orders/buying/

- É possível listar as orders de compra:

**Exemplo de retorno**:

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 184,
      "order_status": "PEDIDO REALIZADO",
      "total_price": "2641.98",
      "created_at": "2023-05-09T13:44:05.317355Z",
      "product": [
        {
          "id": 3,
          "name": "Pc 2",
          "category": "Eletrodomésticos",
          "price": "1320.99",
          "seller_id": "f05b0351-414e-466f-b981-72aa192ed594",
          "availability": true
        },
        {
          "id": 4,
          "name": "Pc 21323123",
          "category": "Eletrodomésticos",
          "price": "1320.99",
          "seller_id": "f05b0351-414e-466f-b981-72aa192ed594",
          "availability": true
        }
      ]
    },
    {
      "id": 185,
      "order_status": "PEDIDO REALIZADO",
      "total_price": "2641.98",
      "created_at": "2023-05-09T20:53:12.957520Z",
      "product": [
        {
          "id": 4,
          "name": "Pc 21323123",
          "category": "Eletrodomésticos",
          "price": "1320.99",
          "seller_id": "f05b0351-414e-466f-b981-72aa192ed594",
          "availability": true
        },
        {
          "id": 6,
          "name": "Pc 2132asdasdas3123",
          "category": "Eletrodomésticos",
          "price": "1320.99",
          "seller_id": "f05b0351-414e-466f-b981-72aa192ed594",
          "availability": true
        }
      ]
    }
  ]
}
```

- Caso não tenha ordens:

**Exemplo de retorno**:

```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### PATCH: /api/users/orders/id/

- É possível editar o status do pedido.

**Exemplo de retorno**:

```json
{
  "id": 1,
  "order_status": "ENTREGUE",
  "total_price": "4000.00",
  "created_at": "2023-05-10T16:49:58.468329Z",
  "product": [
    {
      "id": 1,
      "name": "Produto Apresentacao",
      "category": "Update teste",
      "price": "2000.00",
      "seller_id": "1c4caacf-0a59-409f-99b6-ff06cd88167c"
    }
  ]
}
```

### **Address**

### PATCH: /api/users/address/id/

- É possível inserir ou editar o endereço do usuário.

**Exemplo de retorno**:

```json
{
  "id": 5,
  "street": "testando 1",
  "number": "100",
  "po": "10000-000",
  "city": "Kenzielândia",
  "country": "Brasil",
  "state": "Paraná",
  "complement": "Seguindo reto onde o tiro fez curva."
}
```

- Caso endereço passado por parâmetro seja de outro usuário:

**Exemplo de retorno**:

```json
{
  "detail": "You do not have permission to perform this action."
}
```

- Caso o token inserido seja inválido:

**Exemplo de retorno**:

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```
# Integrantes:

### Gabryel Martins - Scrum Master

- linkedin: https://www.linkedin.com/in/gabryelmaraujo/

### Gustavo Gussoni - Tech Leader

- linkedin: https://www.linkedin.com/in/gustavogussoni/

### Kelly Cristina - Code Reviewer

- linkedin: https://www.linkedin.com/in/kelly-cristina-galliani/

### Pablo Silva - Code Reviewer

- linkedin: https://www.linkedin.com/in/pablo-silva-96901798/
