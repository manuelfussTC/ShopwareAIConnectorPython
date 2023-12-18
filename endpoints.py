import json

# def get_schemas_for_endpoints(endpoints, prompt):
#     with open('apiEndpoints.json', 'r') as file:
#         api_endpoints = json.load(file)
#
#     simplified_schemas = {}
#     for endpoint, similarity in endpoints.items():
#         if endpoint in api_endpoints['paths']:
#             schema = api_endpoints['paths'][endpoint]
#             simplified_schema = simplify_schema(schema)
#             simplified_schemas[endpoint] = simplified_schema
#
#     return build_prompt_with_schemas(simplified_schemas, prompt)
#
#
#
#
# def simplify_parameters(parameters):
#     simplified_parameters = []
#     for param in parameters:
#         name = param.get('name', 'Unnamed')
#         description = param.get('description', 'No description')
#         if len(description) > 30:
#             description = description[:27] + '...'
#         simplified_parameters.append({'name': name, 'description': description})
#     return simplified_parameters
#
# def simplify_responses(responses):
#     simplified_responses = {}
#     for status_code, response in responses.items():
#         description = response.get('description', 'No description')
#         if len(description) > 30:
#             description = description[:27] + '...'
#         simplified_responses[status_code] = {'description': description}
#     return simplified_responses
#

def build_prompt_with_schemas(schemas, prompt):
    first_prompt = prompt
    enhanced_prompt = (f"You are a well-experienced shopware developer with experience in Symfony and who knows "
                       f"the Shopware API best for over 20 years. This is my initial prompt: '{prompt}' and these are "
                       f"the possible schemas: '{json.dumps(schemas, indent=2)}' from the Shopware API that might help, "
                       "getting the data that is asked for within this prompt. "
                       "Give me only the exact, direct, clean, and unmodified answer to my question in the following: "
                       "I want you to give me the perfect endpoints for this case in a structure like "
                       "***endpoint 1*** here the data ***endpoint 1 end***, ***endpoint 2*** here the data ***endpoint 2 end***, "
                       "etc., and also the data part as this will be the head data for a cURL PHP call to the API always in JSON format. "
                       "If there will be no head with a data part as this is not always necessary, just skip this part and leave the head data part empty. "
                       "Use all information from the prompt to cover all parameters in the head also consider associations, "
                       "includes, ids, total-count-mode, page, limit, filter, post-filter, query, term, sort, aggregations, grouping. "
                       "Do not return complete curl calls, just the post or get content. Also return the CURLOPT_CUSTOMREQUEST method in a separated part like "
                       "***requestmethod 1*** here the data ***requestmethod 1 end*** Separate it in your answer like this "
                       "{{{head data 1}}} here the data {{{head data 1 end}}}, {{{head data 2}}} here the data {{{head data 2 end}}}, etc. "
                       "Please give me the perfect endpoints for this case and spare every additional information as I want to use those endpoints "
                       "and head data for a cURL PHP call to the Shopware API.")

    return enhanced_prompt
