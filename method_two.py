import os
from fillpdf import fillpdfs
import json
import random
#To extract all the filliable fields from the pdf form.
dictionary1 = fillpdfs.get_form_fields('Account Opening Form ARN- BSE STAR MF V 2.0.pdf')
# fillpdfs.get_coordinate_map('Account Opening Form ARN- BSE STAR MF V 2.0.pdf', 'template-3.pdf',page_number=2)

print(data_dict)
#Extracted data dictionary from the pdf.
# dictionary1 = {
    "Combo Box0": "86685",
    "pg1ClientName": "None",
    "pg1tfPANNo": "None",
    "Text Field16": "None",
    "pg1DOB": "None",
    "pg1tfFatherName": "None",
    "pg1tfMotherName": "None",
    "pg1GaurdianfirstName": "None",
    "Text5": "None",
    "pg1tfperAddressLine1": "None",
    "pg1tfperAddressLine2line3": "None",
    "pg1tfPerCity": "None",
    "pg1tfPerPinCode": "None",
    "pg1PerrState": "None",
    "pg1PerrCountry": "None",
    "pg1TellOff": "None",
    "Text Field2": "None",
    "pg1EmailId": "None",
    "Text Field3": "None",
    "Text Field4": "None",
    "pg1MobileNo": "None",
    "pg1tfNetWorthRs": "None",
    "pg1CityOfBirth": "None",
    "pg1OccSpecifyOther": "None",
    "pg1taxressident": "None",
    "pg1tfPANNo1": "None",
    "pg1ChkPEP": "None",
    "pg1ChkRPEP": "None",
    "Text Field5": "None",
    "Text10": "None",
    "pg1SecondHolderName": "None",
    "Pg1_tfPanNo2": "None",
    "Text Field6": "None",
    "Text Field7": "None",
    "Text Field8": "None",
    "Text3": "None",
    "Text31A": "None",
    "Text31B": "None",
    "Text7": "None",
    "Check Box9": "None",
    "pg1ThirdHolderName": "None",
    "Pg1_tfPanNo3": "None",
    "Text Field9": "None",
    "Text Field10": "None",
    "Text31C": "None",
    "Text31D": "None",
    "Text31E": "None",
    "Text31F": "None",
    "Text7A": "None",
    "Check Box8A": "None",
    "Check Box9A": "None",
    "Text10A": "None",
    "Text Field11": "None",
    "Text Field12": "None",
    "Text Field13": "None",
    "Text Field14": "None",
    "pg1tfBankName1": "None",
    "Text Field15": "None",
    "pg1tfBankAccNo1": "None",
    "pg1Accounttype1": "None",
    "pg1tfBankIFSC1": "None",
    "pg1tfBranchAddressL1": "None",
    "Text14": "None",
    "Text14a": "None",
    "Text14B": "None",
    "Text14C": "None",
    "pg1tffirstNomName1": "None",
    "Text15": "None",
    "pg1GaurdianfirstName1": "None",
    "pg1tfNomAddress": "None",
    "pg1tfNomAddress2n3": "None",
    "pg1NomCity": "None",
    "pg1NomPinCode": "None",
    "pg1NomCountry": "None",
    "pg1Date": "None",
    "Pg1_Place": "None",
    "Check Box8": "None",
    "Text Field17": "None",
    "pg2ChkAccountTypeSaving": "None",
    "pg2ChkAccountTypeCurrent": "None",
    "pg2Date": "None",
    "pg2BankAccNo": "None",
    "pg2BankName": "None",
    "pg2BankIFSC": "None",
    "pg2BankMICR": "None",
    "Text Field18": "None",
    "Text Field19": "None",
    "Text Field20": "None",
    "pg2MobileNo": "None",
    "pg2tfClientID": "None",
    "Pg2Emailid": "None",
    "pg2ChkFrequency": "None",
    "pg2Chkdebittypemax": "None",
    "pg2Chkperiod": "None",
    "Text Field0": "CITI000PIGW",
    "Text Field1": "CITI00002000000037"
  }

with open('input_data.json') as json_file:
  dictionary3 = json.load(json_file)

with open('default_format.json') as json_file:
  dictionary2 = json.load(json_file)

print("D1:", dictionary1)
print("D2:", dictionary2)
print("D3:", dictionary3)
# dictionary1 = {'a': 0, 'b': 0, 'c': 0}
# dictionary2 = {'a': ['b', 'c'], 'd': ['e', 'f']}
# dictionary3 = {'b': 1, 'e': 3, 'f': 4}
for key in dictionary1.keys():
    if key in dictionary2:
        for k in dictionary2[key]:
            print(k)
            if k in dictionary3:
                print(dictionary3[k])
                dictionary1[key]=dictionary3[k]
print("result",dictionary1)
fillpdfs.write_fillable_pdf('Account Opening Form ARN- BSE STAR MF V 2.0.pdf', 'method_two_output.pdf', dictionary1)

#FOR TEXT FIELDS
unfetched_fields = {
  "sub_broker" : [330, 51,1],
  "euin_no": [460,51,1],
  "period_from": [80,318,2],
  "period_to":[80,333,2],
}

#FOR IMAGE FIELDS
image_fields = {
  "signature1" : [50,770,1],
  "signature2" : [230,770,1],
  "signature3" : [400,770,1]
}

#FOR CHECKBOX TICKMARK
check_boxes = {
  "CREATE" : [80,85,2],
  "MODIFY" : [80,102,2],
  "CANCEL" : [80,115,2],
  "frequency_monthly" : [113,175,2],
  "frequency_quaterly" : [159,175,2],
  "frequency_halfyearly" : [199,175,2],
  "frequency_yearly" : [247,175,2],
  "frequency_as_when_presented" : [284,175,2],
}
dictionary3_keys = dictionary3.keys()

print(dictionary3_keys)
count = len(unfetched_fields)

flag = True

for key,value in unfetched_fields.items():
  print(key)
  data = dictionary3[key]
  cord_x = value[0]
  cord_y = value[1]
  page_no = value[2]
  if flag == True:
    fillpdfs.place_text(data, cord_x, cord_y,'method_two_output.pdf',f"output_{key}.pdf", page_no,font_size=10, font_name="helv", color=None)
    flag = False
  else:
    fillpdfs.place_text(data, cord_x, cord_y,f'output_{prev_key}.pdf',f"output_{key}.pdf", page_no,font_size=10, font_name="helv", color=None)
  prev_key = key
  latest_generated_pdf = f'output_{key}.pdf'
  print(latest_generated_pdf)

flag = True

for key,value in image_fields.items():
  print(key)
  data = dictionary3[key]
  cord_x = value[0]
  cord_y = value[1]
  page_no = value[2]
  if flag == True:
    fillpdfs.place_image(data, cord_x, cord_y,latest_generated_pdf,f"output_{key}.pdf", page_no,width=100, height=30 )
    flag = False
  else:
    fillpdfs.place_image(data, cord_x, cord_y, f'image_{prev_key}.pdf',f'image_{key}.pdf', page_no, width=100, height=30)
  prev_key = key

latest_generated_pdf = f'image_{prev_key}.pdf'
print(latest_generated_pdf)

flag = True
for key,value in check_boxes.items():
  print(key)
  data = dictionary3[key]
  print(data)
  cord_x = value[0]
  cord_y = value[1]
  page_no = value[2]
  if flag == True:
    if data == "Yes":
      fillpdfs.place_image("check-mark.png", cord_x, cord_y,latest_generated_pdf,f"checkbox_{key}.pdf", page_no,width=12, height=12)
      flag = False
    else:
      pass      
    
  else:
    if data == "Yes":
      fillpdfs.place_image("check-mark.png", cord_x, cord_y, f'checkbox_{prev_key}.pdf',f'checkbox_{key}.pdf', page_no, width=12, height=12)
    else:
      pass      
  prev_key = key
