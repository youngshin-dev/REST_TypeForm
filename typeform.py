'''Developer: Sophie(Youngshin) Oh
Date: Apr 29,2017

Description:
1.Requests a form from Typeform and extract completed answers
2.Put the answers Dataframe and save it as csv.

Questions not answered are missing keys and Dataframe puts NAN for those questons
'''
import requests
import pandas


def main():
    #request all responses including incomplete ones
    data = requests.get('https://api.typeform.com/v1/form/PfSNFM?key=ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d&order_by=date_submit')
    if data.status_code != 200:
        raise Exception('GET /tasks/ {}'.format(data.status_code))



    #convert the resp into JSON format
    allData = data.json()


    question_list=allData['questions']

    # create a dict that will have question 'id' as the key and actual question as the value
    question_dict={}
    for question in question_list:
        question_dict[question['id']]=question['question']

    response_list = allData['responses']

    A=pandas.DataFrame(response_list)

    A.to_csv('responses.csv')


if __name__ == "__main__":
    main()