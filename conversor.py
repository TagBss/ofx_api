from decimal import Decimal


# Função para processar os dados OFX
def process_ofx(ofx_data):
    json = {
        "Instituicao banco": ofx_data.account.institution.organization,
        "Agencia": ofx_data.account.routing_number,                                                    # O número de roteamento do banco
        "Tipo de conta": ofx_data.account.type,                                                        # Um objeto Tipo de conta
        "Numero da conta": ofx_data.account.account_id,                                                # O número da conta
        "Start date": ofx_data.account.statement.start_date.strftime('%d/%m/%Y %H:%M:%S'),             # A data de início das transações
        "End date": ofx_data.account.statement.end_date.strftime('%d/%m/%Y %H:%M:%S'),                 # A data final das transações
        "balance (saldo)": float(ofx_data.account.statement.balance),                                  # O dinheiro na conta na data do extrato
        "transactions": [
            {
                'payee (beneficiario)': transaction.payee,                                                                                 # payee: O nome do beneficiário ou destinatário do pagamento (quem recebeu o valor).
                'type ()': transaction.type,                                                                                               # type: O tipo de transação, como crédito, débito ou transferência.
                'date': transaction.date.strftime("%d/%m/%Y"),                                                                             # Converter para string. A data em que a transação foi registrada pelo banco.
                'user_date': transaction.user_date.strftime("%d/%m/%Y") if transaction.user_date else None,                                # Converter para string. user_date: A data que o usuário associou à transação, que pode ser diferente da data oficial registrada pelo banco.
                'amount (valor_transacao)': float(transaction.amount) if isinstance(transaction.amount, Decimal) else transaction.amount,  # Converter para float. amount: O valor da transação (positivo para créditos, negativo para débitos).
                'id': transaction.id,                                                                                                      # id: Um identificador único da transação.
                'memo (OBS)': transaction.memo,                                                                                            # memo: Um campo para observações ou notas associadas à transação.
                'sic': transaction.sic,                                                                                                    # sic: Standard Industrial Classification (SIC) code, que identifica a indústria da empresa envolvida na transação.
                'mcc': transaction.mcc,                                                                                                    # mcc: Merchant Category Code (MCC), que categoriza o tipo de serviço ou negócio associado à transação.
                'checknum': transaction.checknum                                                                                           # checknum: O número do cheque, caso a transação tenha sido feita por cheque.
            }
            for transaction in ofx_data.account.statement.transactions
        ]
    }

    return json

