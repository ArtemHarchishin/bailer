from collections import defaultdict
import functools
import os

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
        self._filename = filename
        Storage.__init__(self, *self._read())

    def _read(self):
        if not os.path.exists(self._filename):
            with open(self._filename, 'w') as f:
                pass
                
        with open(self._filename, 'r') as f:
            print(f.readlines())
        return [], {}, defaultdict(list)
    
    def _flush(self):
        with open(self._filename, 'w') as f:
            s = functools.reduce(lambda acc, item: acc + str(item), self._list, "")
            f.write(s)
    
    def delete_entry(self, entry):
        Storage.delete_entry(self, entry)
        self._flush()

    def delete_entry_by_name(self, name):
        Storage.delete_entry_by_name(self, name)
        self._flush()

    def add_entry(self, entry):
        Storage.add_entry(self, entry)
        self._flush()
        
