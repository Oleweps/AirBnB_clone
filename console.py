#!/usr/bin/python3
""" Method Command Interpreter Command Line Interpreter using cmd Module """

import cmd
import json
import os
import models

from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

""" A list of all classes """
CLASSES = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_quit(self, line) -> bool:
        """ quit command to exit the program
            Args:
                line: a string containig command arguments.
        """
        return True

    def do_EOF(self, line) -> bool:
        """EOF command to exit the program
           Args:
               line: a string containig command arguments.
        """
        print()
        return True

    def emptyline(self) -> None:
        """overwrite the emptyline not to execute anything"""
        pass

    def do_create(self, arg) -> None:
        """Creates a new instance of BaseModel, saves it
           and prints the id.
           Usage: create <class name>
           Args:
               arg: a string containig command arguments
        """
        if not arg:
            print("** class name missing **")
        elif arg not in CLASSES:
            print("** class doesn't exist **")
        else:
            new_creation = eval(arg[0] + '()')
            models.storage.save()
            print(new_creation.id)

    def do_show(self, arg) -> None:
        """Prints the string representation of a specific instance
           based on the class name and id.
           Usage: show <class name> <id>
           Args:
               arg: a string containig command arguments.
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key_value = "{}.{}".format(args[0], args[1])
            obj_dict = storage.all()
            if key_value in obj_dict:
                print(obj_dict[key_value])
            else:
                print("** no instance found **")

    def do_destroy(self, arg) -> None:
        """Deletes an instance based on the class name and id
           (save the change into the JSON file).
           Usage: destroy <class name> <id>
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key_value = "{}.{}".format(args[0], args[1])
            obj_dict = storage.all()
            if key_value in obj_dict:
                del obj_dict[key_value]
            else:
                print("** no instance found **")
            storage.save()

    def do_all(self, arg) -> None:
        """Prints all string representations of all instances based
           or not on the class name.
           Usage: all <class name>
           Args:
               arg: a string containig command arguments.
        """
        args = arg.split()
        obj_dict = storage.all()
        if len(args) == 0:
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

    def do_update(self, arg) -> None:
        """Updates an instance based on the class name and id by
           adding or updating attribute.
           Usage update <class name> <id> <attribute name> "<attribute value>"
           Args:
               arg: a string containig command arguments.
        """

        attrs = {}
        if "from_func" in arg:
            args = arg
            attrs = json.loads(args[2])
        else:
            args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in CLASSES:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            obj_dict = storage.all()

            if key not in obj_dict:
                print("** no instance found **")
            elif len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                obj = obj_dict[key]
                if len(attrs) > 0:
                    for key, val in attrs.items():
                        setattr(obj, key, val)
                else:
                    attribute_name = args[2]
                    attribute_value = args[3].strip("\"")
                    setattr(obj, attribute_name, attribute_value)
                obj.save()

    def __do_count(self, obj) -> int:
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

    def check_class_name(self, name=""):
        """Check if stdin user typed class name and id."""
        if len(name) == 0:
            print("** class name missing **")
            return False
        else:
            return True

    def check_class_id(self, name=""):
        """Check class id"""
        if len(name.split(' ')) == 1:
            print("** instance id missing **")
            return False
        else:
            return True

    def default(self, line) -> None:
        """ called on an input line when,
            the command prefix is not recognized
            Args:
                line: a string containing commandline arguments
        """
        args = line.split(".", 1)

        if len(args) != 2:
            return cmd.Cmd.default(self, line)

        # Validate that the class in in our classes list
        if args[0] not in CLASSES:
            return cmd.Cmd.default(self, line)

        # Check that we have brackets
        if "(" not in args[1] or ")" not in args[1]:
            return cmd.Cmd.default(self, line)

        # Remove  all unwanted characters
        args = line.replace("(", " ").replace(")", " ")
        args = args.replace('"', '').replace("'", " ").replace(",", "")
        # Remove whitespaces
        args = args.strip()

        if not self.__run_functions(line, args):
            return cmd.Cmd.default(self, line)

    def __run_functions(self, line, args) -> bool:
        """ method to to invoke all the functions
            Args:
                line: string of arguments
                args: an array of arguments
            Return:
                  True if function is run else False
        """
        functions = ["all", "count", "show", "destroy", "update"]

        args_list = args.split(" ")  # get list of arguments
        class_name = args_list[0].split(".")[0]  # Class name
        func_name = args_list[0].split(".")[1]  # The function name
        length = len(args_list)  # length of argument list

        # Check if function is in our list of functions
        if func_name not in functions:
            return False

        del args_list[0]
        # add only the class name instead of <class>.
        args_list.insert(0, class_name)

        if func_name == "all":
            self.do_all(class_name)
            return True
        if func_name == "count":
            self.__do_count(class_name)
            return True
        if func_name == "show":
            self.do_show(" ".join([args_list[x] for x in range(length)]))
            return True
        if func_name == "destroy":
            self.do_destroy(" ".join([args_list[x] for x in range(length)]))
            return True

        # For functions with more than one argument
        new_args = line.split(" ", 1)
        to_data = ""

        if len(new_args) > 1:
            try:
                new_args[1] = new_args[1].replace("'", '"')
                to_data = json.loads(new_args[1].strip(")"))
            except Exception as e:
                to_data = ""

        # Update for if a dictionary is provided in arguments
        if func_name == "update" and isinstance(to_data, dict):
            arr = [class_name, args_list[1], json.dumps(to_data)]
            arr.append("from_func")
            self.do_update(arr)
            return True
        else:
            if length > 4:  # we want to update only one attribute
                length = 4
            arr = [args_list[x].strip(")") for x in range(length)]
            self.do_update(" ".join(arr))
            return True
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
