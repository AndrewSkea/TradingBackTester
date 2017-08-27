def percent_change(_start_point, _current_point):
    try:
        if _start_point > _current_point:
            x = -((float(_start_point) - float(_current_point)) / abs(_current_point)) * 100
        else:
            x = ((float(_current_point) - float(_start_point)) / abs(_start_point)) * 100
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.000000001