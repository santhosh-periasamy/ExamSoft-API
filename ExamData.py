from zeep import Client
import xml.etree.ElementTree as ET
import csv
import config


with open('ExportedGridData.csv', newline='', encoding='utf-8') as f:
  reader = csv.reader(f)
  examsoft_input = list(reader)


exam_data_header = ["ExamId", "ExamType", "ExamName", "Course", "PostingId", "DLClose"]
row_of_data = []


with open('ExamData.csv', 'w', newline='', encoding='utf-8') as result_file:
  writer = csv.writer(result_file)
  writer.writerow(exam_data_header)


for i in range(1,len(examsoft_input)):
  client = Client(wsdl='https://esintegration.examsoft.com/esclientdataretriever/retriever.asmx?WSDL')
  api_response = client.service.GetExamDataX(int(examsoft_input[i][2]), int(examsoft_input[i][1]), config.username, config.password)

  f = open('api_response.xml', 'wb')
  f.write(api_response)
  f.close()


  xmlparse = ET.parse('api_response.xml')
  root = xmlparse.getroot()

  with open('ExamData.csv', 'a', newline='', encoding='utf-8') as result_file:
    writer = csv.writer(result_file)
    row_of_data = []
    for elem in root:
      row_of_data.append(elem.text)
    
    writer.writerow(row_of_data)





