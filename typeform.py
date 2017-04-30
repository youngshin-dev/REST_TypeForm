'''Developer: Sophie(Youngshin) Oh
Date: Apr 29,2017

Description:
1.Requests a form from Typeform and extract completed answers
2.Put the answers Dataframe and save it as csv.

Questions not answered are missing keys and Dataframe puts NAN for those questons
'''
import requests
import pandas

def extract_dictionary(response_list,key):
    list_of_dict = []
    for item in response_list:
        list_of_dict.append(item[key])
    return list_of_dict

def extract_into_dictionary(response_list,key):
    list = []
    for item in response_list:
        list.append(item[key])

    dict = {}
    dict[key] = list

    return dict


def main():
    #request all responses including incomplete ones
    data = requests.get('https://api.typeform.com/v1/form/PfSNFM?key=ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d&order_by=date_submit')
    if data.status_code != 200:
        raise Exception('GET /tasks/ {}'.format(data.status_code))


    #convert the resp into JSON format
    allData = data.json()
    # now the allData is a dictionary with 4 top level keys 'http_status','questions','responses', and 'stats'
    # allData['questions'] is a list of dictionaries each of which has keys 'field_id','id', and 'questions'. There are 5 questions
    # allData['responses'] is a list of dictionaries each with keys 'answers','completed','hidden','metadata', and 'token'
    # allData['responses']['answers'] is a dictionary with keys that are the question id from the questions dictionary.
    # allData['responses']['metadata'] is a dictionary with keys 'browser','date_land','date_submitted','network_id','platform','referer',and 'user_agent'
    # we will produce a table such that each row corresponds to each response

    response_list = allData['responses']

     # extract the answeres from the response_list
    answer=extract_dictionary(response_list,'answers')

    # extract the metadata from the response_list
    meta = extract_dictionary(response_list, 'metadata')

    # extract the completed from the response_list
    completed = extract_into_dictionary(response_list, 'completed')

    # extract the hidden from the response_list
    hidden = extract_into_dictionary(response_list, 'hidden')

    # extract the tokens from the response_list
    tokens= extract_into_dictionary(response_list,'token')


    A = pandas.DataFrame(answer)
    B = pandas.DataFrame(completed)
    C = pandas.DataFrame(hidden)
    D = pandas.DataFrame(meta)
    E = pandas.DataFrame(tokens)

    result = pandas.concat([A, B, C, D, E], axis=1)

    result.to_csv('responses.csv')

if __name__ == "__main__":
    main()