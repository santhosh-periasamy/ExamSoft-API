from zeep import Client
import xml.etree.ElementTree as ET
import csv
import config


with open('ExportedGridData.csv', newline='', encoding='utf-8') as f:
  reader = csv.reader(f)
  examsoft_input = list(reader)


exam_results_header = ["ExamId", "PostingId", "UserId", "ItemId", "Score", "Answer", "Weight"]

with open('ExamResults.csv', 'w', newline='', encoding='utf-8') as result_file:
   writer = csv.writer(result_file)
   writer.writerow(exam_results_header)


for i in range(1,len(examsoft_input)):
   client = Client(wsdl='https://esintegration.examsoft.com/esclientdataretriever/retriever.asmx?WSDL')
   api_response = client.service.GetExamResultsX(int(examsoft_input[i][2]), int(examsoft_input[i][1]), config.username, config.password)


   f = open('api_response.xml', 'wb')
   f.write(api_response)
   f.close()


   xmlparse = ET.parse('api_response.xml')
   root = xmlparse.getroot()

   examresults_list = list(root)


   for l in range (0, len(examresults_list)):
      match examresults_list[l].tag:
         case "ExamId":
            exam_id = examresults_list[l].text
         case "PostingId":
            posting_id = examresults_list[l].text
         case "UserSets":
            usersets_list = list(examresults_list[l])

   user_id = ""


   exam_results_output = []

   exam_result_details_pos = -1

   for j in range(0,len(usersets_list)):
      
      for m in range (0, len(list(usersets_list[j]))):
         if list(usersets_list[j])[m].tag == "UserId":
            user_id = list(usersets_list[j])[m].text
         if list(usersets_list[j])[m].tag == "ExamResultsDetails":
            exam_result_details_pos = m

      for k in range(0, len(list(list(usersets_list[j])[exam_result_details_pos]))):
         
         for p in range(0, len(list(list(list(usersets_list[j])[exam_result_details_pos])[k]))):
            match list(list(list(usersets_list[j])[1])[k])[p].tag:
               case "ItemId":
                  item_id = list(list(list(usersets_list[j])[exam_result_details_pos])[k])[p].text
               case "Score":
                  score = list(list(list(usersets_list[j])[exam_result_details_pos])[k])[p].text
               case "Answer":
                  answer = list(list(list(usersets_list[j])[exam_result_details_pos])[k])[p].text
               case "Weight":
                  weight = list(list(list(usersets_list[j])[1])[k])[p].text

         exam_results_output.append(exam_id)
         exam_results_output.append(posting_id)
         exam_results_output.append(user_id)
         exam_results_output.append(item_id)
         exam_results_output.append(score)
         exam_results_output.append(answer)
         exam_results_output.append(weight)
         with open('ExamResults.csv', 'a', newline='', encoding='utf-8') as result_file:
            writer = csv.writer(result_file)
            writer.writerow(exam_results_output)
         exam_results_output = []




