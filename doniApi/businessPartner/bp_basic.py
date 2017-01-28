from doniApi.apiImports import Response, GenericAPIView, status


class BpBasicAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        bp_id = kwargs.get('bp_id')
        if bp_id == 'all':
            return Response({'businessPartners': [
                {
                    "bp_ID": 274,
                    "bp_Name": "A.A Enterprises",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 0,
                    "bp_country": "Pakistan",
                    "tr_transactionID": None,
                    "tr_date": None
                }, {
                    "bp_ID": 289,
                    "bp_Name": "A.A. Corporation",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 2,
                    "bp_country": "Pakistan",
                    "tr_transactionID": None,
                    "tr_date": None
                }, {
                    "bp_ID": 276,
                    "bp_Name": "A.D Impex",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 2,
                    "bp_country": "Pakistan",
                    "tr_transactionID": None,
                    "tr_date": None
                }, {
                    "bp_ID": 294,
                    "bp_Name": "A.M Enterprises",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 2,
                    "bp_country": "Pakistan",
                    "tr_transactionID": None,
                    "tr_date": None
                }, {
                    "bp_ID": 250,
                    "bp_Name": "A.S International",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": True,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 2,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 1623,
                    "tr_date": "2016-11-17T00:00:00"
                }, {
                    "bp_ID": 273,
                    "bp_Name": "ABD Corporation - Faizan Nagaria",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": True,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 2,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 1538,
                    "tr_date": "2016-11-09T00:00:00"
                }, {
                    "bp_ID": 12,
                    "bp_Name": "Abdul Basit",
                    "bp_cont_ID": 15,
                    "bp_Cont_fullName": "Abdul Basit",
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 5,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 1655,
                    "tr_date": "2016-11-21T00:00:00"
                }, {
                    "bp_ID": 171,
                    "bp_Name": "Abdul Basit - Irfan - Jalil Paracha",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 3,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 295,
                    "tr_date": "2016-03-10T00:00:00"
                }, {
                    "bp_ID": 157,
                    "bp_Name": "Abdul Basit and Irfan",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": True,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 5,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 2004,
                    "tr_date": "2016-12-16T00:00:00"
                }, {
                    "bp_ID": 77,
                    "bp_Name": "Abdul Ghani",
                    "bp_cont_ID": 17,
                    "bp_Cont_fullName": "Abdul Ghani",
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 3,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 1957,
                    "tr_date": "2016-12-07T00:00:00"
                }, {
                    "bp_ID": 215,
                    "bp_Name": "Abdul Qadir Abdul Sattar",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 4,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 2007,
                    "tr_date": "2016-12-16T00:00:00"
                }, {
                    "bp_ID": 76,
                    "bp_Name": "Abdul Qayyum",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 4,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 1496,
                    "tr_date": "2016-10-31T00:00:00"
                }, {
                    "bp_ID": 293,
                    "bp_Name": "Abdul Sattar Dullay Wala",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 3,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 1923,
                    "tr_date": "2016-12-05T00:00:00"
                }, {
                    "bp_ID": 114,
                    "bp_Name": "Abrahem Abebe",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": False,
                    "bp_isSeller": True,
                    "bp_isShipper": True,
                    "bp_credibilityIndex": 1,
                    "bp_country": "Ethiopia",
                    "tr_transactionID": None,
                    "tr_date": None
                }, {
                    "bp_ID": 224,
                    "bp_Name": "ACAA Absolute Alliance Incorporated",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": False,
                    "bp_isSeller": True,
                    "bp_isShipper": True,
                    "bp_credibilityIndex": 2,
                    "bp_country": "Canada",
                    "tr_transactionID": 1048,
                    "tr_date": "2016-07-17T00:00:00"
                }, {
                    "bp_ID": 103,
                    "bp_Name": "Adroit Overseas",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": False,
                    "bp_isSeller": True,
                    "bp_isShipper": True,
                    "bp_credibilityIndex": 3,
                    "bp_country": "Singapore",
                    "tr_transactionID": 370,
                    "tr_date": "2016-03-07T00:00:00"
                }, {
                    "bp_ID": 192,
                    "bp_Name": "Afrisian Ginning Ltd",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": False,
                    "bp_isSeller": True,
                    "bp_isShipper": True,
                    "bp_credibilityIndex": 3,
                    "bp_country": "Tanzania",
                    "tr_transactionID": 1218,
                    "tr_date": "2016-09-02T00:00:00"
                }, {
                    "bp_ID": 238,
                    "bp_Name": "AG DALL MILL",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 2,
                    "bp_country": "Pakistan",
                    "tr_transactionID": None,
                    "tr_date": None
                }, {
                    "bp_ID": 14,
                    "bp_Name": "Agar International",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": True,
                    "bp_isSeller": False,
                    "bp_isShipper": False,
                    "bp_credibilityIndex": 5,
                    "bp_country": "Pakistan",
                    "tr_transactionID": 889,
                    "tr_date": "2016-06-23T00:00:00"
                }, {
                    "bp_ID": 168,
                    "bp_Name": "Agri Commodities & Finance. FZE",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": False,
                    "bp_isSeller": True,
                    "bp_isShipper": True,
                    "bp_credibilityIndex": 3,
                    "bp_country": "Dubai",
                    "tr_transactionID": 862,
                    "tr_date": "2016-03-17T00:00:00"
                }, {
                    "bp_ID": 109,
                    "bp_Name": "Agriex Australia",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": False,
                    "bp_isSeller": True,
                    "bp_isShipper": True,
                    "bp_credibilityIndex": 3,
                    "bp_country": "Singapore",
                    "tr_transactionID": 1594,
                    "tr_date": "2016-11-15T00:00:00"
                }, {
                    "bp_ID": 288,
                    "bp_Name": "Agri-Oz Commodities Pty Ltd",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": False,
                    "bp_isSeller": True,
                    "bp_isShipper": True,
                    "bp_credibilityIndex": 3,
                    "bp_country": "Australia",
                    "tr_transactionID": 1656,
                    "tr_date": "2016-11-21T00:00:00"
                }, {
                    "bp_ID": 104,
                    "bp_Name": "Agrocorp International",
                    "bp_cont_ID": None,
                    "bp_Cont_fullName": None,
                    "bp_isBroker": False,
                    "bp_isBuyer": False,
                    "bp_isSeller": True,
                    "bp_isShipper": True,
                    "bp_credibilityIndex": 4,
                    "bp_country": "Singapore",
                    "tr_transactionID": 1160,
                    "tr_date": "2016-08-17T00:00:00"
                }
            ]})
        return Response()

    def post(self, request, *args, **kwargs):
        return Response()

    def delete(self, request, *args, **kwargs):
        return Response()

    def put(self, request, *args, **kwargs):
        return Response()
