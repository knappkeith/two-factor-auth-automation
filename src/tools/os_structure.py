import os
import json


def my_dir():
    """
    Returns current directory expanded
    """
    return os.path.abspath(os.curdir)


def does_directory_exist(path):
    """
    return boolean if a directory exists
    """
    return os.path.isdir(os.path.expanduser(path))


def get_containing_directory(path):
    """
    Returns the directory containing the path,
    if path is directory will return the parent directory
    """
    path = _get_full_path(path)
    if does_file_exist(path):
        return os.path.split(path)[0]
    elif does_directory_exist(path):
        return os.sep.join(path.split(os.sep)[0:-1])
    else:
        raise OSError(_build_error_str(2).format(arg=path))


def get_file_name(path):
    """
    Returns the file name of supplied path
    """
    return os.path.split(path)[1]


def create_directory(root_path, directory_name="", is_recursive=True):
    """
    Creates a directory in the root_path, is_recursive will make
    all needed directories in path
    """
    full_path = _get_full_path(root_path, directory_name)
    if does_directory_exist(full_path):
        return
    else:
        if is_recursive:
            os.makedirs(full_path)
        else:
            os.mkdir(full_path)


def does_file_exist(path):
    """
    return boolean if a file exists
    """
    return os.path.isfile(os.path.expanduser(path))


def get_file_path_counter(root_path, file_name, file_counter_offset=1):
    """
    returns a file path that doesn't exist based on a counter
    if ``{cnt}`` doesn't exist in file_name then file_name{_#}.file_name_ext
    will be used
    """

    # Check for `{cnt` and add if file_name already exists
    if "{cnt" not in file_name:
        if not does_file_exist(_get_full_path(root_path, file_name)):
            return _get_full_path(root_path, file_name)
        file_ext = os.path.splitext(file_name)
        file_name = "{name}_{{cnt:0>3}}{ext}".format(
            name=file_ext[0], ext=file_ext[1])

    # Loop until file name not found
    path = _get_full_path(root_path, file_name)
    counter = file_counter_offset
    while does_file_exist(path.format(cnt=counter)):
        counter += 1

    # Return file name
    return path.format(cnt=counter)


def delete_file(path):
    """
    will delete a single file
    """
    os.remove(_get_full_path(path))


def delete_all_files(root_path, file_pattern):
    """
    will delete all files found in the root_path that
    matches the file_pattern
    """

    # Get files from filter
    files_to_delete = find_files(root_path, file_pattern)
    rtn_array = []

    # Delete each file
    for file_to_delete in files_to_delete:
        try:
            os.remove(file_to_delete)
            rtn_array.append((file_to_delete, None))
        except Exception as e:
            rtn_array.append((file_to_delete, e))
    return rtn_array


def delete_directory(path):
    """
    will delete all files in a path recursively then delete
    all the directories in that path
    """

    # Delete the files
    delete_all_files(path, "*")

    # Delete the folder, if an error occurred it will
    #   bubble up here
    os.removedirs(path)


def read_file(path):
    """
    Reads a file and returns the string of that file
    """
    path = _get_full_path(path)

    # Make sure file exists
    if does_file_exist(path):

        # Check file Size, limited to 100MBi
        if os.path.getsize(path) > 100000000:
            raise OSError(_build_error_str(27).format(
                arg=os.path.getsize(path)))

        # Read File, and close
        try:
            with open(path, "r", encoding='utf-8') as fd:
                file_contents = fd.read()
        except UnicodeDecodeError:
            with open(path, "rb") as fd:
                file_contents = fd.read()
        return file_contents
    else:
        raise OSError(_build_error_str(2).format(arg=path))


def read_json_file(path):
    """
    Reads a file and returns the JSON of it
    """
    json_file = read_file(path)
    return json.loads(json_file)


def open_file(path, open_type='w', overwrite=False):
    """
    Returns an open file object
    """
    path = _get_full_path(path)
    open_type = open_type.lower()

    # Set Encoding Type
    if 'b' in open_type:
        my_encoding = None
    else:
        my_encoding = 'utf-8'

    # Open a write file
    if open_type in ['w', 'wb']:
        if overwrite:
            fd = open(path, open_type, encoding=my_encoding)
        else:
            if does_file_exist(path):
                raise OSError(_build_error_str(17).format(arg=path))
            else:
                fd = open(path, open_type, encoding=my_encoding)

    # Open an append file
    elif open_type == 'a':
        if does_file_exist(path):
            fd = open(path, open_type, encoding=my_encoding)
        else:
            raise OSError(_build_error_str(2).format(arg=path))
    elif open_type in ['r', 'rb', 'r+']:
        if does_file_exist(path):
            fd = open(path, open_type, encoding=my_encoding)
        else:
            raise OSError(_build_error_str(2).format(arg=path))

    # Raise error for unknown open_type
    else:
        raise OSError(_build_error_str(22).format(arg=open_type))
    return fd


def write_file(path, to_write, append=False, overwrite=False):
    """
    Writes to_write to a file of path.  append will append the passed
    file, overwrite will overwrite the file if it exists
    * to_write can be a list of strings - will be converted to single
      string with \n between lines
    * to_write can be a JSON Object - will be converted with json.dumps
    * to_write can be a str - preformatted and ready to go
    """
    path = _get_full_path(path)

    # Open file
    if append:
        my_file = open_file(path, 'a')
    else:
        if overwrite:
            my_file = open_file(path, 'w', overwrite=True)
        else:
            if does_file_exist(path):
                raise OSError(_build_error_str(17).format(arg=path))
            else:
                my_file = open_file(path, 'w')

    # Determine and convert what to write
    if isinstance(to_write, list) and isinstance(to_write[0], str):
        to_write = u"\n".join(to_write)
    elif isinstance(to_write, (list, dict)):
        try:
            to_write = json.dumps(to_write, indent=2)
        except Exception:
            to_write = str(to_write)

    # Write and close file
    try:
        my_file.write(str(to_write))
    except Exception:
        my_file.write(to_write)
    my_file.close()

    return path


def write_byte_file(path, to_write, overwrite=False):
    path = _get_full_path(path)

    # Open file
    if overwrite:
        my_file = open_file(path, 'wb', overwrite=True)
    else:
        if does_file_exist(path):
            raise OSError(_build_error_str(17).format(arg=path))
        else:
            my_file = open_file(path, 'wb')

    my_file.write(to_write)
    my_file.close()

    return path


def create_file_of_specific_size(path, size_in_bytes):
    '''
    Will crate a File of specified size
    '''
    file = open_file(path=path, open_type="wb")
    file.write("\0" * size_in_bytes)
    file.close()


def find_files(root_path, file_name):
    """
    will return a list of files that match pattern, only
    works with single ``*`` at beginning or end of file_name
    """
    # Ensure path is valid
    if not does_directory_exist(root_path):
        raise OSError(_build_error_str(20).format(arg=root_path))

    # Get all the files in the root
    files = _get_all_files_directories(root_path)[1]
    results = []

    # Filter and search for ``*text``
    if file_name.startswith("*"):
        file_name = file_name[1:]
        for i in files:
            if i.endswith(file_name):
                results.append(i)

    # Filter and search for ``text*``
    elif file_name.endswith("*"):
        file_name = file_name[:-1]
        for i in files:
            if os.path.split(i)[1].startswith(file_name):
                results.append(i)

    # Filter and search for an exact match on the file name
    else:
        for i in files:
            if i == file_name or os.path.split(i)[1] == file_name:
                results.append(i)
    return results


def _get_full_path(path, *p):
    """
    will join a path and expand the user, should
    be used by all functions
    """
    return os.path.abspath(os.path.expanduser(os.path.join(path, *p)))


def _get_all_files_directories(path):
    """
    returns all file and directory paths in the path
    """
    # Ensure path exists
    if not does_directory_exist(path):
        raise OSError(_build_error_str(2).format(arg=path))

    # Walk path and get all tuple sets
    walk = [x for x in os.walk(_get_full_path(path))]

    # Filter
    walk_dirs = [(x[0], x[1]) for x in walk if x[1] != []]
    walk_files = [(x[0], x[2]) for x in walk if x[2] != []]

    # Build Directory paths
    dirs = []
    for i in walk_dirs:
        dirs.extend([os.path.join(i[0], j) for j in i[1]])

    # Build File paths
    files = []
    for i in walk_files:
        files.extend([os.path.join(i[0], j) for j in i[1]])
    return dirs, files


def _build_error_str(err_num):
    """
    will build the error string to mimic the os library
    error string

    Common errors:
      1 - Operation not Permitted
      2 - No such file or directory
     13 - Permission Denied
     17 - File Exists
     20 - Not a directory
     27 - File too Large

    To get all:
    import os
    for key, val in os.errno.errorcode.iteritems():
        print "{}: {}".format(key, os.strerror(key))
    """
    return "[{estr} {enum}] {edesc}: {{arg}}".format(
        estr=os.errno.errorcode[err_num],
        enum=err_num,
        edesc=os.strerror(err_num))
