#!/usr/bin/python3
""" Command Line Interpreter using cmd Module """

import cmd
import json
import os

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

""" A list of all classes """
CLASS_LIST = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
FUNCTIONS = ["all", "count", "show", "destroy", "update"]

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_quit(self, line):
        """ quit command to exit the program
            Args:
                line: a string containig command arguments.
        """
        return (True)

    def do_EOF(self, line):
        """EOF command to exit the program
           Args:
               line: a string containig command arguments.
        """
        print()
        return (True)

    def emptyline(self):
        """overwrite the emptyline not to execute anything"""
        pass

    def do_create(self, args):
        arg_list1 = args.split()
        if len(arg_list1) < 1:
            print("** class name missing **")
            return (False)

        arg = arg_list1[0]

        if arg not in CLASS_LIST:
            print("** class doesn't exist **")
            return (False)
        obj = self.create_obj(arg)
        if obj:
            print(obj)

    def create_obj(self, class_name):
        if class_name == "BaseModel":
            base_model = BaseModel()
            base_model.save()
            return (base_model.id)
        if class_name  == "User":
            user = User()
            user.save()
            return (user.id)
        if class_name == "State":
            state = State()
            state.save()
            return (state.id)
        if class_name == "City":
            city = City()
            city.save()
            return (city.id)
        if class_name == "Amenity":
            amenity = Amenity()
            amenity.save()
            return (amenity.id)
        if class_name  == "Place":
            place = Place()
            place.save()
            return (place.id)
        if class_name == "Review":
            review = Review()
            review.save()
            return (review.id)
        return (None)

    def do_all(self, arg):
        """Prints all string representations of all instances based
        or not on the class name.
        Args:
            arg: a string containig command arguments.
        """
        arg_list = arg.split()
        object_dict = storage.all()
        if not arg_list:
            object_list = list(object_dict.values())
        elif arg_list[0] not in CLASS_LIST:
            print("** class doesn't exist **")
            return
        else:
            object_list = [
                    i for i in object_dict.values(
                        ) if i.__class__.__name__ == arg_list[0]]

            print([str(i) for i in object_list])                                    

    def do_show(self, arg):
        """Prints the string representation of an instance
           based on the class name and id.
           Args:
               arg: a string containig command arguments.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            obj_dict = storage.all()
            if key in obj_dict:
                print(obj_dict[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg) -> None:
        """Deletes an instance based on the class name and id
           (save the change into the JSON file).
           Args:
               arg: a string containig command arguments
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            obj_dict = storage.all()
            if key in obj_dict:
                del obj_dict[key]
            else:
                print("** no instance found **")
            storage.save()

    def do_all(self, arg) -> None:
        """Prints all string representations of all instances based
           or not on the class name.
           Args:
               arg: a string containig command arguments.
        """
        args = arg.split()
        obj_dict = storage.all()
        if not args:
            obj_list = list(obj_dict.values())
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        else:
            obj_list = [
                obj for obj in obj_dict.values()
                if obj.__class__.__name__ == args[0]
            ]
        print([str(obj) for obj in obj_list])

    def do_update(self, args):
        """Updates an instance based on the class name and id by
           adding or updating attribute.
           Args:
               arg: a string containig command arguments.
        """

        attrs = {}
        if "from_func" in args:
            arg = args
            attrs = json.loads(arg[2])
        else:
            arg = args.split()

        if not arg:
            print("** class name missing **")
        elif arg[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(arg) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(arg[0], arg[1])
            obj_dict = storage.all()

            if key not in obj_dict:
                print("** no instance found **")
            elif len(arg) < 3:
                print("** attribute name missing **")
            elif len(arg) < 4:
                print("** value missing **")
            else:
                obj = obj_dict[key]
                if len(attrs) > 0:
                    for key, val in attrs.items():
                        setattr(obj, key, val)
                else:
                    attribute_name = arg[2]
                    attribute_value = arg[3].strip("\"")
                    setattr(obj, attribute_name, attribute_value)
                obj.save()

    def __do_count(self, obj):
        """ count the number of objects in storage
            Return:
                  number of objects in storage
        """
        obj_dict = storage.all()
        count = 0

        for key, value in obj_dict.items():
            to_dict = value.to_dict()
            if to_dict["__class__"] == obj:
                count += 1

        print(count)

    def _default_process(self, line):
        """ called on an input line when,
            the command prefix is not recognized
            Args:
                line: a string containing commandline arguments
        """
        arguments = line.split(".", 1)
        if len(args) != 2:
            return (cmd.Cmd.default(self, line))
        if args[0] not in CLASS_LIST:
            return (cmd.Cmd.default(self, line))
        if "(" not in args[1] or ")" not in args[1]:
            return (cmd.Cmd.default(self, line))
        args = line.replace("(", " ").replace(")", " ")
        args = args.replace('"', '').replace("'", " ").replace(",", "")
        args = args.strip()
        if not self.__run_functions(line, args):
            cmd.Cmd.default(self, line)

    def default(self, line):
        return self._default_process(line)
    def execute_command(self, line, args):
        """ method to to invoke all the functions
            Args:
                line: string of arguments
                args: an array of arguments
            Return:
                  True if function is run else False
        """
        args_list = args.split(" ")
        class_name = args_list[0].split(".")[0]
        function_name = args_list[0].split(".")[1]
        length = len(args_list)
        if function_name not in FUNCTIONS:
            return False
        del args_list[0]
        args_list.insert(0, class_name)

        if function_name == "all":
            self.do_all(class_name)
            return True
        if function_name == "count":
            self.__do_count(class_name)
            return True
        if function_name == "show":
            self.do_show(" ".join([args_list[x] for x in range(length)]))
            return True
        if function_name == "destroy":
            self.do_destroy(" ".join([args_list[x] for x in range(length)]))
            return True

        new_args_list = line.split(" ", 1)
        to_data = ""

        if len(new_args_list) > 1:
            try:
                new_args_list[1] = new_args_list[1].replace("'", '"')
                to_data = json.loads(new_args_list[1].strip(")"))
            except Exception as ie:
                to_data = ""

        if function_name == "update" and isinstance(to_data, dict):
            arr = [class_name, args_list[1], json.dumps(to_data)]
            arr.append("from_func")
            self.do_update(arr)
            return True
        else:
            if length > 4:
                length = 4
            arr = [args_list[x].strip(")") for x in range(length)]
            self.do_update(" ".join(arr))
            return True
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
