import os
from time import time
from django.utils import timezone


# accepts 1 optional argument 'dir_name' - the initial path to save
# format for receiving argument 'dir_name' - 'animals/dog'
def path_upload(dir_name=''):
    # def wrap(instance, filename):
    #     date = timezone.now()
    #     ext = filename.split('.')[-1]
    #     filename = "%s.%s" % (str(date.second) + filename.split('.')[0].lower() + str(int(time())), ext)
    #     if dir_name:
    #         template_path = f'{dir_name}/{instance}/{date.year}/{date.month}/{date.day}/{date.hour}/{date.minute}'
    #     else:
    #         template_path = f'{instance}/{date.year}/{date.month}/{date.day}/{date.hour}/{date.minute}'
    #     return os.path.join(template_path, filename)
    return 'wrap'

# def path_upload(dir_name=''):
#     def wrap(instance, filename):
#         date = timezone.now()
#         ext = filename.split('.')[-1]
#         filename = "%s.%s" % (str(date.second) + filename.split('.')[0].lower() + str(int(time())), ext)
#         if dir_name:
#             template_path = f'{dir_name}/{instance}/{date.year}/{date.month}/{date.day}/{date.hour}/{date.minute}'
#         else:
#             template_path = f'{instance}/{date.year}/{date.month}/{date.day}/{date.hour}/{date.minute}'
#         return os.path.join(template_path, filename)
#
#     return wrap
