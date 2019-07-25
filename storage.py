from collections import defaultdict
import functools
import os
from flower_entry import create_from_string

class Storage(object):
    def __init__(self, l=None, by_id=None, by_name=None):
        self._list = l or []
        self._by_id = by_id or {}
        self._by_name = by_name or defaultdict(list)

    @property
    def list(self):
        return self._list

    @property
    def by_id(self):
        return self._by_id

    @property
    def by_name(self):
        return self._by_name

    def add_entry(self, entry):
        self._list.append(entry)
        self._by_id[entry.id] = entry
        self._by_name[entry.name].append(entry)

    def delete_entry(self, entry):
        exists_entry = self._by_id.get(entry.id, None)
        if exists_entry:
            entries = self._by_name[exists_entry.name]
            entries.remove(exists_entry)
            self._list.remove(exists_entry)
            del self._by_id[exists_entry.id]

            return True

        return False

    def delete_entry_by_name(self, name):
        entries = self._by_name[name]
        if entries:
            entry = entries.pop()
            self._list.remove(entry)
            del self._by_id[entry.id]

            if not entries:
                del self._by_name[name]

            return True

        return False



class FileStorage(Storage):
    def __init__(self, filename):
        Storage.__init__(self)
        self._filename = filename
        self._read()

    def _read(self):
        if not os.path.exists(self._filename):
            with open(self._filename, 'w') as f:
                pass

        s = ""

        with open(self._filename, 'r') as f:
            s = f.read()
            
        ss = s.split(";")

        for s in ss:
            if s:
                entry = create_from_string(s)
                self.add_entry(entry)
    
    def _flush(self):
        with open(self._filename, 'w') as f:
            s = functools.reduce(lambda acc, item: acc + str(item), self._list, "")
            f.write(s)
    
    def add_entry(self, entry):
        Storage.add_entry(self, entry)
        self._flush()

    def delete_entry(self, entry):
        deleted = Storage.delete_entry(self, entry)
        self._flush()
        return deleted

    def delete_entry_by_name(self, name):
        deleted = Storage.delete_entry_by_name(self, name)
        self._flush()
        return deleted

        
