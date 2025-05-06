from collections import defaultdict


def group_by_grades(students: list[tuple]):
    """
    Groups students by their grade.
    """
    student_per_grade = defaultdict(list)
    for name, grade in students:
        student_per_grade[grade].append(name)

    return student_per_grade.items()


students = [
    ("Alice", "A"),
    ("Bob", "B"),
    ("Charlie", "A"),
    ("David", "C"),
    ("Eve", "B"),
]


print(group_by_grades(students))
