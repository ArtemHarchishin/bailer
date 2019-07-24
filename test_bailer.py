import bailer
import time
import pytest

def setup_function(function):
    bailer.init_storage()

def assert_list(l, amount):
    assert isinstance(l, list)
    assert len(l) == amount


def test_flower_entry():
    # Given
    flower_name = "foo"
    watering_interval = 1000
    
    # When 
    entry = bailer.create_flower_entry(flower_name, watering_interval)

    # Then
    assert str(entry) == entry.to_string()

# ADD ===============================================================

def test_add_flower():
    # Given
    flower_name = "foo"
    watering_interval = 1000
    
    # When 
    bailer.add_flower(flower_name, watering_interval)

    # Then
    flowers = bailer.get_all_flowers()
    assert_list(flowers, 1)

    # When 
    watering_interval = "1000"
    bailer.add_flower(flower_name, watering_interval)

    # Then
    flowers = bailer.get_all_flowers()
    assert_list(flowers, 2)
    

def test_add_flower_with_empty_name():
    # Given
    flower_name = None
    watering_interval = 1000
    
    # When
    with pytest.raises(Exception, match="Flower's name can't be empty."): 
        bailer.add_flower(flower_name, watering_interval)

    # Then
    # Expected exception


def test_add_flower_with_negative_interval():
    # Given
    flower_name = "None"
    watering_interval = -1000
    
    # When
    with pytest.raises(Exception, match="Watering interval can't be negative or zero."): 
        bailer.add_flower(flower_name, watering_interval)

    # Then
    # Expected exception


def test_add_flower_with_zero_interval():
    # Given
    flower_name = "None"
    watering_interval = 0
    
    # When
    with pytest.raises(Exception, match="Watering interval can't be negative or zero."): 
        bailer.add_flower(flower_name, watering_interval)

    # Then
    # Expected exception


# REMOVE ===============================================================

def test_remove_not_exists_flower():
    # Given
    flower_name = "tree"

    # When 
    removed = bailer.remove_flower(flower_name)

    # Then 
    assert not removed
    flowers = bailer.get_all_flowers()
    assert_list(flowers, 0)


def test_remove_exists_flower():
    # Given
    flower_name = "tree"
    watering_interval = 1000

    # When 
    bailer.add_flower(flower_name, watering_interval)

    # Then 
    flowers = bailer.get_all_flowers()
    assert_list(flowers, 1)

    # When 
    removed = bailer.remove_flower(flower_name)

    # Then 
    assert removed
    flowers = bailer.get_all_flowers()
    assert_list(flowers, 0)


# WATERING ===============================================================

def test_water_flower_watered():
    # Given
    flower_name = "small_tree"
    watering_interval = 1
    bailer.add_flower(flower_name, watering_interval)

    # When 
    time.sleep(2)
    watered = bailer.water_flower(flower_name)

    # Then 
    assert watered
    assert_list(bailer.need_watering_list(), 0)


def test_water_flower_not_watered():
    # Given
    flower_name = "small_tree"
    watering_interval = 1000
    bailer.add_flower(flower_name, watering_interval)

    # When 
    watered = bailer.water_flower(flower_name)

    # Then 
    assert not watered
    assert_list(bailer.need_watering_list(), 0)


def test_water_flower_many():
    # Given
    small_tree = "small_tree"
    watering_interval = 1000
    bailer.add_flower(small_tree, watering_interval)

    tree = "tree"
    watering_interval = 100
    bailer.add_flower(tree, watering_interval)

    big_tree = "big_tree"
    watering_interval = 1
    bailer.add_flower(big_tree, watering_interval)

    # When 
    time.sleep(2)
    watered = bailer.water_flower(big_tree)

    # Then 
    assert watered
    l = bailer.need_watering_list()
    assert_list(l, 0)


# WATERING LIST ===============================================================

def test_need_watering_one():
    # Given
    flower_name = "small_tree"
    watering_interval = 1
    bailer.add_flower(flower_name, watering_interval)

    # When 
    time.sleep(2)

    # Then 
    assert_list(bailer.need_watering_list(), 1)


def test_need_watering_zero():
    # Given
    flower_name = "small_tree"
    watering_interval = 1
    bailer.add_flower(flower_name, watering_interval)

    # When 
    time.sleep(2)

    # Then 
    assert_list(bailer.need_watering_list(), 1)

    # When 
    watered = bailer.water_flower(flower_name)

    # Then 
    assert watered
    assert_list(bailer.need_watering_list(), 0)


def test_need_watering_many():
    # Given
    small_tree = "small_tree"
    watering_interval = 1
    bailer.add_flower(small_tree, watering_interval)

    tree = "tree"
    watering_interval = 1
    bailer.add_flower(tree, watering_interval)

    big_tree = "big_tree"
    watering_interval = 1
    bailer.add_flower(big_tree, watering_interval)

    # When 
    time.sleep(2)

    # Then 
    assert_list(bailer.need_watering_list(), 3)


# NOTIFY ===============================================================

def test_notify_callback_not_func():
    # Given
    bailer.init_notice()

    small_tree = "small_tree"
    watering_interval = 3
    bailer.add_flower(small_tree, watering_interval)    

    # When
    with pytest.raises(Exception, match="Callback incorrect - _not_func"): 
        bailer.add_notify_callback("_not_func") 

    # Then 
    # Expected exception


@pytest.mark.asyncio
async def test_notify():
    # Given
    def callback_1():
        print()
        print("callback_1")
        bailer.remove_notify_callback(callback_1)

    def callback_2(need_watering):
        print()
        print(need_watering)
        bailer.remove_notify_callback(callback_2)

    bailer.init_notice(5)

    small_tree = "small_tree"
    watering_interval = 3
    bailer.add_flower(small_tree, watering_interval)    
    big_tree = "big_tree"
    watering_interval = 1000
    bailer.add_flower(big_tree, watering_interval)

    # When
    bailer.add_notify_callback(callback_1) 
    bailer.add_notify_callback(callback_2) 

    # Then 
    time.sleep(100)