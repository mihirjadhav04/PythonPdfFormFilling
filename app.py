from flask import Flask, request
import os
import json
from fillpdf import fillpdfs
import shutil
import boto3
from bolt.storage import BoltStore, BoltStoreConfig

storage_config = {
    "PROVIDER": "AWSS3STORAGE",
    "AWSS3STORAGE": {
        "BUCKET_NAME": "kwikid-doc-service",
        "AWS_ACCESS_KEY_ID": "AKIAVJPOSZMP4KWKA5SA",
        "AWS_SECRET_ACCESS_KEY": "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",
        "REGION_NAME": "ap-south-1",
    },
}
storage_config = BoltStoreConfig.parse_obj(storage_config)

bolt_store = BoltStore(storage_config)

app = Flask(__name__)

@app.route('/fill-pdf-form-data', methods=['POST'])
def generate_pdf():
    input_data = request.get_json()
    pdf_name = "Account Opening Form ARN- BSE STAR MF V 2.0.pdf"
    client_name = input_data.get('client_name')
    name = fill_pdf_form_with_data(pdf_name,input_data)
    file_name = f'{client_name}_{name}'
    s3_url = bolt_store.upload_file(file_path = name, file_name=file_name)
    return { 
        "final_pdf_name" : file_name, 
        "s3_url": s3_url 
        }

def extract_form_fields(pdf_file_name):
    # To extract all the fillable fields from the pdf form.
    form_fields = fillpdfs.get_form_fields(pdf_file_name)
    for key,value in form_fields.items():
        print(value)
        form_fields[key] = ""
        print(value)
    return form_fields

def open_pdf_files():
    with open('default_format.json') as json_file:
        json_data = json.load(json_file)
    return json_data

def fill_pdf_with_extracted_fields(file_name,dictionary1, dictionary2, dictionary3):
    for key in dictionary1.keys():
        if key in dictionary2:
            for k in dictionary2[key]:
                print(k)
                if k in dictionary3:
                    print(dictionary3[k])
                    dictionary1[key]=dictionary3[k]
    print("result",dictionary1)
    fillpdfs.write_fillable_pdf(file_name, 'document/file_version1.pdf', dictionary1)
    file_version1 = "document/file_version1.pdf"
    return file_version1


def fill_remaining_text_fields_in_pdf(file_version1, dictionary3):
    #FOR TEXT FIELDS
    unfetched_fields = {
    "sub_broker" : [330, 51,1],
    "euin_no": [460,51,1],
    "period_from": [80,318,2],
    "period_to":[80,333,2],
    }
    flag = True
    latest_generated_pdf = None

    for key, value in unfetched_fields.items():
        data = dictionary3[key]
        cord_x = value[0]
        cord_y = value[1]
        page_no = value[2]

        if flag:
            fillpdfs.place_text(
                data, cord_x, cord_y,
                file_version1, f"document/output_{key}.pdf",
                page_no, font_size=10, font_name="helv", color=None
            )
            flag = False
        else:
            fillpdfs.place_text(
                data, cord_x, cord_y,
                f'document/output_{prev_key}.pdf', f"document/output_{key}.pdf",
                page_no, font_size=10, font_name="helv", color=None
            )

        prev_key = key
        latest_generated_pdf = f'document/output_{key}.pdf'

    return latest_generated_pdf

def fill_pdf_with_images( file_version2,dictionary3):
    #FOR IMAGE FIELDS
    image_fields = {
      "signature1" : [50,770,1],
      "signature2" : [230,770,1],
      "signature3" : [400,770,1]
    }
    flag = True
    for key,value in image_fields.items():
      print(key)
      data = dictionary3[key]
      cord_x = value[0]
      cord_y = value[1]
      page_no = value[2]
      if flag == True:
        fillpdfs.place_image(data, cord_x, cord_y, file_version2,f"document/image_{key}.pdf", page_no,width=100, height=30 )
        flag = False
      else:
        fillpdfs.place_image(data, cord_x, cord_y, f'document/image_{prev_key}.pdf',f'document/image_{key}.pdf', page_no, width=100, height=30)
      prev_key = key

    latest_generated_pdf = f'document/image_{prev_key}.pdf'
    print(latest_generated_pdf)
    
    return latest_generated_pdf


def fill_pdf_with_checkbox_data(file_version3,dictionary3):
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
      "debit_fixed_amount":[113,195,2],
      "debit_maximum_amount": [197,195,2],
      "SB": [420,88,2],
      "CA": [437,88,2],
      "CC": [457,88,2],
      "SB-NRE": [508,88,2],
      "SB-NRO": [442,100,2],
      "Other":[470,100,2],
      "political_exposed_person_or_related1_yes": [370,255,1],
      "political_exposed_person_or_related1_no": [442,255,1],
      "political_exposed_person_or_related2_yes": [370,363,1],
      "political_exposed_person_or_related2_no": [442,363,1],
      "political_exposed_person_or_related3_yes": [370,456,1],
      "political_exposed_person_or_related3_no": [442,456,1]
    }

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
          fillpdfs.place_image("check-mark.png", cord_x, cord_y,file_version3,f"document/checkbox_{key}.pdf", page_no,width=12, height=12)
          flag = False
        else:
            fillpdfs.place_text("", cord_x, cord_y,file_version3,f"document/checkbox_{key}.pdf", page_no)
            flag = False

      else:
        if data == "Yes":
            fillpdfs.place_image("check-mark.png", cord_x, cord_y, f'document/checkbox_{prev_key}.pdf',f'document/checkbox_{key}.pdf', page_no, width=12, height=12)
        else:
            fillpdfs.place_text("", cord_x, cord_y,f'document/checkbox_{prev_key}.pdf',f"document/checkbox_{key}.pdf", page_no)
                     
      prev_key = key
      file_version4 = f'document/checkbox_{prev_key}.pdf'
      
    return file_version4


def fill_pdf_form_with_data(pdf_file_name,input_data):
    dictionary1 = extract_form_fields(pdf_file_name)
    
    print(dictionary1)
    dictionary2 = open_pdf_files()
    dictionary3 = input_data

    newpath = r'./document' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    file_version1 = fill_pdf_with_extracted_fields(pdf_file_name,dictionary1,dictionary2,dictionary3)
    print(file_version1)
  
    file_version2 = fill_remaining_text_fields_in_pdf(file_version1,dictionary3)
    print(file_version2)

    file_version3 = fill_pdf_with_images(file_version2, dictionary3)
    print(file_version3)

    file_version4 = fill_pdf_with_checkbox_data(file_version3,dictionary3)
    print(file_version4)
    final_result = copy_final_file_version(file_version4)
    print(final_result)
    try:
        shutil.rmtree("document")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return final_result


def copy_final_file_version(source_file_path): 
    
    # Source path
    source = source_file_path
    
    # Destination path
    destination = "output_file.pdf"
    
    # Copy the content of
    # source to destination
    try:
        shutil.copy(source, destination)
        print("File copied successfully.")
        return destination
    # If source and destination are same
    except shutil.SameFileError:
        print("Source and destination represents the same file.")

if __name__ == "__main__":
    app.run(debug=True)