from os import getenv
import pymssql
from django.contrib.auth.models import User

server = "donigroup.cczhghwibti9.us-west-2.rds.amazonaws.com:1433"
user = "immadimtiaz"
password = "Giki1990????"

conn = pymssql.connect(server, user, password, "DoniEnterprises")

# cursor = conn.cursor()

from doniServer.models import Transaction, TrFiles

created_by = User.objects.get(username='immadimtiaz')


def get_files_for_all_trades():

    all_trade = Transaction.objects.all()

    for trade in all_trade:
        cursor = conn.cursor()
        get_transaction_files_from_old_erp(trade.file_id, cursor)
        print  trade.file_id
        conn.close()


def get_transaction_files_from_old_erp(file_id, cursor):
    query = 'SELECT tf.tf_fileId,tf_file,tf_fileName, tf_fileType FROM TransactionFiles as tf INNER JOIN Transactions as t ON t.tr_transactionID = tf.tf_transactionID AND t.tr_fileID =\'%s\' '
    query = query.replace('%s',file_id)
    transaction = Transaction.objects.get(file_id=file_id)
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
