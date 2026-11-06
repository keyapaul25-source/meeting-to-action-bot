import re


def test_extract_tasks_detects_owner_and_deadline():
    text = "Rahul will complete the frontend by Friday. Priya will handle backend integration."
    from meeting_bot.task_extractor import extract_tasks

    tasks = extract_tasks(text)
    assert any(task["task"] == "Complete frontend" and task["owner"] == "Rahul" for task in tasks)
    assert any(task["task"] == "Handle backend integration" and task["owner"] == "Priya" for task in tasks)


def test_extract_tasks_flags_missing_information():
    text = "The team will finalise project documentation."
    from meeting_bot.task_extractor import extract_tasks

    tasks = extract_tasks(text)
    assert tasks[0]["missing_owner"] is True or tasks[0]["missing_deadline"] is True
