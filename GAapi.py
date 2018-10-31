  import GAapi
  import datetime

  view_id = GAapi.VIEW_ID
  date = datetime.date.today() - datetime.timedelta(1)
  dateWeth = datetime.date.today().weekday();

  # 火から金は前日、月は先週の金から日までを選択
  if dateWeth == 0:
      dateFri = datetime.date.today() - datetime.timedelta(3)
      dateSun = datetime.date.today() - datetime.timedelta(1)
      dateStrSt = dateFri.strftime('%Y-%m-%d')
      dateStrEn = dateSun.strftime('%Y-%m-%d')
  else:
      dateStrSt = date.strftime('%Y-%m-%d')
      dateStrEn = date.strftime('%Y-%m-%d')


  dateFormat = date.strftime('%y%m%d')
  dateRanges = [{"startDate": dateStrSt, "endDate": dateStrEn}]

  # とりたい情報
  dimensions = [{"name": "ga:dateHourMinute"},
                {"name": "ga:dayOfWeekName"},
                {"name": "ga:browser"},
                {"name": "ga:deviceCategory"},
                {"name": "ga:sourceMedium"},
                {"name": "ga:campaign"},
                {"name": "ga:city"},
                {"name": "ga:adMatchedQuery"}]

  #特定のページを通った場合という条件
  dimensionFilterClauses = [{"operator": "OR",
                             "filters":[{"dimensionName": "ga:pagePath",
                             "not": "false",
                             "operator": "REGEXP",
                             "expressions": ["ページ名"],
                             "caseSensitive": "false"},
                             {"dimensionName": "ga:pagePath",
                              "not": "false",
                              "operator": "REGEXP",
                              "expressions": ["ページ名"],
                              "caseSensitive": "false"}]
                             }]
  metrics = [{"expression": "ga:pageviews", "formattingType": "INTEGER"}]
  pageSize = 10000

  body = {"reportRequests": []}
  body["reportRequests"].append({"viewId": view_id,
                                  "dateRanges": dateRanges,
                                  "dimensions": dimensions,
                                  "dimensionFilterClauses": dimensionFilterClauses,
                                  "metrics": metrics,
                                  "pageSize": pageSize
                                 })

  csvAnalytics = "analyEve"+dateFormat+".csv"
  pattern = "event"

  def main():
      analytics = GAapi.initialize_analyticsreporting()
      response = GAapi.get_report(analytics,body)
      list = GAapi.print_response(response,9)
      GAapi.print_csv(list,csvAnalytics,pattern)

  if __name__ == '__main__':
      main()