class CustomPagination:

    def get_paginated_data(self, data, page_number, page_size):
       
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        paginated_queryset = data[start_index:end_index]
        if len(paginated_queryset) != len(data):
            return paginated_queryset, True
        else:
            return paginated_queryset, False