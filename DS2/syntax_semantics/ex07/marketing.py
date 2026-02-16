import sys

def marketing(operation):
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
    'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
    'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    set_clients = set(clients)
    set_participants = set(participants)
    set_recipients = set(recipients)

    if operation== 'call_center':
        return list(set_clients.difference(set_recipients))
    elif operation== 'potential_clients':
        return list(set_participants.difference(set_clients))
    elif operation== 'loyalty_program':
        return list(set_clients.difference(set_participants))
    else:
        raise ValueError("Wrong name")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    operation = sys.argv[1]

    print(marketing(operation))