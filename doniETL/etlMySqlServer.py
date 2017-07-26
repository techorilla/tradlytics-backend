from os import getenv
import pymssql
from django.contrib.auth.models import User
from pymssql import InterfaceError
import dateutil.parser

server = "donigroup.cczhghwibti9.us-west-2.rds.amazonaws.com:1433"
user = "immadimtiaz"
password = "Giki1990????"

conn = pymssql.connect(server, user, password, "DoniEnterprises")


from doniServer.models.dropDowns import *
from doniServer.models import Transaction, TrFiles, TrShipment, ProductItem, BpBasic, TrCommission, TrComplete, TrSellerInvoice

created_by = User.objects.get(username='immadimtiaz')


def check_files_not_in_system():
    cursor = conn.cursor()
    query = """
            Select
                RTRIM(LTRIM(t.tr_fileID))
            from Transactions as t
        """
    cursor.execute(query)
    file_does_not_exist = []
    for row in cursor.fetchall():
        try:
            trade = Transaction.objects.get(file_id=row[0])
        except Transaction.DoesNotExist:
            file_does_not_exist.append(row[0])
            print 'This transaction is not in the system %s' % row[0]
            transfer_trade_commission_data(file_id=row[0])

    return file_does_not_exist




def mark_completed_transactions():
    cursor = conn.cursor()
    query = """
        Select
            t.tr_fileID,
            ts.tr_transactionStatus,
            ts.tr_editedOn,
            ts.tr_createdOn
        from TransactionsStatus as ts
        INNER JOIN
        Transactions as t
        ON t.tr_transactionID = ts.tr_transactionID
        where tr_transactionStatus=\'Completed\'
    """
    cursor.execute(query)

    for row in cursor:
        file_id = row[0]
        completion_date = row[2] if row[2] else row[3]
        try:
            trade = Transaction.objects.get(file_id=file_id)
            complete_status = trade.completion_status if hasattr(trade, 'completion_status') else TrComplete()

            complete_status.is_complete = True
            complete_status.completion_date = completion_date
            complete_status.transaction = trade
            if not hasattr(trade, 'completion_status'):
                complete_status.created_by = created_by
            else:
                complete_status.created_by = created_by
                complete_status.updated_by = created_by
            complete_status.save()

        except Transaction.DoesNotExist:
            print 'This transaction is not in the system  %s'%file_id



def get_files_for_all_trades(trades=None):
    cursor = conn.cursor()
    all_trade = all_trade if trades else Transaction.objects.all()
    for trade in all_trade:
        get_transaction_files_from_old_erp(trade.file_id, cursor)
        print  trade.file_id
    conn.close()


def get_transaction_files_from_old_erp(file_id, cursor):

    query = 'SELECT tf.tf_fileId,tf_file,tf_fileName, tf_fileType FROM TransactionFiles as tf INNER JOIN Transactions as t ON t.tr_transactionID = tf.tf_transactionID AND t.tr_fileID =\'%s\' '
    query = query.replace('%s',file_id)
    transaction = Transaction.objects.get(file_id=file_id)
    try:
        cursor.execute(query)
    except InterfaceError:
        cursor = conn.cursor()
        cursor.execute(query)

    for row in cursor:
        if not transaction.files.filter(file_name=row[2]).exists():
            file = TrFiles()
            file.transaction = transaction
            file.file = row[1]
            file.file_name = row[2]
            file.extension = row[3]
            file.created_by = created_by
            file.save()
    return query


def transfer_trade_commission_data(file_id=None):
    cursor = conn.cursor()
    query = """
                SELECT
                    t.tr_fileID,
                    t.tr_contractId,
                    t.tr_bpBuyerId,
                    t.tr_bpSellerId,
                    t.tr_productId,
                    t.tr_price,
                    t.tr_quantity,
                    t.tr_packing,
                    t.tr_shipment_start,
                    t.tr_shipment_end,
                    t.tr_other_info,
                    tc.tr_sellerBrokerID,
                    tc.tr_buyerBrokerID,
                    tc.tr_ownCommissionType,
                    tc.tr_own_Commission,
                    tc.tr_buyerBroker_comm_type,
                    tc.tr_buyerBroker_comm,
                    tc.tr_difference,
                    tc.tr_discount,
                    t.tr_date,
                    tcc.tr_ContractualBuyer
                FROM
                Transactions as t
                INNER JOIN
                TransactionsCommission tc
                ON t.tr_transactionID = tc.tr_transactionID
                INNER JOIN
                TransactionsContract tcc
                ON t.tr_transactionID = tcc.tr_transactionID

    """

    if file_id:
        query = query + ' WHERE t.tr_fileID = \'%s\''
        query = query%file_id
    cursor.execute(query.strip())
    all = cursor.fetchall()
    save_trade_commission_data(all)


def save_trade_commission_data(cursor):
    print cursor
    for row in cursor:
        file_id = row[0]
        contract_id = row[1]
        buyer = BpBasic.get_business_with_database_id(database_id=row[2])
        seller = BpBasic.get_business_with_database_id(database_id=row[3])
        product = ProductItem.get_product_with_database_id(database_id=row[4])
        price = float(row[5])
        quantity = float(row[6])
        packing = Packaging.objects.get(name=row[7])

        ship_start = row[8]
        ship_end = row[9]
        other_info = row[10]

        seller_broker = None if not row[11] else BpBasic.get_business_with_database_id(database_id=row[11])
        buyer_broker = None if not row[12] else BpBasic.get_business_with_database_id(database_id=row[12])
        commission_type = CommissionType.objects.get(name=row[13])

        commission = float(row[14])
        buyer_broker_commission_type = CommissionType.objects.get(name=row[15])
        buyer_broker_commission = 0.00 if not row[16] else float(row[16])
        difference = float(row[17])
        discount = float(row[18])
        date = row[19]

        if row[20]:
            contractual_buyer = BpBasic.get_business_with_database_id(database_id=row[20])
        else:
            contractual_buyer = buyer

        if not Transaction.objects.filter(file_id=file_id).exists():
            new_trade = Transaction()
            new_trade.date = date
            new_trade.buyer = buyer
            new_trade.seller = seller
            new_trade.contractual_buyer = contractual_buyer
            new_trade.product_item = product
            new_trade.quantity = quantity
            new_trade.price = price
            new_trade.packaging = packing
            new_trade.shipment_start = ship_start
            new_trade.shipment_end = ship_end
            new_trade.file_id = file_id
            new_trade.contract_id = contract_id
            new_trade.other_info = other_info
            new_trade.created_by = created_by
            new_trade.save()
            new_commission = TrCommission()
            new_commission.seller_broker = seller_broker
            new_commission.transaction = new_trade
            new_commission.buyer_broker = buyer_broker
            new_commission.buyer_broker_comm_type = buyer_broker_commission_type
            new_commission.buyer_broker_comm = buyer_broker_commission
            new_commission.commission_type = commission_type
            new_commission.commission = commission
            new_commission.difference = difference
            new_commission.discount = discount
            new_commission.save()
            print 'File Created'
        else:
            print 'File Already Exist in the System'



def get_transaction_shipment_data():
    cursor = conn.cursor()
    query = """
                Select
                    t.tr_fileID,
                    tr_expectedShipment,
                    tr_inTransit,
                    tr_dateShipped,
                    tr_expectedArrival,
                    tr_ship_notShipped_reason,
                    ts.tr_ship_BlNo,
                    ts.tr_ship_quantity
                from TransactionsShipment  as ts
                inner join
                Transactions as t
                ON
                t.tr_transactionID = ts.tr_transactionID
            """

    cursor.execute(query.strip())
    for row in cursor:
        try:
            transaction = Transaction.objects.get(file_id=row[0])
            commission = transaction.commission
            try:
                shipment = transaction.shipment
            except TrShipment.DoesNotExist:
                print row[0], 'Not Exist'
                shipment = TrShipment()
                shipment.created_by = created_by

            if row[1]: shipment.expected_shipment = row[1]
            if row[2]: shipment.in_transit = row[2]
            if row[3]: shipment.date_shipped_on = row[3]
            if row[4]: shipment.expected_arrival = row[4]
            if row[5]: shipment.not_shipped_reason = row[5]
            if row[6]: shipment.bl_no = row[6]
            if row[7]:
                if not commission.quantity_shipped:
                    commission.quantity_shipped = float(row[7])

            transaction.save()
            commission.save()
            shipment.save()
        except Transaction.DoesNotExist:
            pass


def fix_all_transaction_date_invoice_data():
    cursor = conn.cursor()
    query = """
                    Select
                        t.tr_fileID,
                        t.tr_date,
                        ts.tr_ship_invoiceNo,
                        ts.tr_ship_invoiceAmt
                    from TransactionsShipment  as ts
                    inner join
                    Transactions as t
                    ON
                    t.tr_transactionID = ts.tr_transactionID
                """
    cursor.execute(query)
    all_row = cursor.fetchall()

    for row in all_row:
        file_id = row[0]
        date = row[1]ex
        try:
            transaction = Transaction.objects.get(file_id=file_id)
            transaction.date = date
            if row[3]:
                transaction.seller_invoice = TrSellerInvoice()
                transaction.seller_invoice.tr_seller_invoice_no = row[2]
                transaction.seller_invoice.tr_seller_invoice_amount_usd = row[3]
                transaction.seller_invoice.save()
            transaction.save()
        except transaction.DoesNotExist:
            pass


def update_arrived_at_port_transaction():
    cursor = conn.cursor()
    query = """
                SELECT
                      t.tr_fileID,
                      ts.tr_transactionStatus,
                      ts.tr_editedOn,
                      sh.tr_dateArrived
                FROM TransactionsStatus as ts
                INNER JOIN dbo.Transactions as t
                ON t.tr_transactionID = ts.tr_transactionID
                INNER JOIN TransactionsShipment as sh
                ON sh.tr_transactionID = ts.tr_transactionID
                where tr_transactionStatus=\'Arrived\'
            """
    cursor.execute(query)
    all = cursor.fetchall()
    for row in all:
        try:
            transaction = Transaction.objects.get(file_id=row[0])
            shipment= TrShipment() if not hasattr(transaction,'shipment') else transaction.shipment
            shipment.created_by=created_by
            shipment.transaction = transaction
            shipment.not_shipped = False
            shipment.app_received = True
            shipment.shipped = True
            shipment.arrived_at_port = True
            shipment.save()
            print 'Saved'
        except Transaction.DoesNotExist:
            print '%s file does not exist'%row[0]
    return all


