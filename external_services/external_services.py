routes = {"r11": "1, Больница - Завод" , "r22": "2, Площадь - Стадион", "r33": "3, БКЗ - Завод"}

rides = {"r11": {"z890": "10:00", "nw33": "11:00", "dew": "12:00", "xsq": "13:00", "mkm": "14:00"},
         "r22": {"zxcd": "10:15", "vfv": "11:15", "w2w2": "12:15"},
         "r33": {"yh": "10:30", "dede": "11:30", "mju": "12:30"}}

def get_routes() -> dict[str: str]:
    return routes

def get_route_name(route_id: str) -> str:
    return routes[route_id]

def get_rides(route: str) -> dict[str: str]:
    return rides[route]

def get_ride_time(route_id: str, ride_id:str) -> str:
    return rides[route_id][ride_id]

