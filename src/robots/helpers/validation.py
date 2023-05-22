
def validate_data(data: dict) -> tuple:
        """Validate the data to search
        :param data: data to search
        :return: tuple with the data to search
        """
        search_phrase = "rpachallenge"
        sections = []
        number_of_months = 0

        if ('search_phrase' in data.keys()) and type(data['search_phrase']) == str:
            search_phrase = data['search_phrase']
        
        if ('section' in data.keys()):
            if (type(data['section']) == list):
                sections = data['section']
            elif type(data['section']) == str:
                sections.append(data['section'])
        
        if ('number_of_months' in data.keys()) and (type(data['number_of_months']) == int) and data['number_of_months'] >= 0 :
            number_of_months = data['number_of_months']
        
        return (search_phrase, sections, number_of_months)