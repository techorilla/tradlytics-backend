from os import getenv
import pymssql
from django.contrib.auth.models import User
from pymssql import InterfaceError
import dateutil.parser

server = "donigroup.cczhghwibti9.us-west-2.rds.amazonaws.com:1433"
user = "immadimtiaz"
password = "Giki1990????"

conn = pymssql.connect(server, user, password, "DoniEnterprises")



from doniServer.models import Transaction, TrFiles, TrShipment

created_by = User.objects.get(username='immadimtiaz')


def get_files_for_all_trades():
    cursor = conn.cursor()
    all_trade = Transaction.objects.all()
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
            if row[7]: commission.quantity_shipped = float(row[7])

            transaction.save()
            commission.save()
            shipment.save()
        except Transaction.DoesNotExist:
            pass




