import app

def test_add_flower():
    # Given
    flower_name = "foo"
    watering_interval = 1000
    
    # When 
    app.add_flower(flower_name, watering_interval)

    # Then
    flowers = app.what_need_watering()
    flower = flowers[0]
    print(flower)
    assert isinstance(flowers, list)
    assert len(flowers) == 1
    assert flower.name == flower_name
    assert flower.watering_interval == watering_interval

def test_remove_flower():
    pass

def test_watering_flower():
    pass

def test_what_need_watering():
    pass