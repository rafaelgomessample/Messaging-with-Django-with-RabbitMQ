# Mensageria com Python, Django e RabbitMQ

Projeto de estudos sobre comunicação assíncrona entre serviços utilizando **RabbitMQ** como message broker, **Django** como framework web e **Pika** como cliente Python para o protocolo AMQP.

---

## Objetivo

Explorar na prática os conceitos de mensageria orientada a eventos, incluindo:

- Publicação e consumo de mensagens
- Exchanges do tipo **Topic**
- Filas duráveis e mensagens persistentes
- Acknowledgment e Nack com tratamento de erros
- Consumer workers via Django Management Commands

---

## Tecnologias

| Tecnologia | Versão |
|---|---|
| Python | 3.x |
| Django | 6.0.7 |
| Django REST Framework | 3.17.1 |
| Pika (AMQP client) | 1.4.1 |
| RabbitMQ | latest |
| python-decouple | 3.8 |

---

## Arquitetura de Mensageria

O projeto utiliza o padrão **Publish/Subscribe** com exchanges do tipo **Topic**, permitindo roteamento de mensagens por routing keys.

```
[API REST]
    │
    ▼
[EventPublisher]
    │
    ├──► orders_exchange  ──► orders.order_created       ──► order_created_handler
    │                    ──► orders.order_notification   ──► order_notification_handler
    │
    └──► payments_exchange ──► payments.payment_change_status  ──► payment_change_status_handler
                          ──► payments.payment_notification    ──► payment_notification_handler
```

### Exchanges

| Exchange | Tipo | Descrição |
|---|---|---|
| `orders_exchange` | topic | Eventos relacionados a pedidos |
| `payments_exchange` | topic | Eventos relacionados a pagamentos |

### Filas e Routing Keys

| Fila | Routing Key | Handler |
|---|---|---|
| `orders.order_created` | `orders.order_created` | Processa criação de pedido e dispara eventos de notificação e pagamento |
| `orders.order_notification` | `orders.order_notification` | Processa notificações de pedidos |
| `payments.payment_change_status` | `payments.payment_change_status` | Atualiza status de pagamento do pedido no banco |
| `payments.payment_notification` | `payments.payment_notification` | Processa notificações de pagamento |

---

## Fluxo de Eventos

1. Uma **ordem é criada** via API REST (`POST /orders/`)
2. O evento `orders.order_created` é publicado no `orders_exchange`
3. O consumer do pedido processa o evento:
   - Publica `orders.order_notification` → notificação por e-mail
   - Aguarda 10 segundos e publica `payments.payment_change_status`
4. O consumer de pagamentos atualiza o status do pedido no banco de dados
5. Em seguida, publica `payments.payment_notification` com o novo status

---

## Estrutura do Projeto

```
.
├── core/
│   ├── settings.py
│   └── messaging/
│       ├── connection.py      # Gerenciamento de conexão com RabbitMQ
│       ├── exchanges.py       # Declaração de exchanges (ExchangeEnum)
│       ├── publisher.py       # EventPublisher — publica eventos
│       └── consumer.py        # EventConsumer — consome eventos com ack/nack
├── orders/
│   ├── api/v1/                # Endpoints REST da app de pedidos
│   ├── handlers/
│   │   └── orders_handlers.py # Lógica de negócio dos eventos de pedidos
│   ├── management/commands/
│   │   └── start_consumer_order_event.py  # Worker de consumo
│   └── models/order_model.py
└── payments/
    ├── handlers/
    │   └── payments_handlers.py           # Lógica de negócio dos eventos de pagamentos
    └── management/commands/
        └── start_consumer_payment_event.py # Worker de consumo
```

---

## Como Executar

### Pré-requisitos

- Python 3.x
- RabbitMQ em execução (localmente ou via Docker)

```bash
docker run -d --hostname rabbitmq --name rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  rabbitmq:3-management
```

### Instalação

```bash
pip install -r requirements.txt
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

### Migrações

```bash
python manage.py migrate
```

### Iniciando os Consumers

Cada consumer deve ser executado em um terminal separado:

```bash
# Pedidos
python manage.py start_consumer_order_event order_created
python manage.py start_consumer_order_event order_notification

# Pagamentos
python manage.py start_consumer_payment_event payment_change_status
python manage.py start_consumer_payment_event payment_notification
```

### Iniciando o Servidor

```bash
python manage.py runserver
```

---

## Conceitos Abordados

- **Exchange Topic**: roteamento flexível de mensagens por padrões de routing key
- **Durable Queues & Persistent Messages**: mensagens sobrevivem a reinicializações do broker
- **Prefetch Count**: controle de throughput do consumer (`basic_qos`)
- **Manual Acknowledgment**: `basic_ack` em sucesso e `basic_nack` com `requeue=False` em falha
- **Management Commands Django**: consumers rodando como processos independentes
- **Separação de responsabilidades**: camada de mensageria desacoplada das apps Django
