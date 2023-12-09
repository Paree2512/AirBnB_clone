#!/usr/bin/python3

"""
Console Module
Entry point of our command interpreter
"""

import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    # List to hold all classes created
    class_list = {"BaseModel": BaseModel, "User": User,
                  "State": State, "City": City, "Place": Place,
                  "Amenity": Amenity, "Review": Review}

    def emptyline(self):
        """Do nothing when empty line + ENTER"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def do_create(self, arg):
        """
        Usage: create <class_name>
        Create a new instance of BaseModel, save it and print id
        """
        if not arg:
            print("** class name missing **")
            return
        if arg in HBNBCommand.class_list:
            obj = eval(arg)()
            obj.save()
            print(obj.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Print the string representation of an instance
        Usage: show BaseModel 3195da8d-2c7e-464b-a028-1f123247f74f
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if args[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        objects = storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key in objects:
            print(objects[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance based on class name and id.
        Usage: destroy BaseModel 1234-1234-1234
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if args[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        objects = storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key in objects:
            objects.pop(key)
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """
        Print all string representations of instances
        Usage: all Basemodel or all
        """
        args = arg.split()
        objects = storage.all()

        if len(args) == 0:
            print([str(obj) for obj in objects.values()])
        elif len(args) == 1 and args[0] in HBNBCommand.class_list:
            print([str(obj) for obj in objects.values()
                   if type(obj).__name__ == args[0]])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """
        Update an instance attribute based on classname and id
        Usage: update <class> <id> <attribute name> <attribute value>
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if args[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        objects = storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key not in objects:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        if len(args) == 4:    
            obj = objects[key]
            attribute_name = args[2]
            # Remove leading and trailing whitespaces/quotes
            attribute_value = args[3].strip("'\"")
            if hasattr(obj, attribute_name):
                setattr(obj, attribute_name, attribute_value)
                obj.save()
        else:
            print("** attribute doesn't exist **")

    def do_count(self, arg):
        """
        Retrieve the number of instances of a class and send to stdout
        Usage: count User or State.count()
        """
        if arg in HBNBCommand.class_list:
            count = 0
            objects = storage.all()
            for key, objs in objects.items():
                if arg in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def exec_cls_first(self, class_name, arg):
        """
        Execution function for commands starting with class_name first used to:
        retrieve all instances of a class by using: <class name>.all().
        retrieve the number of instances of a class: <class name>.count().
        """
        if arg[:6] == ".all()":
            self.do_all(class_name)
        elif arg[:6] == '.show(':
            self.do_show(class_name + ' ' + arg[7:-2])
        elif arg[:8] == '.count()':
            self.do_count(class_name)
        elif arg[:9] == '.destroy(':
            self.do_destroy(class_name + ' ' + arg[10:-2])
        elif arg[:8] == '.update(':
            if '{' in arg and '}' in arg:
                new_arg = arg[8:-1].split('{')
                new_arg[1] = '{' + new_arg[1]
            else:
                new_arg = arg[8:-1].split(',')
            if len(new_arg) == 3:
                new_arg = " ".join(new_arg)
                new_arg = new_arg.replace("\"", "")
                new_arg = new_arg.replace("  ", " ")
                self.do_update(class_name + ' ' + new_arg)
            elif len(new_arg) == 2:
                try:
                    dict = eval(new_arg[1])
                except:
                    return
                for j in dict.keys():
                    self.do_update(class_name + ' ' + new_arg[0][1:-3] + ' ' +
                                   str(j) + ' ' + str(dict[j]))
            else:
                return
        else:
            print("Not a valid command.")

    def do_BaseModel(self, arg):
        """
        Usages:
        BaseModel.all(): retrieve all instances of the BaseModel class.
        BaseModel.count(): retrieves the number of instances in BaseModel class
        BaseModel.show(<id>): retrieves BaseModel instance based on its ID
        BaseModel.destroy(<id>): destroy BaseModel instance based on its ID
        BaseModel.update(<id>, <attribute name>, <attribute value>):
            update BaseModel instance based on its ID
        BaseModel.update(<id>, <dictionary representation>):
            update BaseModel instance based on its ID with a disctionary
        """
        self.exec_cls_first('BaseModel', arg)

    def do_User(self, arg):
        """
        Usages:
        User.all(): retrieve all instances of the User class.
        User.count(): retrieves the number of instances in User class
        User.show(<id>): retrieves User instance based on its ID
        User.destroy(<id>): destroy User instance based on its ID
        User.update(<id>, <attribute name>, <attribute value>):
            update User instance based on its ID
        User.update(<id>, <dictionary representation>):
            update User instance based on its ID with a disctionary
        """
        self.exec_cls_first('User', arg)

    def do_State(self, arg):
        """
        Usages:
        State.all(): retrieve all instances of the State class.
        State.count(): retrieves the number of instances in State class
        State.show(<id>): retrieves State instance based on its ID
        State.destroy(<id>): destroy State instance based on its ID
        State.update(<id>, <attribute name>, <attribute value>):
            update State instance based on its ID
        State.update(<id>, <dictionary representation>):
            update State instance based on its ID with a disctionary
        """
        self.exec_cls_first('State', arg)

    def do_City(self, arg):
        """
        Usages:
        City.all(): retrieve all instances of the City class.
        City.count(): retrieves the number of instances in City class
        City.show(<id>): retrieves City instance based on its ID
        City.destroy(<id>): destroy City instance based on its ID
        City.update(<id>, <attribute name>, <attribute value>):
            update City instance based on its ID
        City.update(<id>, <dictionary representation>):
            update City instance based on its ID with a disctionary
        """
        self.exec_cls_first('City', arg)

    def do_Place(self, arg):
        """
        Usages:
        Place.all(): retrieve all instances of the Place class.
        Place.count(): retrieves the number of instances in Place class
        Place.show(<id>): retrieves Place instance based on its ID
        Place.destroy(<id>): destroy Place instance based on its ID
        Place.update(<id>, <attribute name>, <attribute value>):
            update Place instance based on its ID
        Place.update(<id>, <dictionary representation>):
            update Place instance based on its ID with a disctionary
        """
        self.exec_cls_first('Place', arg)

    def do_Amenity(self, arg):
        """
        Usages:
        Amenity.all(): retrieve all instances of the Amenity class.
        Amenity.count(): retrieves the number of instances in Amenity class
        Amenity.show(<id>): retrieves Amenity instance based on its ID
        Amenity.destroy(<id>): destroy Amenity instance based on its ID
        Amenity.update(<id>, <attribute name>, <attribute value>):
            update Amenity instance based on its ID
        Amenity.update(<id>, <dictionary representation>):
            update Amenity instance based on its ID with a disctionary
        """
        self.exec_cls_first('Amenity', arg)

    def do_Review(self, arg):
        """
        Usages:
        Review.all(): retrieve all instances of the Review class.
        Review.count(): retrieves the number of instances in Review class
        Review.show(<id>): retrieves Review instance based on its ID
        Review.destroy(<id>): destroy Review instance based on its ID
        Review.update(<id>, <attribute name>, <attribute value>):
            update Review instance based on its ID
        Review.update(<id>, <dictionary representation>):
            update Review instance based on its ID with a disctionary
        """
        self.exec_cls_first('Review', arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
