def group_by_grades(students: list[tuple]):
    """
    Groups students by their grade.
    """
    student_per_grade = {}
    for student in students:
        name, grade = student
        student_per_grade.setdefault(grade, []).append(name)

    return student_per_grade


students = [
    ("Alice", "A"),
    ("Bob", "B"),
    ("Charlie", "A"),
    ("David", "C"),
    ("Eve", "B"),
]


print(group_by_grades(students))
