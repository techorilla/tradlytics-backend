from doniApi.apiImports import Response, GenericAPIView,status


class AppTabFilters(object):
    PRODUCTS = 'Products'
    BP = 'Business_Partner'
    BUYER = 'Buyer'
    SELLER = 'Seller'
    SHIPPER = 'Shipper'
    BROKER = 'Broker'
    TRANSACTION_STATUS = 'Transaction_Status'
    COUNTRY = 'Country'
    ORIGIN = 'Origin'
    CONTRACT_TYPES = 'Contract_Types'
    USERS = 'Users'
    COMMISSION_TYPES = 'Commission_Types'
    BP_TYPES = 'Business_Partner_Types'



class TabFiltersAPI(GenericAPIView):

    def get(self, request, *args, **kwargs):
        type = request.GET.get('type')
        sub_type = request.GET.get('subtype')
        print type

        if type == AppTabFilters.PRODUCTS:
            return Response({'filterList': [{
                "id": 1,
                "name": "Lentils Crimson 2016/17 crop",
                "quality": "Machine-Cleaned-or-Farmer-Dressed",
                "origin": "Canada",
                "t_id": 1649,
                "t_date": "2016-10-25T00:00:00"
            }, {
                "id": 2,
                "name": "Kabuli 9mm",
                "quality": "62/64",
                "origin": "India",
                "t_id": 866,
                "t_date": "2016-06-20T00:00:00"
            }, {
                "id": 3,
                "name": "Black Mapte SQ",
                "quality": "Super-Quality",
                "origin": "Burma",
                "t_id": 2027,
                "t_date": "2016-12-17T00:00:00"
            }]})
        elif type == AppTabFilters.TRANSACTION_STATUS:
            return Response({'filterList': []})
        elif type == AppTabFilters.BP_TYPES:
            return Response({'filterList': [
                {
                    "id": 1,
                    "name": "Buyer",
                    "isChecked": False,
                    "model": "bp_isBuyer"
                },
                {
                    "id": 2,
                    "name": "Seller",
                    "isChecked": False,
                    "model": "bp_isSeller"

                },
                {
                    "id": 3,
                    "name": "Broker",
                    "isChecked": False,
                    "model": "bp_isBroker"
                },
                {
                    "id": 4,
                    "name": "Shipper",
                    "isChecked": False,
                    "model": "bp_isShipper"
                }
            ]})
        elif type == AppTabFilters:
            return Response({'filterList': []})
        elif type == AppTabFilters.COUNTRY:
            return Response({'filterList': []})
        elif type == AppTabFilters.ORIGIN:
            return Response({'filterList': []})
        elif type == AppTabFilters.USERS:
            return Response({'filterList': []})
        elif type == AppTabFilters.BP:
            return Response({'filterList': []})
        elif type == AppTabFilters.TRANSACTION_STATUS:
            return Response({'filterList': [
                {"value": "1", "text": "Not Shipped"},
                {"value": "2", "text": "Shipped"},
                {"value": "3", "text": "Arrived"},
                {"value": "4", "text": "Completed"},
                {"value": "5", "text": "Washout at Par"},
                {"value": "6", "text": "Washout at X"}
            ]})
        elif type == AppTabFilters.CONTRACT_TYPES:
            return Response({'filterList': [
                {"value": "1", "text": "Fixed"},
                {"value": "2", "text": "Percentage"}
            ]})

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)





    def post(self, request, *args, **kwargs):
        return Response()

    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        return Response()