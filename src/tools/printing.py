import json


def generate_printout(request_obj, ignore=[], limit_body=None):
    '''
    Generates a pretty print version of the passed request object's Request and
    Response.
    ``ignore`` is an array of items to not include in the printout: 'status',
               'headers', 'body'
    ``limit_body`` an integer to limit the length of the body string or None
    '''

    # Set the amount of padding for the Left Column
    left_column_width = 12

    def _build_headers(headers):
        heads = [u"{txt:>{padding}}:".format(
            txt="Headers", padding=left_column_width)]
        header_width = max(
            left_column_width, *[len(k) for k in headers.keys()])
        heads.extend([u"{key:>{padding}}:  {value}".format(
            key=k, padding=header_width,
            value=v) for k, v in headers.items()])
        return heads

    def _build_data(data, limit_body=None):
        rtn_data = [u"{txt:>{padding}}:".format(
            txt="JSON", padding=left_column_width)]
        try:
            my_data = json.dumps(json.loads(data), indent=4)
        except Exception:
            rtn_data = [u"{txt:>{padding}}:".format(
                txt="DATA", padding=left_column_width)]
            my_data = u"    {data}".format(data=data)
        my_data = ellipsis_print(my_data, limit_body)

        # split lines to add padding
        rtn_data.append(indent_text_block(my_data, left_column_width))
        return rtn_data

    def _generate_response_printout(my_request, ignore=[], limit_body=None):
        if request_obj is None:
            return "No Response"
        request = my_request
        output = ["{txt:>{padding}}:".format(
            txt="RESPONSE", padding=left_column_width)]
        if "status" not in ignore:

            # this is here because sometimes the requests library
            #    returns a blank string for the reason, and it's
            #    driving me crazy!!!!
            reason_str = request.reason
            if reason_str == "":
                import http.client
                reason_str = http.client.responses[int(request.status_code)]
            output.append("{txt:>{padding}}:  {code:>3} - {reason}".format(
                txt="Status", padding=left_column_width,
                code=request.status_code, reason=reason_str))
        if "headers" not in ignore:
            output += _build_headers(request.headers)
        if "body" not in ignore:
            if request._content is False:
                output += _build_data("--- Content Already Consumed "
                                      "/ Content was Streamed ---")
            else:
                output += _build_data(request.text, limit_body=limit_body)
        return "\n".join(output)

    def _generate_request_printout(my_request, ignore=[], limit_body=None):
        if request_obj is None:
            return "No Request"
        request = my_request.request
        output = ["{txt:>{padding}}:".format(
            txt="REQUEST", padding=left_column_width)]
        output.append("{txt:>{padding}}:  {method}".format(
            txt="Method", padding=left_column_width, method=request.method))
        output.append("{txt:>{padding}}:  {url}".format(
            txt="URL", padding=left_column_width, url=request.url))

        # Check for Redirects
        if len(my_request.history) > 0:
            response_codes = [x.status_code for x in my_request.history]
            output.append("{txt:>{padding}}:  {num} times, ({codes})".format(
                txt="Redirected", padding=left_column_width,
                num=len(my_request.history), codes=response_codes))
        else:
            output.append("{txt:>{padding}}:  False".format(
                txt="Redirected", padding=left_column_width))
        if "headers" not in ignore:
            output = output + _build_headers(request.headers)
        if "body" not in ignore:
            output = output + _build_data(request.body, limit_body)
        return "\n".join(output)

    if limit_body and not isinstance(limit_body, int):
        limit_body = None
    return "\n\n".join(
        [
            "{text:{fill}^{length}}".format(text="=", fill="=", length=100),
            _generate_request_printout(
                my_request=request_obj, ignore=ignore, limit_body=limit_body),
            "{text:{fill}^{length}}".format(text="-", fill="-", length=100),
            _generate_response_printout(
                my_request=request_obj, ignore=ignore, limit_body=limit_body)
        ])


def ellipsis_print(string, length):
    if length is None:
        return string
    if len(string) > length:
        return "{}...".format(string[0:length - 3])
    return string


def indent_text_block(text_block, indent):
    """Will indent an entire block of text

    ``text_block`` text block to indent
    ``indent`` if int number of spaces to indent, if str or unicode will use
               as the indent
    """
    if isinstance(indent, str):
        fill = indent
        indent = len(fill)
    elif isinstance(indent, int):
        fill = ""
        indent = indent
    else:
        fill = ""
        indent = 4
    lines = text_block.splitlines()
    return u"\n".join(["{fill:>{width}}{txt}".format(
        fill=fill, width=indent, txt=line) for line in lines])
