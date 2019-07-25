import bailer
import pytest
from storage import Storage
from flower_entry import FlowerEntry

storage = None
flower_entry = None

def setup_function(function):
    global storage, flower_entry

    storage = Storage()
    flower_entry = FlowerEntry(1, "tree", 1, 1)


def assert_is_entry_in_storage(storage, flower_entry, amount, exists):
    assert len(storage.list) == amount
    assert len(storage.by_name[flower_entry.name]) == amount
    if exists:
        assert exists and flower_entry.id in storage.by_id
    else:
        assert not exists and not flower_entry.id in storage.by_id

# Storage ==============================================================

def test_storage_property():
    # Given
    

    # When
    storage.list.append(flower_entry)
    storage.by_id[flower_entry.id] = flower_entry
    storage.by_name[flower_entry.name].append(flower_entry)
    
    # Then
    assert_is_entry_in_storage(storage, flower_entry, amount=1, exists=True)


def test_storage_add_entry():
    # Given
    

    # When
    storage.add_entry(flower_entry)
    
    # Then
    assert_is_entry_in_storage(storage, flower_entry, amount=1, exists=True)


def test_storage_delete_entry_true():
    # Given
    storage.add_entry(flower_entry)

    # When
    deleted = storage.delete_entry(flower_entry)
    
    # Then
    assert deleted
    assert_is_entry_in_storage(storage, flower_entry, amount=0, exists=False)


def test_storage_delete_entry_false():
    # Given
    

    # When
    deleted = storage.delete_entry(flower_entry)
    
    # Then
    assert not deleted
    assert_is_entry_in_storage(storage, flower_entry, amount=0, exists=False)


def test_storage_delete_entry_by_name_true():
    # Given
    storage.add_entry(flower_entry)

    # When
    deleted = storage.delete_entry_by_name(flower_entry.name)
    
    # Then
    assert deleted
    assert_is_entry_in_storage(storage, flower_entry, amount=0, exists=False)


def test_storage_delete_entry_by_name_false():
    # Given
    

    # When
    deleted = storage.delete_entry_by_name(flower_entry)
    
    # Then
    assert not deleted
    assert_is_entry_in_storage(storage, flower_entry, amount=0, exists=False)