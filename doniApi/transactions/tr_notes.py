from doniApi.apiImports import Response, GenericAPIView, status
from doniServer.models import TrNote, Transaction
from rest_framework.permissions import IsAuthenticated, AllowAny

class TransactionNoteAPI(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        transaction_id = kwargs.get('tr_id')
        if transaction_id:
            transaction = Transaction.objects.get(tr_id=int(transaction_id))
            all_notes = transaction.notes.all()
            all_notes = [note.get_obj(base_url, request.user) for note in all_notes]
            return Response({
                'notesList': all_notes
            }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        try:
            data = request.data
            user = request.user
            transaction_id = data.get('tradeId')
            transaction = Transaction.objects.get(tr_id=int(transaction_id))
            note = TrNote()
            note.note = data.get('note')
            note.transaction = transaction
            note.created_by = user
            note.save()
            return Response({
                'note': note.get_obj(base_url, user),
                'success': True,
                'message': 'Trade Note for File Id %s added successfully.' % transaction.file_id
            }, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            transaction_id = kwargs.get('tr_id')
            note_id = kwargs.get('note_id')
            note = TrNote.objects.filter(note_id=int(note_id)).filter(transaction__tr_id=int(transaction_id))
            file_id = note[0].transaction.file_id
            note.delete()
            return Response({
                'success':True,
                'message': 'Trade Note for File Id %s deleted successfully.' % file_id
            })
        except Exception, e:
            return Response({
                'success': False,
                'message': str(e)
            })

    def put(self, request, *args, **kwargs):
        base_url = request.META.get('HTTP_HOST')
        try:
            data = request.data
            transaction_id = data.get('tradeId')
            note_id = data.get('noteId')
            note = TrNote.objects.filter(note_id=int(note_id)).filter(transaction__tr_id=int(transaction_id)).first()
            file_id = note.transaction.file_id
            note_text = data.get('note')
            note.note = note_text
            note.save()
            return Response({
                'note': note.get_obj(base_url, request.user),
                'success': True,
                'message': 'Your trade Note for File Id %s updated successfully.' % file_id
            })

        except Exception,e:
            return Response({
                'success': False,
                'message': str(e)
            })
        return Response()