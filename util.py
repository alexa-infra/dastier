
def truncate_char_to_space(data, num):
    if len(data) < num:
        return data

    if data.find(' ', num, num + 5) == -1:
        return data[:num] + '...'
    else:
        return data[:num] + data[data:data.find(' ', num)] + '...'

