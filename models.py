class Category:
    """Класс - создание категорий и их методы."""
    def __init__(self, cat_name):
        self.name = cat_name
        self.courses_dict = dict()

    def course_count(self):
        return len(self.courses_dict) if self.courses_dict else 0


class CategoryRepo:
    """Класс - хранение и управление объектами категорий."""
    object_dict = dict()

    @classmethod
    def add_category(cls, cat_name, courses_set=None):
        """Создать объект категории и сохранить его."""
        category_obj = Category(cat_name)

        # Если такой категории еще не существует, добавить её в словарь объектов категорий.
        if category_obj.name not in cls.object_dict:
            cls.object_dict[category_obj.name] = category_obj

        # Если передано множество содержащее курсы, наполнить ими текущий объект.
        if courses_set:
            cls.fill_with_courses(category_obj, courses_set)

    @classmethod
    def fill_with_courses(cls, category_obj, courses_set):
        """Наполнить объект категория объектами входящих в него курсов."""
        for course_name in courses_set:

            # Если в словаре курсов объекта категории нет текущего курса, добавить его.
            if course_name not in category_obj.courses_dict:
                course_obj = CourseRepo.add_course(course_name, category_obj.name)
                category_obj.courses_dict[course_name] = course_obj

    @classmethod
    def delete_category(cls, category_obj):
        """Удалить категорию."""
        try:
            cls.object_dict.pop(category_obj.name)
        except KeyError:
            print('Такой категории не существует!')

    @classmethod
    def load_categories(cls):
        """Получить список объектов категорий."""
        return cls.object_dict.values()


class Course:
    """Класс - создание объектов 'курс' и их методы."""
    def __init__(self, course_name, cat_name):
        self.name = course_name
        self.category = cat_name


class CourseRepo:
    """Класс - хранение и управление объектов курсов."""
    object_dict = dict()

    @classmethod
    def add_course(cls, course_name, cat_name):
        """Создать объект курса и сохранить его."""
        course_obj = Course(course_name, cat_name)

        # Если такого курса не существует, добавляем его в словарь объектов курсов.
        if course_obj.name not in cls.object_dict:
            cls.object_dict[course_obj.name] = course_obj

            # Получить объект категории, в который будет добавлен данный курс.
            category_obj = CategoryRepo.object_dict[course_obj.category]

            # Добавить новый курс в соответствующий объект категории.
            CategoryRepo.fill_with_courses(category_obj, {course_obj.name})
            return course_obj

    @classmethod
    def delete_course(cls, course_obj):
        """Удалить объект курса."""
        try:
            cls.object_dict.pop(course_obj.name)
        except KeyError:
            print('Такого курса не существует!')

    @classmethod
    def load_courses(cls):
        """Получить список объектов курсов."""
        return cls.object_dict.values()


def create_category_obj():
    """Создать объекты категорий и курсов этих категорий."""
    CategoryRepo.add_category('Python', {'Основы Питона', 'Алгоритмы', 'Клиент-серверные приложения'})
    CategoryRepo.add_category('JavaScript', {'Основы JS', 'Продвинутый JS'})
    CategoryRepo.add_category('DataBase', {'MySql', 'PostgreSql', 'Не реляционные БД'})


if __name__ == '__main__':
    create_category_obj()
