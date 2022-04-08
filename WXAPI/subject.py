class Subject:
    gradePoint = ""
    score = ""
    credit = ""
    schoolYear = ""
    semester = ""
    name = ""
    grade = ""
    class_ = ""
    teacher = ""

    def __init__(self, credit, score, gradePoint, schoolYear, name, grade, class_, teacher, semester):
        self.gradePoint = gradePoint
        self.score = score
        self.credit = credit
        self.schoolYear = schoolYear
        self.name = name
        self.grade = grade
        self.class_ = class_
        self.teacher = teacher
        self.semester = semester

    def jsonserializer(self):
        return {
            'gradePoint': self.gradePoint,
            'score': self.score,
            'credit': self.credit,
            'schoolYear': self.schoolYear,
            'name': self.name,
            'grade': self.grade,
            'class': self.class_,
            'teacher': self.teacher,
            'semester': self.semester
        }
