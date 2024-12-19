from background_task import background
from background_task.models import Task

from house.models import House
from task.models import COMPLETE

@background(schedule=10)
def calculate_house_stats():
    print("Starting calculate_house_stats task...")

    houses = House.objects.all()
    print(f"Fetched houses: {houses}")

    for house in houses:
        print(f"Processing house: {house.id}, name: {house}")
        total_tasks = 0
        completed_tasks_count = 0
        house_task_lists = house.lists.all()
        print(f"Task lists for house {house.id}: {house_task_lists}")

        for task_list in house_task_lists:
            print(f"Processing task list: {task_list.id}, name: {task_list}")
            tasks_in_list = task_list.tasks.count()
            total_tasks += tasks_in_list
            print(f"Total tasks in list {task_list.id}: {tasks_in_list}")

            completed_in_list = task_list.tasks.filter(status=COMPLETE).count()
            completed_tasks_count += completed_in_list
            print(f"Completed tasks in list {task_list.id}: {completed_in_list}")

        not_completed = total_tasks - completed_tasks_count
        print(f"House {house.id} stats: Total tasks={total_tasks}, Completed={completed_tasks_count}, Not completed={not_completed}")

        house.completed_tasks_count = completed_tasks_count
        house.notcompleted_tasks_count = not_completed
        house.save()
        print(f"Updated house {house.id} with new stats.")

    print("Finished calculate_house_stats task.")

# Check if the task is already scheduled by filtering by verbose_name
task_exists = Task.objects.filter(verbose_name='calculate_house_stats').exists()
if not task_exists:
    print("Scheduling the calculate_house_stats task...")
    calculate_house_stats(repeat=Task.DAILY, verbose_name='calculate_house_stats', priority=0)
    print("Task scheduled successfully.")
else:
    print("Task already scheduled.")
