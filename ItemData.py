from zeep import Client
import xml.etree.ElementTree as ET
import csv
import config

with open('ExportedGridData.csv', newline='') as f:
  reader = csv.reader(f)
  examsoft_input = list(reader)


exam_results_header = ["ExamId", "PostingId", "ItemId", "QuestionText", "Rationale", "ItemType", "ItemImageName", "Author", "ChoiceText", "Comment 1", "Comment 2", "Comment 3", "Comment 4", "Comment 5", "pointValue", "discriminationIndex", "pointBiSerial", "RankUpperPercent", "RankLowerPercent", "Group", "Title", "EmbeddedComment"]

with open('ItemData.csv', 'w', newline='', encoding='utf-8') as result_file:
   writer = csv.writer(result_file)
   writer.writerow(exam_results_header)


for i in range(1,len(examsoft_input)):
   client = Client(wsdl='https://esintegration.examsoft.com/esclientdataretriever/retriever.asmx?WSDL')
   api_response = client.service.GetItemDataX(int(examsoft_input[i][2]), int(examsoft_input[i][1]), config.username, config.password)


   f = open('api_response.xml', 'wb')
   f.write(api_response)
   f.close()


   xmlparse = ET.parse('api_response.xml')
   root = xmlparse.getroot()


   item_category_list = list(root)
   exam_id = item_category_list[0].text
   posting_id = item_category_list[1].text

   item_id = ""
   question_text = ""
   rationale = ""
   item_type = ""
   item_image_name = ""
   author = ""

   choice_text = []

   comment = []
   
   point_value = ""
   discrimination_index = ""
   point_bi_serial = ""
   rank_upper_percent = ""
   rank_lower_percent = ""
   group = ""
   title = ""
   embedded_comment = ""

   exam_results_output = []


   for i in range(3, len(item_category_list)):

      for l in range (0, len(item_category_list[i])):
         
         match list(item_category_list[i])[l].tag:
            case "ItemId":
               item_id = list(item_category_list[i])[l].text
            case "QuestionText":
               question_text = list(item_category_list[i])[l].text
            case "Rationale":
               rationale = list(item_category_list[i])[l].text
            case "ItemType":
               item_type = list(item_category_list[i])[l].text
            case "ItemImageName":
               item_image_name = list(item_category_list[i])[l].text
            case "Author":
               author = list(item_category_list[i])[l].text
            case "Group":
               group = list(item_category_list[i])[l].text
            case "Title":
               title = list(item_category_list[i])[l].text
            case "EmbeddedComment":
               embedded_comment = list(item_category_list[i])[l].text

   
      for j in range(6, len(item_category_list[i])):
         if len(list(item_category_list[i])[j]) == 1:
            if list(list(item_category_list[i])[j])[0].tag == "ChoiceText":
               choice_text.append(list(list(item_category_list[i])[j])[0].text)
            else:
               comment.append(list(list(item_category_list[i])[j])[0].text)

      
         if len(list(item_category_list[i])[j]) > 1:

            for m in range (0, len(list(list(item_category_list[i])[j]))):
               match list(list(item_category_list[i])[j])[m].tag:
                  case "pointValue":
                     point_value = list(list(item_category_list[i])[j])[m].text
                  case "discriminationIndex":
                     discrimination_index =  list(list(item_category_list[i])[j])[m].text
                  case "pointBiSerial":
                     point_bi_serial =  list(list(item_category_list[i])[j])[m].text
                  case "RankUpperPercent":
                     rank_upper_percent =  list(list(item_category_list[i])[j])[m].text
                  case "RankLowerPercent":
                     rank_lower_percent =  list(list(item_category_list[i])[j])[m].text


            for k in range (0,len(choice_text)):
               while len(comment) < 5:
                  comment.append("")
               exam_results_output.append(exam_id)
               exam_results_output.append(posting_id)
               exam_results_output.append(item_id)
               exam_results_output.append(question_text)
               exam_results_output.append(rationale)
               exam_results_output.append(item_type)
               exam_results_output.append(item_image_name)
               exam_results_output.append(author)
               exam_results_output.append(choice_text[k])
               exam_results_output.append(comment[0])
               exam_results_output.append(comment[1])
               exam_results_output.append(comment[2])
               exam_results_output.append(comment[3])
               exam_results_output.append(comment[4])
               exam_results_output.append(point_value)
               exam_results_output.append(discrimination_index)
               exam_results_output.append(point_bi_serial)
               exam_results_output.append(rank_upper_percent)
               exam_results_output.append(rank_lower_percent)
               exam_results_output.append(group)
               exam_results_output.append(title)
               exam_results_output.append(embedded_comment)

               with open('ItemData.csv', 'a', newline='', encoding='utf-8') as result_file:
                  writer = csv.writer(result_file)
                  writer.writerow(exam_results_output)
               exam_results_output = []
            choice_text = []
            comment = []

