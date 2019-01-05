# coding: utf-8


def filter_block_content(old_file, new_file, start_word, filter_word):
    """
    Treat string content between two words given by start_word as a block.
    Delete a block that contains the keyword given by filter_word.
    """
    is_filter = 0
    block_num = 0
    block_str = ''
    with open(old_file) as f, open(new_file, 'w') as f2:
        for line in f:
            sline = line.strip()
            if sline.startswith('#'):
                # ignore and keep comment lines
                block_str += line
                continue
            elif sline.startswith(start_word):
                # save a block if not filtered
                if is_filter == 0:
                    f2.write(block_str)
                # then reset blcok
                block_str = line
                block_num += 1
                # and reset filter flag
                is_filter = 0
            else:
                block_str += line
                if filter_word in line:
                    is_filter = 1
        # process the last one
        if is_filter == 0:
            f2.write(block_str)
    print('{} blocks processed'.format(block_num))


if __name__ == '__main__':
    # example: delete a caffe layer that contains 'TRAIN'
    filter_block_content("ResNet.prototxt", 'cvt.prototxt', 'layer', 'TRAIN')
