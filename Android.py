# coding=utf-8
import os
import re
from adb_android import adb_android

# Имя папки для бэкапа
dir_backup = "backup_tmp"

# Бекапить большие разделы? (userdata, system_a, system_b etc)
big_partition = False


adb_android.wait_for_device()  # Ждем устройство

# Получаем список разделов  с именами
partition_list_table = adb_android.shell("ls -l /dev/block/platform/soc/c0c4000.sdhci/by-name/")

# Разбивем список по строкам.
partition_list_clean = partition_list_table[1].split("\n")

# Чистим список от первого и последнего элемента. Там мусор.
partition_list_clean.pop()
partition_list_clean.pop(0)

# Список имен
list_name_partition = []

# Список путей до разделов
list_block_path = []

# Собираем регуляркой из построчного списка пути до разбелов и их имена.
while len(partition_list_clean) > 0:
    regex = r"\W([a-z_]+)\W\W+(\/dev\/block\/[a-z0-9]+)"
    line = partition_list_clean.pop()
    matches = re.finditer(regex, line, re.MULTILINE)
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            print ("Found {groupNum} - {group}".format(groupNum=groupNum, group=match.group(groupNum)))
            if groupNum == 1:
                list_name_partition.append(match.group(groupNum))
            if groupNum == 2:
                list_block_path.append(match.group(groupNum))
print ("В списке имен разделов {size} названий".format(size=len(list_name_partition)))
print ("В списке  разделов {size} путей".format(size=len(list_block_path)))
if len(list_block_path) != len(list_name_partition):
    print("Длинна списков разная. Этого не может быть")
    exit(1)
# Бекапимся
if os.path.isdir(dir_backup):
    print("Директория backup уже есть!")
    exit(1)
if os.path.isfile(dir_backup):
    print("backup это файл. Можно создавать каталог.")
os.mkdir(dir_backup)
real_path = os.getcwd()
os.chdir(dir_backup)

while len(list_block_path) > 0:
    name = list_name_partition.pop()
    block = list_block_path.pop()

    if name == "userdata":
        if not big_partition:
            continue

    if name == "system_a":
        if not big_partition:
            continue

    if name == "system_b":
        if not big_partition:
            continue

    adb_android.pull(block, name)

os.chdir(real_path)
pass
