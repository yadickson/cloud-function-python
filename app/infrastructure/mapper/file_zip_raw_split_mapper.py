from typing import List

from app.infrastructure.mapper.file_zip_raw_split_mapper_interface import FileZipRawSplitMapperInterface


class FileZipRawSplitMapper(FileZipRawSplitMapperInterface):
    def get_parts(self, content: bytes) -> List[bytes]:
        occurrences = []
        start_index = 0  # pragma: no mutate
        target = b"\x50\x4b\x03\x04\x14"  # pragma: no mutate

        while True:
            index = content.find(target, start_index)  # pragma: no mutate
            if index == -1:  # pragma: no mutate
                break
            occurrences.append(index)
            start_index = index + len(target)  # pragma: no mutate

        contents = []

        if occurrences:
            start_index = occurrences[0]  # pragma: no mutate

            for pos in occurrences[1:]:
                contents.append(content[start_index:pos])
                start_index = pos

            contents.append(content[start_index:])

        return contents
