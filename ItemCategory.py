from zeep import Client
import xml.etree.ElementTree as ET
import csv
import config

with open('ExportedGridData.csv', newline='', encoding='utf-8') as f:
  reader = csv.reader(f)
  examsoft_input = list(reader)


exam_results_header = ["ExamId", "ItemId", "ParentUid", "SubscaleUid", "Description"]

with open('ItemCategory.csv', 'w', newline='', encoding='utf-8') as result_file:
   writer = csv.writer(result_file)
   writer.writerow(exam_results_header)


for k in range(1,len(examsoft_input)):
   client = Client(wsdl='https://esintegration.examsoft.com/esclientdataretriever/retriever.asmx?WSDL')
   api_response = client.service.GetItemCategoryX(int(examsoft_input[k][2]), int(examsoft_input[k][1]), config.username, config.password)


   f = open('api_response.xml', 'wb')
   f.write(api_response)
   f.close()


   xmlparse = ET.parse('api_response.xml')
   root = xmlparse.getroot()


   item_category_list = list(root)

   for l in range (0, len(item_category_list)):
      if item_category_list[l].tag == "ExamId":
         exam_id = item_category_list[l].text

   item_id = ""
   parent_uid = ""
   subscale_uid = ""
   description = ""


   exam_results_output = []

   categories_pos = -1

   for i in range(2,len(item_category_list)):

      for m in range(0, len(list(item_category_list[i]))):
         if list(item_category_list[i])[m].tag == "ItemId":
            item_id = list(item_category_list[i])[0].text

      if item_id != "0":

         for n in range(0, len(list(list(item_category_list[i])))):
            if list(list(item_category_list[i]))[n].tag == "Categories":
               categories_pos = n

         for j in range(len(list(list(item_category_list[i])[categories_pos]))):

            for p in range (0, len(list(list(list(list(item_category_list[i])[categories_pos]))[j]))):
               match list(list(list(list(item_category_list[i])[categories_pos]))[j])[p].tag:
                  case "ParentUid":
                     parent_uid = list(list(list(list(item_category_list[i])[categories_pos]))[j])[p].text
                  case "SubscaleUid":
                     subscale_uid = list(list(list(list(item_category_list[i])[categories_pos]))[j])[p].text
                  case "Description":
                     description = list(list(list(list(item_category_list[i])[categories_pos]))[j])[p].text

            exam_results_output.append(exam_id)
            exam_results_output.append(item_id)
            exam_results_output.append(parent_uid)
            exam_results_output.append(subscale_uid)
            exam_results_output.append(description)
            with open('ItemCategory.csv', 'a', newline='', encoding='utf-8') as result_file:
               writer = csv.writer(result_file)
               writer.writerow(exam_results_output)
            exam_results_output = []
      
      else:
         exam_results_output.append(exam_id)
         exam_results_output.append(item_id)
         exam_results_output.append("")
         exam_results_output.append("")
         exam_results_output.append("")

         with open('ItemCategory.csv', 'a', newline='', encoding='utf-8') as result_file:
               writer = csv.writer(result_file)
               writer.writerow(exam_results_output)
         exam_results_output = []
