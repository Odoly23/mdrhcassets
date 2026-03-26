from staff.models import Employee

def c_user_staff(user):
    Employee.objects.select_related("employeeuser", "employeedivision__gabinete", "employeedivision__unidade","employeedivision__dg", "employeedivision__dn","employeedivision__department",).filter(employeeuser__user=user).first()
    obj = ""
    if objects: obj = objects
    return staff