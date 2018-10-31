from apiclient.discovery import build
    from oauth2client.service_account import ServiceAccountCredentials

    import httplib2
    from oauth2client import client
    from oauth2client import file
    from oauth2client import tools

    import pandas as pd

    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
    KEY_FILE_LOCATION = r'json-fileのPATH'
    SERVICE_ACCOUNT_EMAIL = '調べたいGAのPATH'
    VIEW_ID = '調べたいGAのView-Id'

    # GAのレポート初期化
    def initialize_analyticsreporting():
        credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
        analytics = build('analyticsreporting', 'v4', credentials=credentials)
        return analytics

    # GAからデータを抽出
    def get_report(analytics,body):
        return analytics.reports().batchGet(body=body).execute()

    # とってきたデータを配列にする
    def print_response(response,span):
        length = 0
        j = -1
        for report in response.get('reports', []):
            for row in report.get('data', {}).get('rows', []):
                length = length + 1
        list = [[0 for a in range(span)] for b in range(length)]

        for report in response.get('reports', []):
            columnHeader = report.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

            for row in report.get('data', {}).get('rows', []):
                j = j + 1
                k = 0
                dimensions = row.get('dimensions', [])
                dateRangeValues = row.get('metrics', [])

                for header, dimension in zip(dimensionHeaders, dimensions):
                    print (header + ':' + dimension)
                    if k == 0:
                        list[j][k] = dimension[0:8]
                        k = k + 1
                        list[j][k] = dimension[8:10] + ':' + dimension[10:12]
                    else:
                        k = k + 1
                        list[j][k] = dimension

                for i, values in enumerate(dateRangeValues):
                    for metricHeader, value in zip(metricHeaders, values.get('values')):
                        print (metricHeader.get('name') + ': ' + value)
        return list

    # CSVファイルに変換
    def print_csv(list,csv,pattern):
            df = pd.DataFrame(list,columns = ['登録日','時間','曜日','ブラウザ','デバイス','CV経路','キャンペーン','地域','検索クエリ'])
        df.to_csv(csv,encoding = 'SHIFT-JIS')