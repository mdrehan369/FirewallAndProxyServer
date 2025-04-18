from .helpers.DbHelper import DbHelper
from .helpers.RedisHelper import RedisHelper
from fastapi.templating import Jinja2Templates
import os

dbHelperInstance = DbHelper()
redisHelperInstance = RedisHelper()

templates = Jinja2Templates(directory=os.path.join(os.getcwd(), "app/templates"))