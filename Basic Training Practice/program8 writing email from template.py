#lista tuple [(numefisier, numarul liniei, tipul erorii, numele utilizatorului, departamentul)....]

def mailTo(mail_address, mail_message):
    print(mail_message)

def composeMail():
    global list_errors
    for x in range(0, len(list_errors)):
        email = ("Dear {0}{1}".format(list_errors[x].get("name"), ",\n\n"))
        email += ("The file: {0} contains an error of type \"{1}\" at line: {2},\n" \
                  .format(list_errors[x].get("file"), list_errors[x].get("error_type"), list_errors[x].get("line")))
        email += ("Please solve the error as soon as possible.\n")
        email += ("Your sincere: %s\n" % list_errors[x].get("department"))
        mailTo(list_errors[x].get("name"), email)

def composeMailFromTemplate():
    global list_errors
    file = open("mail_template.txt", "r")
    email_template = ""
    for line in file:
        email_template += line
    file.close()
    for x in range(0, len(list_errors)):
        email = email_template
        email=email.replace("USER_NAME", list_errors[x].get("name"))
        email=email.replace("LINE", str(list_errors[x].get("line")))
        email=email.replace("DEPARTMENT_NAME", list_errors[x].get("department"))
        email=email.replace("ERROR_MESSAGE", list_errors[x].get("error_type"))
        email=email.replace("FILE_NAME", list_errors[x].get("file"))
        mailTo(list_errors[x].get("name"), email)

list_errors = [{"file":"supplier.c", "line":5874, "error_type":"Missing semi-colon", "name":"Ioan Gheba", "department":"Code Management & Quality"},
                {"file":"stubs.h", "line":778, "error_type":"double definition", "name":"Markus Apostol", "department":"Code Management & Quality"},
                {"file":"stubs.c", "line":8892, "error_type":"redefinition of variable", "name":"Antony Skeptra", "department":"Code Management & Quality"},
                {"file":"extern_decl.c", "line":909, "error_type":"cannot #include file extern_dec.h", "name":"Anemona Dolores", "department":"Code Management & Quality"}]

composeMailFromTemplate()
print("\nAll the users have been notified.".upper())